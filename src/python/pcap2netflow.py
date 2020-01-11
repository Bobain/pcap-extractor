import os
from download_netflow2 import URL_IN_DIR_OUT
import datetime, subprocess, sys
import shutil

# ROOT_DIR = "/private/nfs/09 JEUX DE DONNEES/CU-LID/netflow-public-1/2009_CDX_Datasets"
# ROOT_DIR = "/Users/romainburgot/Downloads/2009_CDX_Datasets"

ROOT_DIR = "/private/nfs/09 JEUX DE DONNEES/CU-LID/netflow-public-2"

ROOT_DIR = "/Users/romainburgot/Downloads/pcap_big_2017"

DIR_4_NFLOW = os.path.join(ROOT_DIR, "nflow")
DIR_4_NETFLOWS = os.path.join(ROOT_DIR, "netflows")


def run_cmd(cmd, file=None):
    print("%s running : %s" % (datetime.datetime.now().isoformat(), " ".join(cmd)))
    if file is not None:
        with open(file, "w+") as f:
            subprocess.run(cmd, check=True, stdout=f, stderr=sys.stderr)
    else:
        subprocess.run(cmd, check=True, stdout=sys.stdout, stderr=sys.stderr)


def pcap_2_nflow(pcap_file_path, dir_4_nflow):
    run_cmd(
        [
            "nfpcapd",
            "-r",
            "%s" % pcap_file_path,
            "-l",
            "%s" % dir_4_nflow,
        ]
    )


def nflow_2_netflows(dir_4_nflow, dir_4_netflows, file_by_file=False):
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


def pcap_2_netflows(pcap_file_path, dir_4_netflows, dir_4_nflow=None, delete_dir4nflow=False):
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
    # used to convert netflow-public-2

    DIR_PCAP = os.path.join(ROOT_DIR, "pcap")
    assert os.path.exists(DIR_PCAP)
    os.mkdir(DIR_4_NFLOW)
    for _, real_pcap_dir in URL_IN_DIR_OUT:
        for f in sorted(os.listdir(real_pcap_dir)):
            if not (f in [".", ".."]):
                pcap_2_nflow(os.path.join(real_pcap_dir, f), DIR_4_NFLOW)

    os.mkdir(DIR_4_NETFLOWS)
    nflow_2_netflows(DIR_4_NFLOW, DIR_4_NETFLOWS)
