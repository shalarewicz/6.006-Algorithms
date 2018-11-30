#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
from kfasta import *

### Utility classes ###


# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = {}
        for (key, value) in pairs:
            self.put(key, value)

    # Associates the value v with the key k.
    def put(self, k, v):
        if self.dict.has_key(k):
            self.dict[k].append(v)
        else:
            self.dict[k] = [v]

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        values = self.dict.get(k)
        if values is None:
            return []
        else:
            return values

    def keys(self):
        return self.dict.keys()

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):

    if k < 0:
        raise RuntimeError("Subsequence cannot have negative length")

    subseq = ''
    for i in range(0,k):
        subseq += next(seq)
    h = RollingHash(subseq)

    index = 0
    while True:
        try:
            yield subseq, h.current_hash(), index
            c = next(seq)
            h.slide(subseq[0], c)
            subseq = subseq[1:k] + c
            index += 1
        except StopIteration:
            break


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    if k < 0:
        raise RuntimeError("Subsequence cannot have negative length")
    if m < k:
        raise RuntimeError("Subsequence length must be less than the interval, m")
    else:
        j = 0
        while True:
            subseq = ''
            try:
                for i in range(0, k):
                    subseq += next(seq)
                yield subseq, RollingHash(subseq).current_hash(), j
                for i in range(0, m-k):
                    next(seq)
                j += m
            except StopIteration:
                break


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    seqA = intervalSubsequenceHashes(a, k, m)
    # seqA = subsequenceHashes(a, k)
    seqB = subsequenceHashes(b, k)
    dictA = Multidict([])
    dictB = Multidict([])

    while True:
        try:
            keyA, hashA, position = next(seqA)
            dictA.put(hashA, position)
        except StopIteration:
            break

    while True:
        try:
            keyB, hashB, position = next(seqB)
            dictB.put(hashB, position)
        except StopIteration:
            break

    for subseq in dictA.keys():
        locationsInB = dictB.get(subseq)
        for location in locationsInB:
            for x in dictA.get(subseq):
                yield (x, location)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
