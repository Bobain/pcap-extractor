from nfstream import NFStreamer
from src.python.utils import replace_path_prefix, run_cmd, dir_walk_apply
import os
import src.python.env as env


def apply_ndpi(file_path, dir_path_out):
    NFStreamer(source=file_path).to_pandas().to_csv(
        os.path.join(dir_path_out, os.path.split(file_path)[-1] + ".ndpi.csv")
    )


if __name__ == "__main__":
    dir_walk_apply(env.ROOT_DIR, env.TARGET_DIR, apply_ndpi)
