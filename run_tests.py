import glob
import os

ignore = []


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


if __name__ == "__main__":
    files = [f for f in glob.glob("./tests/**/*.py")] + [f for f in glob.glob("./tests/*.py")]
    for f in files:
        if f in ignore:
            continue
        path, filename = os.path.split(f)
        with cd(path):
            exitcode = os.system("python %s" % filename)
            if exitcode != 0:
                assert False, "Testfile %s was not successful!" % f
            else:
                print("Testfile %s was successful!" % f)
    print('Done tests')
