import os
import datetime, subprocess, sys
import shutil

ROOT_DIR = "/data"
target_dir = os.path.join(ROOT_DIR, "extracted_from_pcap")


def run_cmd(cmd, file=None):
    print("%s running : %s" % (datetime.datetime.now().isoformat(), " ".join(cmd)))
    if file is not None:
        with open(file, "w+") as f:
            subprocess.run(cmd, check=True, stdout=f, stderr=sys.stderr)
    else:
        subprocess.run(cmd, check=True, stdout=sys.stdout, stderr=sys.stderr)


def pcap_2_nflow(pcap_file_path, dir_4_nflow):
    run_cmd(
        ["nfcapd", "-r", "%s" % pcap_file_path, "-l", "%s" % dir_4_nflow,]
    )


def nflow_2_netflows(dir_4_nflow, dir_4_netflows, file_by_file=True):
    if file_by_file:
        for f in sorted(os.listdir(dir_4_nflow)):
            run_cmd(
                [
                    "nfdump",
                    "-B",
                    "-r",
                    "%s" % os.path.join(dir_4_nflow, f),
                    "-b",
                    "-o",
                    "extended",
                    "-o",
                    "csv",
                ],
                "%s.csv" % os.path.join(dir_4_netflows, f),
            )
    else:
        raise Exception("not yet implemented")


def pcap_2_netflows(
    pcap_file_path, dir_4_netflows, dir_4_nflow=None, delete_dir4nflow=False
):
    if dir_4_nflow is None:
        dir_4_nflow = "./dir_4_nflow"
        delete_dir4nflow = True
    if not os.path.isdir(dir_4_nflow):
        os.mkdir(dir_4_nflow)
    pcap_2_nflow(pcap_file_path, dir_4_nflow)
    nflow_2_netflows(dir_4_nflow, dir_4_netflows)
    if delete_dir4nflow:
        shutil.rmtree(dir_4_nflow, ignore_errors=False, onerror=None)


if __name__ == "__main__":
    assert os.path.exists(ROOT_DIR)
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    for r, d, f in os.walk(ROOT_DIR):
        for file in f:
            file_path = os.path.join(r, file)
            if os.path.isfile(file_path) and file_path.endswith(".pcap"):
                print(
                    "Extracting data from <%s> : <%s> -> <%s>"
                    % (file, file_path, os.path.join(target_dir, file))
                )
                pcap_2_netflows(
                    os.path.join(file_path),
                    dir_4_netflows=os.path.join(target_dir, file),
                )
