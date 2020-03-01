from utils import clean_then_raise, run_cmd
import shutil
import os


@clean_then_raise(lambda _, unzip_dir: shutil.rmtree(unzip_dir, ignore_errors=True))
def unzip(zip_file, unzip_dir):
    if not os.path.exists(unzip_dir):
        os.makedirs(unzip_dir)
    run_cmd(["unzip", zip_file, "-d", unzip_dir], no_stdout=False)


@clean_then_raise(lambda _, unrar_dir: shutil.rmtree(unrar_dir, ignore_errors=True))
def unrar(rar_file, unrar_dir):
    if not os.path.exists(unrar_dir):
        os.makedirs(unrar_dir)
    run_cmd(["unrar", "x", "-r", rar_file, unrar_dir], no_stdout=False)


DECOMPRESS_FUNCS = [
    (lambda x: (x.endswith("pcap.zip") and not(os.path.split(x)[1].startswith("."))), unzip),
    (lambda x: (x.endswith("pcap.rar") and not(os.path.split(x)[1].startswith("."))), unrar),
]
