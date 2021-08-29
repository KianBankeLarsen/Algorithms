# Note: When a BitReader is instantiated, it must be given as argument a file
# object opened in binary reading mode ('rb'). When a BitWriter is
# instantiated, it must be given as argument a file object opened in binary
# writing mode ('wb').

# Code is based on http://rosettacode.org/wiki/Bitwise_IO#Python, with changes
# by Rolf Fagerberg.

# Bits are represented by ints, which in Python can be thougth of as infinite
# bitstrings of the form ...000001XXXXXXXXX (positive ints) or ...111110XXXXXXX
# (negative ints). In all situations in the code below, some suffix (of length
# 1, 8, or n) of such bitstrings is the bits in question.

# The code is always passing from left to right in the sequence of bits,
# e.g. when writing to/reading from a byte, or if writing n bits (i.e., these
# will be the rigthmost n bits of the int supplied).

# For writing, note that when flush() is called, a full byte will be written to
# the file by right-filling the byte with 0's (because the accumulator is reset
# to 0 (= ......0000000) after each write). This is the intended
# functionality. If on the other hand flush() is not called after writing has
# finished , the last bits written (up to 7) may be lost.

# If a BitWriter is instantiated via a "with ... as ..." statement, flush()
# will automatically be called (via the __exit__() method).

class BitWriter(object): # "(object)" present to be Python2/3-agnostic
    def __init__(self, f):
        self.accumulator = 0 # the int building up to a full byte to be written
        self.bcount = 0 # number of bits put in the accumulator so far
        self.output = f # the file object we are writing to
                        # (must be opened in binary mode)

    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
 
    def __del__(self):
        try:
            self.flush()
        except ValueError:   # I/O operation on closed file.
            pass
 
    def close(self):
        self.flush()
        self.output.close()
        
    def writebit(self, bit):
        # if a full byte has accumulated, write it out to file
        # and reset accumulater to all 0's:
        if self.bcount == 8:
            self.flush()
        # add the new bit to the accumulator:
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount += 1
 
    def _writebits(self, bits, n):
        while n > 0:
            self.writebit(bits & 1 << n-1)
            n -= 1
 
    def writeint32bits(self, intvalue):
        self._writebits(intvalue, 32)

    def flush(self):
        # Writes current accumulator to file, then
        # resets accumulator to all 0's.

        if self.bcount: # but only if any bits have accumulated
            self.output.write(bytearray([self.accumulator]))
            self.accumulator = 0
            self.bcount = 0
 
class BitReader(object): # "(object)" present to be Python2/3-agnostic
    def __init__(self, f):
        self.input = f # the file object we are reading from
                       # (must be opened in binary mode)
        self.accumulator = 0 # cache of the last byte read
        self.bcount = 0 # number of bits left unread in accumulator
        self.read = 0 # Was last read succesful? [EOF or not?]
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        self.input.close()
        
    def readsucces(self):
        return self.read
    
    def readbit(self):
        if not self.bcount: # if bcount == 0 [no unread bits in accumulator]
            a = self.input.read(1)
            if a: # if not EOF [EOF = attempt at reading returns empty list]
                self.accumulator = ord(a) # int between 0 and 256, [note that
                                          # ord works for byte objects]
            self.bcount = 8 # number of bits available
            self.read = len(a) # remember number of bytes read (0 => EOF)
        # extract the (bcount-1)'th bit [the next bit] in the accumulator:
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1 # move to next bit in accumulator
        return rv
 
    def _readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v

    def readint32bits(self):
        return self._readbits(32)