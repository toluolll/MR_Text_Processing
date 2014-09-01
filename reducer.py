#!/usr/bin/env python

from operator import itemgetter
import sys
import time

def main(debug=0, separator="_____@@@@@_____"):
    for line in sys.stdin:
        line = line.strip()

        if debug == 1:
            print "Line to be reduced"
            print line

        # Get elements of pair created by the mapper
        article_path, positions, sentence, parse_tree = line.split(separator)

        if debug == 1:
            print article_path
            print "Positions"
            print positions
            print "Sentence"
            print sentence
            print "Parse_tree"
            print parse_tree
	    time.sleep(5)

        # Convert count to an integer
        try:
            pos1, pos2 = positions.split("_")
            pos1 = int(pos1)
            pos2 = int(pos2)
        except ValueError:
            continue

        # Hadoop passes pairs ordered by key (first value), so
        # we can be sure that all pairs with the same key will
        # sent sequentially. When we detect a different one, we
        # won't see that word again.
        print('%s%s%s%s%s%s%s' % (
                    article_path, 
                    separator, 
                    sentence, 
                    separator, 
                    "concepts", 
                    separator, 
                    "relations"))

if __name__ == "__main__":
    main(debug=1)
