from bitIO import *
from Element import Element
from PQHeap import PQHeap
import os

class Huffman:
    """
    Huffman compression and decompression.

    Authors:
    - Kian Banke Larsen (kilar20)
    - Silas Pockendahl (silch20)
    """

    HEADER_SIZE = 1024

    def _createHuffmanTree(freqs):
        """
        Creates and returns a Huffman tree,
            given a map (list) from byte to frequency.
        """

        q = PQHeap()
        
        # Build heap with key as freq, value as Node
        for byte in range(256):
            q.insert(Element(freqs[byte], [byte]))
        
        # Build Huffman tree
        for i in range(255): # leave one element
            x = q.extractMin()
            y = q.extractMin()
            freq = x.key + y.key
            q.insert(Element(freq, [x.data, y.data]))

        # Return root of the tree
        return q.extractMin().data

    def _createLookupTable(tree):
        """
        Create a lookup table for a Huffman tree.
        The table (list) maps bytes to a tuple (code, num_of_bits),
            where `code` is the compact binary representation,
            and `num_of_bits` is the number of bits in the representation.
        """
        lookup = [None] * 256

        # Function for recursive tree traversal
        def recurse(subtree, code, num_of_bits):
            if len(subtree) == 1:
                # `subtree` is a leaf
                lookup[subtree[0]] = (code, num_of_bits)
            else:
                # Not a leaf, both subtrees must exist
                # We are aware that we do not store the huffman codes as strings, 
                #   but this change has been approved by Rolf Fagerberg
                recurse(subtree[0], code << 1, num_of_bits + 1)     # left  => 0
                recurse(subtree[1], code << 1 | 1, num_of_bits + 1) # right => 1

        # Start recursion
        recurse(tree, 0, 0)
        return lookup

    def compress(input_file, output_file):
        """
        Reads `input_file`, applies Huffman compression and writes to `output_file`.
        Returns number of bytes read, and number of bytes written to output file.
        """

        freqs = [0] * 256

        # Not necessary for functionality
        bits_written = 1024 * 8 # header size in bits
        
        with open(input_file, "rb") as input_file:

            # Count bytes
            byte = input_file.read(1)
            while byte:
                freqs[byte[0]] += 1
                byte = input_file.read(1)
            
            tree = Huffman._createHuffmanTree(freqs)
            table = Huffman._createLookupTable(tree)
            
            # Count output bits ()
            for byte in range(256):
                bits_written += table[byte][1] * freqs[byte]
            
            # BitWriter handles padding
            with BitWriter(open(output_file, "wb")) as output:

                # Write frequency header
                for byte in range(256):
                    output.writeint32bits(freqs[byte])
                
                # Resets the cursor state
                input_file.seek(0)
                
                # Encode input file
                byte = input_file.read(1)
                while byte:
                    code, bits = table[byte[0]]
                    byte = input_file.read(1)
                
                    # Very similar to `BitWriter._writebits`,
                    #   writes the bits one by one
                    while bits > 0:
                        output.writebit((code >> bits-1) & 1)
                        bits -= 1
                    
        # Return bytes read and bytes written
        return sum(freqs), (bits_written + 7) // 8

    def decompress(input_file, output_file):
        """
        Reads `input_file`, applies Huffman decompression and writes to `output_file`.
        Returns number of bytes read, and number of bytes written to output file.
        """

        # Not necessary for functionality
        input_size = os.path.getsize(input_file)
        output_length = 0

        with BitReader(open(input_file, "rb")) as input_file:

            # Read frequence header
            freqs = [input_file.readint32bits() for _ in range(256)]

            if not input_file.readsucces():
                # not enough data for header
                raise Exception("Could not read header (too short)")
            
            # Count output bytes
            output_length = sum(freqs)

            # Frequency table => Huffman tree
            tree = Huffman._createHuffmanTree(freqs)
            
            with open(output_file, "wb") as output:
                
                # Repeat for number of characters in output
                for _ in range(output_length):
                    x = tree
                    # Traverse tree until a leaf/corresponding byte is found
                    while len(x) == 2:
                        bit = input_file.readbit()
                        if not input_file.readsucces():
                            raise Exception("Not enough data, unexpected EOF")
                        x = x[bit] # 0 => left, 1 => right
                    output.write(bytes(x))

        # Return bytes read and bytes written
        return input_size, output_length
