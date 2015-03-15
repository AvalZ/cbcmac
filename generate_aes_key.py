#! /usr/bin/env python3
import os
import argparse
import pickle

AES_KEY_SIZE = 16


def main():
    parser = argparse.ArgumentParser(description="Generates a random AES key")
    parser.add_argument("output", type=str, help="Output file")
    args = parser.parse_args()
    random_key = os.urandom(AES_KEY_SIZE)
    with open(args.output, mode="wb") as f:
        pickle.dump(random_key, f)
    print("File {} has been successfully written.".format(args.output))

if __name__ == "__main__":
    main()
