from src.python.utils import run_cmd, dir_walk_apply
import os
import src.python.env as env


def apply_zeek(file_path, dir_path_out):
    os.chdir(dir_path_out)
    run_cmd(["zeek", "-Cr", file_path])


if __name__ == "__main__":
    dir_walk_apply(env.ROOT_DIR, env.TARGET_DIR, apply_zeek)
