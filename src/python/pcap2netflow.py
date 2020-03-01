import os
import shutil
import psutil
from utils import (
    clean_then_raise,
    run_cmd,
    replace_path_prefix,
    extract_recursive,
    main,
)
from decompressing import DECOMPRESS_FUNCS
from multiprocessing import Pool

SKIP_ERRORS4unbca = True

ROOT_DIR = "/data_in/"
TARGET_DIR = "/data_out/"
TEMP_DIR = "/tmp/"



num_cpus = psutil.cpu_count(logical=False)
print("Nb CPU : %d" % num_cpus)

# ROOT_DIR = "/Volumes/ELEMENTS/downlods/CICIDS2018/Original Network Traffic and Log data/"
# TARGET_DIR = "/Volumes/ELEMENTS/downlods/CICIDS2018/netflows"
# TEMP_DIR = "/Users/romainburgot/tmp/"


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
    #
    # removed "-B", for CIC IDS 2018
    for f in sorted(os.listdir(dir_4_nflows)):
        run_cmd(
            [
                "nfdump",
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


def ecicids_2018(sub_dir2extract=None):
    extract_recursive(
        ROOT_DIR,
        TARGET_DIR,
        pcap_extract=pcap_extract,
        condition=lambda x: not (
            x.endswith(".zip")
            | x.endswith(".rar")
            | ("logs.zip" in os.path.split(x)[1])
            | ("pcap.zip" in os.path.split(x)[1])
            | ("pcap.rar" in os.path.split(x)[1])
            | x.endswith(".DS_Store")
        ),
        decompress_funcs=DECOMPRESS_FUNCS,
        sub_dir2extract=sub_dir2extract,
        skip_errors=SKIP_ERRORS4unbca,
        temp_dir=TEMP_DIR,
    )


if __name__ == "__main__":
    main(ROOT_DIR, TARGET_DIR, ecicids_2018, temp_dir=TEMP_DIR)
