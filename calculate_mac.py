#! /usr/bin/env python3
import argparse
import os
import Crypto.Cipher.AES as AES
import binascii
import pickle

TAG_EXTENSION = ".tag"

AES_KEY_SIZE = 16
BLOCK_SIZE = AES.block_size


def pad(data, block_size=BLOCK_SIZE):
    data += b'\xff'
    missing_bytes = block_size - (len(data) % block_size)
    return data + b'\0' * missing_bytes


def aes_cbc_mac(filename, key):
    c = AES.new(key, AES.MODE_CBC, b'\0' * BLOCK_SIZE)
    with open(filename, mode="rb") as f:
        while True:
            b = f.read(BLOCK_SIZE)
            l = len(b)
            if l < BLOCK_SIZE:
                return c.encrypt(pad(b))
            else:
                c.encrypt(b)


def read_aes_key(keyfile):
    with open(keyfile, mode="rb") as f:
        key = pickle.load(f)
    assert len(key) == AES_KEY_SIZE
    return key


def tag_filename(filename):
    return os.path.splitext(filename)[0]+TAG_EXTENSION


def main():
    parser = argparse.ArgumentParser(description="Calculate the CBC-MAC")
    parser.add_argument(metavar="key-filename", dest='keyfile', type=str, help="File containing the AES key")
    parser.add_argument("filenames", nargs="+", metavar="filename", type=str, help="Input files")
    args = parser.parse_args()
    try:
        key = read_aes_key(args.keyfile)
    except Exception as e:
        print(e)
        raise SystemExit(-1)

    for filename in args.filenames:
        if os.path.splitext(filename)[1] == TAG_EXTENSION:
            continue
        try:
            mac = aes_cbc_mac(filename, key)
            print(binascii.hexlify(mac).decode(), filename)
            tf = tag_filename(filename)
            try:
                with open(tf, "wb") as of:
                    pickle.dump(mac, of)
            except Exception as e:
                print("Cannot write {}, error={}".format(tf, e))
        except Exception as e:
            print('?'*32, e)


if __name__ == "__main__":
    main()

