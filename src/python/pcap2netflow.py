import os
import shutil
import warnings
import psutil
from .utils import clean_then_raise, run_cmd, replace_path_prefix
from .decompressing import unrar, unzip
from multiprocessing import Pool

SKIP_ERRORS4unbca = True

ROOT_DIR = "/data_in/"
TARGET_DIR = "/data_out/"
TEMP_DIR = "/tmp/"

PARALLELIZE = True

num_cpus = psutil.cpu_count(logical=False)
print("Nb CPU : %d" % num_cpus)

ROOT_DIR = "/Volumes/SSD EVO/Original Network Traffic and Log data/"
TARGET_DIR = "/Users/romainburgot/data_out/"
TEMP_DIR = "/Users/romainburgot/tmp/"


@clean_then_raise(lambda _, nflow_dir: shutil.rmtree(nflow_dir, ignore_errors=True))
def pcap_2_nflow(pcap_file_path, nflow_dir):
    if not (os.path.exists(nflow_dir)):
        os.makedirs(nflow_dir)
    run_cmd(["nfpcapd", "-r", pcap_file_path, "-l", nflow_dir])
    return nflow_dir


def nflow_2_netflows(dir_4_nflows, output_dir_path):
    if not (os.path.exists(output_dir_path)):
        os.makedirs(output_dir_path)
    # This piece of code was aggregating flows at more than five minutes:
    # dir4out_file, _ = os.path.split(output_file_path)
    # if not (os.path.exists(dir4out_file)):
    #     os.makedirs(dir4out_file)
    # run_cmd(
    #     ["nfdump", "-B", "-R", dir_4_nflows, "-b", "-o", "extended", "-o", "csv"],
    #     output_file_path,
    # )
    for f in sorted(os.listdir(dir_4_nflows)):
        run_cmd(
            [
                "nfdump",
                "-B",
                "-r",
                os.path.join(dir_4_nflows, f),
                "-b",
                "-o",
                "extended",
                "-o",
                "csv",
            ],
            "%s.csv" % os.path.join(output_dir_path, f),
        )
    shutil.rmtree(dir_4_nflows, ignore_errors=False, onerror=None)
    return output_dir_path


def pcap_2_netflows(pcap_file_path, nflow_path, output_file_path):
    return nflow_2_netflows(pcap_2_nflow(pcap_file_path, nflow_path), output_file_path)


def pcap_extract(data_in, data_out, file_path):
    if file_path.startswith(TEMP_DIR) and TEMP_DIR != data_in:
        return pcap_2_netflows(
            file_path,
            file_path + ".nflow",
            replace_path_prefix(file_path, TEMP_DIR, data_out) + ".netflows.csv",
        )
    else:
        return pcap_2_netflows(
            file_path,
            replace_path_prefix(file_path, data_in, TEMP_DIR) + ".nflow",
            replace_path_prefix(file_path, data_in, data_out) + ".netflows.csv",
        )


def extract_recursive(
    data_in,
    data_out,
    condition=None,
    decompress_funcs=None,
    sub_dir2extract=None,
    delete_uncompressed_data=True,
    skip_errors=False,
):
    skipped_files = []
    error_files = []
    if condition is None:
        condition = lambda x: x.endswith(".pcap")
    if decompress_funcs is None:
        decompress_funcs = []
    if sub_dir2extract is None:
        sub_dir2extract = data_in
    for r, d, f in os.walk(sub_dir2extract):
        for file in f:
            file_path = os.path.join(r, file)
            print("Having a look at: " + file_path)
            if condition(file_path):
                if skip_errors:
                    try:
                        pcap_extract(data_in, data_out, file_path)
                    except Exception as e:
                        error_files.append((file_path, e))
                        warnings.warn(
                            "Error when extracting data from : %s \n%s"
                            % (file_path, str(e))
                        )
                else:
                    pcap_extract(data_in, data_out, file_path)
            else:
                for cond, dec_func in decompress_funcs:
                    if cond(file_path):
                        dir4dec = replace_path_prefix(file_path, data_in, TEMP_DIR)
                        dec_func(file_path, dir4dec)
                        skipped_files_tmp, error_files_tmp = extract_recursive(
                            data_in,
                            data_out,
                            condition=condition,
                            decompress_funcs=decompress_funcs,
                            sub_dir2extract=dir4dec,
                            delete_uncompressed_data=delete_uncompressed_data,
                            skip_errors=skip_errors,
                        )
                        if delete_uncompressed_data:
                            shutil.rmtree(dir4dec)
                        skipped_files.extend(skipped_files_tmp)
                        error_files.extend(error_files_tmp)
                        break
                else:
                    skipped_files.append(file_path)
    return skipped_files, error_files


def ecicids_2018(sub_dir2extract=None):
    extract_recursive(
        ROOT_DIR,
        TARGET_DIR,
        condition=lambda x: not (
            x.endswith(".zip")
            | x.endswith(".rar")
            | ("logs.zip" in os.path.split(x)[1])
            | ("pcap.zip" in os.path.split(x)[1])
            | ("pcap.rar" in os.path.split(x)[1])
            | x.endswith(".DS_Store")
        ),
        decompress_funcs=[
            (lambda x: (x.endswith("pcap.zip")), unzip),
            (lambda x: (x.endswith("pcap.rar")), unrar),
        ],
        sub_dir2extract=sub_dir2extract,
        skip_errors=SKIP_ERRORS4unbca,
    )


def exemple_unbca_cicids_2018():
    # unb.ca CIC IDS 2018 : https://www.unb.ca/cic/datasets/ids-2018.html
    if PARALLELIZE:
        if num_cpus > 1:
            print("Running %d processes in // " % num_cpus)
            return zip(
                *Pool(num_cpus).map(
                    ecicids_2018,
                    [os.path.join(ROOT_DIR, d) for d in os.listdir(ROOT_DIR)],
                )
            )
        else:
            print("Only %d cpu available : not running in // " % num_cpus)

    return ecicids_2018()


if __name__ == "__main__":
    try:
        print("Starting to extract data")
        assert os.path.exists(ROOT_DIR) and os.path.exists(TEMP_DIR)
        if not os.path.isdir(TARGET_DIR):
            os.mkdir(TARGET_DIR)

        skipped_files, error_files = exemple_unbca_cicids_2018()

        print("We skipped the following files : \n\t" + ("\n\t".join(skipped_files)))
        if len(error_files):
            print(
                ("We got %d errors : \n" % len(error_files))
                + ("\n\t".join(error_files))
            )
        print("Job done, find converted files here: " + TARGET_DIR)
    except:
        print("Fuck...", flush=True)
        # TODO delete temp dir content?
        raise
