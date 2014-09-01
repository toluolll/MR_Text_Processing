#!/usr/bin/env python

from operator import itemgetter
import sys

def main(debug=0, separator="_____@@@@@_____"):
    currentArticle = None

    for line in sys.stdin:
        line = line.strip()

        if debug == 1:
            print "Line to be reduced"
            print line

        # Get elements of pair created by the mapper
        article_path, positions, sentence, parse_tree = line.split(separator)

        if debug == 1:
            print articles_path
            print "Positions"
            print positions
            print "Sentence"
            print sentence
            print "Parse_tree"
            print parse_tree

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
        if currentArticle != article_path:
            if currentArticle is not None:
                print('%s%s%s%s%s%s%s' % (
                    currentArticle, 
                    separator, 
                    sentence, 
                    separator, 
                    "concepts", 
                    separator, 
                    "relations"))
            currencurrentArticle = article_path

    # Output last word group if needed
    if currentCount > 0:
        print('%s\t%d' % (currentWord, currentCount))

if __name__ == "__main__":
    main(debug=1)