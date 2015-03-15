#! /usr/bin/env python3
import argparse
import pickle
import Crypto.Cipher.AES as AES
import Crypto.Util.strxor as sxor
import calculate_mac as cbc


BLOCK_SIZE = AES.block_size


def read_file_and_mac(filename):
    try:
        with open(filename, mode="rb") as f:
            data = f.read()
    except Exception as e:
        print(e)
        raise SystemExit(-1)
    try:
        with open(cbc.tag_filename(filename), mode="rb") as f:
            tag = pickle.load(f)
    except Exception as e:
        print(e)
        raise SystemExit(-1)
    return data, tag


def main():
    parser = argparse.ArgumentParser(description="Creates a different file with the same CBC-MAC")
    parser.add_argument("-i1", "--input1", type=str, help="First input file", required=True)
    parser.add_argument("-i2", "--input2", type=str, help="Second input file")
    parser.add_argument("-o", "--output", type=str, help="Output file", required=True)
    args = parser.parse_args()
    (file_data1, mac1) = read_file_and_mac(args.input1)
    if args.input2:
        (file_data2, mac2) = read_file_and_mac(args.input2)
    else:
        (file_data2, mac2) = file_data1, mac1

    #
    # TODO
    #

    try:
        with open(args.output, mode="wb") as f:
            f.write(forged)
    except Exception as e:
        print(e)
        exit(-1)
    if args.input2:
        print("Files {} and {} successfully forged into {}.".format(args.input1, args.input2, args.output))
    else:
        print("File {} successfully forged into {}.".format(args.input1, args.output))

if __name__ == "__main__":
    main()

