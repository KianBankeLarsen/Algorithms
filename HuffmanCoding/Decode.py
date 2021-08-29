"""
Huffman decoding/decompression script

Authors:
    - Kian Banke Larsen (kilar20)
    - Silas Pockendahl (silch20)
"""

from Huffman import Huffman
from sys import argv

if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: python {argv[0]} <input file> <output file>")
    else:
        print(f"Decompressing '{argv[1]}'...")
        try:
            s0, s1 = Huffman.decompress(argv[1], argv[2])
            # size without header
            s2 = s0 - Huffman.HEADER_SIZE
            ratio = 100 * (s1-s2) // s2 if s2 != 0 else 0
            print(f"Wrote to '{argv[2]}'.")
            print(f" - Input size: {s0:>12}")
            print(f" - Output size:{s1:>12}")
            print(f" - Expanded by:{ratio:>11}% (ignoring header)")
        except FileNotFoundError:
            print(f"The file '{argv[1]}' was not found")
        except KeyboardInterrupt:
            print("Decompression interrupted")
        except Exception as e:
            print(f"Decompression failed: {e}")