#!/usr/bin/env python
import pickle
import libertyparse
import sys

library_file = sys.argv[1]
pickle_file = sys.argv[2]

with open(library_file, "r") as f:
    lib = f.read()
    print "Parsing {0} ...".format(library_file)
    l = libertyparse.parse(lib)
    print "Dump library into {0} ...".format(pickle_file)
    pickle.dump(l, open(pickle_file, "wb"))
    print "done."
    
