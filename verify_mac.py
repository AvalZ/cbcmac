#! /usr/bin/env python3
import argparse
import pickle
import calculate_mac as cbc


def main():
    parser = argparse.ArgumentParser(description="Verify the CBC-MAC")
    parser.add_argument(metavar="key-filename", dest='keyfile', type=str, help="File containing the AES key")
    parser.add_argument("filename", type=str, help="Input file")
    parser.add_argument("tag_filename", type=str, help="Input tag-file")
    args = parser.parse_args()
    try:
        key = cbc.read_aes_key(args.keyfile)
    except Exception as e:
        print("Cannot read the keyfile {}, error={}".format(args.keyfile, e))
        raise SystemExit(-1)
    try:
        with open(args.tag_filename, "rb") as inFile:
            stored_mac = pickle.load(inFile)
        if not isinstance(stored_mac, bytes) or len(stored_mac) != cbc.BLOCK_SIZE:
            print("I don't understand the format of the tag-file!")
            raise SystemExit(-1)
    except Exception as e:
        print("Cannot read the tag-file, error={}".format(e))
        raise SystemExit(-1)
    try:
        calculated_mac = cbc.aes_cbc_mac(args.filename, key)
    except Exception as e:
        print("Cannot read {}, error={}".format(args.filename, e))
        raise SystemExit(-1)
    if calculated_mac == stored_mac:
        print("{} and {} match.".format(args.filename, args.tag_filename))
    else:
        print("{} and {} do NOT match.".format(args.filename, args.tag_filename))

if __name__ == "__main__":
    main()

