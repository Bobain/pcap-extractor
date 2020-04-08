from utils import replace_path_prefix, run_cmd
import os


ROOT_DIR = "/data_in/"
TARGET_DIR = "/data_out/"
TEMP_DIR = "/tmp/"


def pcap_extract(data_in, data_out):
    for root, directories, files in os.walk(data_in):
        for f in files:
            file_path = os.path.join(root, f)
            if f.endswith(".pcap") and os.path.isfile(file_path) and not f.startswith("."):
                dir_path_out = (
                    replace_path_prefix(file_path, data_in, data_out) + ".zeek.logs"
                )
                if not(os.path.exists(dir_path_out)):
                    os.makedirs(dir_path_out)
                os.chdir(dir_path_out)
                run_cmd(["zeek", "-Cr", file_path])


if __name__ == "__main__":
    pcap_extract(ROOT_DIR, TARGET_DIR)
