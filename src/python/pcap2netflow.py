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


def pcap_2_nflow(pcap_file_path):
    # TODO : couldn't we pipe processes instead of writing intermediry files to disk?
    nflow_dir = pcap_file_path.replace(ROOT_DIR, target_dir).replace(
        ".pcap", "pcap.nflow"
    )
    os.mkdir(nflow_dir)
    run_cmd(
        ["nfpcapd", "-r", "%s" % pcap_file_path, "-l", "%s" % nflow_dir,]
    )
    return nflow_dir


def nflow_2_netflows(dir_4_nflows):
    output_file_path = "%s.csv" % dir_4_nflows.replace(ROOT_DIR, target_dir).replace(
        ".nflow", ".netflow"
    )
    run_cmd(
        [
            "nfdump",
            "-B",
            "-R",
            "%s" % dir_4_nflows,
            "-b",
            "-o",
            "extended",
            "-o",
            "csv",
        ],
        output_file_path,
    )
    shutil.rmtree(dir_4_nflows, ignore_errors=False, onerror=None)
    return output_file_path


def pcap_2_netflows(pcap_file_path):
    nflow_2_netflows(pcap_2_nflow(pcap_file_path))


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
                pcap_2_netflows(os.path.join(file_path))
