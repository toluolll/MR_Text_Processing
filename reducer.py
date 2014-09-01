#!/usr/bin/env python

from operator import itemgetter
import sys
import time
from _chrefliterals import WordsDict, findLiterals, TextTag, TextTagList, normLiteral

ABBR_MAX = 4
DictWords = WordsDict('/usr/share/dict/words', ABBR_MAX)
DictWords.insert('I')
DictWords.insert('a')

knownNotLiterals = dict.fromkeys((
    'i.e.', 'ie.',
    'c.f.', 'cf.', 'cf',
    'e.g.', 'eg.',
    'de', 'De'  # for de in the names of Universities
))
stopwords = []

def get_terms_from_string(sentence, literals=None):
    """
    Extract terms from a given string of text
    :param literals: pre-defined list of literals to search in text
    """

    tag_list = TextTagList()
    start = 0
    split_re = re.compile('\w+|\W', flags=re.U)
    non_word = re.compile('^\W$', flags=re.U)

    for tag in split_re.findall(sentence):
        if tag:
            if non_word.match(tag):
                tag_type = TextTag.Type.CHARACTER
            else:
                tag_type = TextTag.Type.WORD

            tag_list.append(TextTag(tag_type, start, start + len(tag), unicode(tag).encode('utf-8')))
            start += len(tag)
    literalTags = findLiterals(tag_list, literals, knownNotLiterals,
                               DictWords, stopwords, 0, False)
    return literalTags

def norm_literal(literal):
    """Return normalized literal form"""
    literal = str(literal.encode('utf-8', 'ignore'))
    n_literal = normLiteral(literal, DictWords, stopwords, False)
    return n_literal.decode('utf-8', 'ignore')

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

        # TODO: extract concepts
        tag_list = get_terms_from_string(article.article_text, temp_literals)
        tag_tuple_list = [(l.value, l.start, l.end) for l in tag_list]

        # TODO: extract relations
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
