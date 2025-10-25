import os
import sys

def print_dir_info(directory1, directory2):
    abs1 = os.path.abspath(directory1)
    abs2 = os.path.abspath(directory2)
    pathlist = [abs1, abs2]
    print(f"Directory1 absolute path: {abs1}")
    print(f"Directory2 absolute path: {abs2}")
    print(f"Common Prefix: {os.path.commonprefix(pathlist)}")
    print(f"Common Path: {os.path.commonpath(pathlist)}")
    print(f"Directory2 contents: {os.listdir(abs2)}")
    print(f"Directory1 is directory: {os.path.isdir(abs1)}")


def main():
    if len(sys.argv) <= 1:
        raise Exception("requires two dirs")
    print_dir_info(sys.argv[1], sys.argv[2])

main()
