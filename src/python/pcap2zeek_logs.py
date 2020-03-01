from utils import replace_path_prefix, run_cmd
import os


def pcap_extract(data_in, data_out, file_path):
    dir_path_out = replace_path_prefix(file_path, data_in, data_out) + ".zeek.logs"
    os.mkdirs(dir_path_out)
    run_cmd(["cd", dir_path_out, "&&", "zeek", "-Cr", file_path])
