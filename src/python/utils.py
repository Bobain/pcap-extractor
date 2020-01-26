import os
import subprocess
import datetime
import sys


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
