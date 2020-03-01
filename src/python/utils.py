import os
import subprocess
import datetime
import sys
import warnings
import shutil

PARALLELIZE = True


def run_cmd(cmd, file=None, verbose=True, no_stdout=True):
    if verbose:
        print("%s running : %s" % (datetime.datetime.now().isoformat(), " ".join(cmd)))
    if file is not None:
        with open(file, "w+") as f:
            subprocess.run(cmd, check=True, stdout=f, stderr=sys.stderr)
    else:
        subprocess.run(
            cmd,
            check=True,
            stdout=(subprocess.DEVNULL if (no_stdout or not verbose) else sys.stdout),
            stderr=sys.stderr,
        )


def replace_path_prefix(path, prefix2sub, prefixtarget):
    assert path[: len(prefix2sub)] == prefix2sub
    return os.path.join(prefixtarget, path[len(prefix2sub) :])


def clean_then_raise(cleaning_func):
    def safe_call_decorator(func):
        def function_wrapper(*kargs, **kwargs):
            try:
                return func(*kargs, **kwargs)
            except:
                cleaning_func(*kargs, **kwargs)
                raise

        return function_wrapper

    return safe_call_decorator


def extract_recursive(
    data_in,
    data_out,
    pcap_extract,
    condition=None,
    decompress_funcs=None,
    sub_dir2extract=None,
    delete_uncompressed_data=True,
    skip_errors=False,
    temp_dir=None,
):

    skipped_files = []
    error_files = []
    if condition is None:
        condition = lambda x: x.endswith(".pcap")
    if decompress_funcs is None:
        decompress_funcs = []
    if sub_dir2extract is None:
        sub_dir2extract = data_in
    if temp_dir is None:
        temp_dir = "/tmp"
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
                        dir4dec = replace_path_prefix(file_path, data_in, temp_dir)
                        dec_func(file_path, dir4dec)
                        skipped_files_tmp, error_files_tmp = extract_recursive(
                            data_in,
                            data_out,
                            pcap_extract,
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


def main(root_dir, target_dir, extractor, temp_dir=None):
    if temp_dir is None:
        temp_dir = "/tmp"
    try:
        print("Starting to extract data")
        assert os.path.exists(root_dir), "<%s> does not exist" % root_dir
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        skipped_files, error_files = extractor()

        print("We skipped the following files : \n\t" + ("\n\t".join(skipped_files)))
        if len(error_files):
            print(
                ("We got %d errors : \n" % len(error_files))
                + ("\n\t".join(error_files))
            )
        print("Job done, find converted files here: " + target_dir)
    except:
        print("Fuck...", flush=True)
        # TODO delete temp dir content?
        raise


def parallel_extract():
    # unb.ca CIC IDS 2018 : https://www.unb.ca/cic/datasets/ids-2018.html
    if PARALLELIZE:  # far from a good way to parallelize : IDC for now
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
