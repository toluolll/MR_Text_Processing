#!/usr/bin/python
import subprocess
import sys, os
import codecs
import time
from tempfile import NamedTemporaryFile

def detect_sentences(text):
    dot_list = []
    for i, c in enumerate(text):
        if c == "." or c == "!" or c == "?":
            if text[i + 1:i + 2] == ' ' or text[i + 1:i + 2] == '\n':
                dot_list.append(i)
	if c == '\n' and not (text[i + 1:i + 2] == ' ' or text[i + 1:i + 2] == '\n'):
	    dot_list.append(i)
    return dot_list

def preprocessText(text):
    # Clean the sentence from the stopwords
    sw = []
    content = [w for w in text.split(" ") if w.lower() not in sw]
    content_without_brackets = []
    i = 0
    while i < len(content):
        el = content[i]
        if "(" not in el:
            content_without_brackets.append(el)
            i += 1
        else:
            while i < len(content) and ")" not in content[i]:
                i += 1
            i += 1

    return " ".join(content_without_brackets).decode("utf-8", "replace")

def main(debug=0, separator="_____@@@@@_____"):
    for line in sys.stdin:
        line = line.strip() # Remove whitespace from beginning and end
        cat = subprocess.Popen(["hadoop", "fs", "-cat", line], stdout=subprocess.PIPE)
        text = ""
        for l in cat.stdout:
            text += l
#	text = os.linesep.join([s for s in text.splitlines() if s])

        if debug == 1:
            print "First 50 characters of the text"
            print text[0:50]

        tag_tuple_list = []
        dot_list = detect_sentences(text)

        if debug == 1:
            print "Dot positions"
            print dot_list

        for el in dot_list:
            tag_tuple_list.append(('.', el, el + 1))
        sorted_tag_list = sorted(tag_tuple_list, key=lambda x: x[1])
        num_elems = len(sorted_tag_list)

        if debug == 1:
            print "Number of sentences (might be +/1 )"
            print num_elems

        i = -1
        while i < num_elems:
            k = i + 1
            if k < num_elems:
                index = 0 if i < 0 else sorted_tag_list[i][2] + 1
                sen = text[index:sorted_tag_list[k][2]]
                if debug == 1:
                    print ('%s\t%s' % (sen, 1))
                preprocessed = preprocessText(sen)
                if debug == 1:
                    print "Preprocessed sentence"
                    print preprocessed
                    time.sleep(3)
                f = NamedTemporaryFile(delete=False)
		filename = f.name
                f.close()
                with codecs.open(filename, 'w', 'utf-8') as fh:
                    fh.write(preprocessed)
                    fh.flush()
                    fh.seek(0)
                    parse_tree = subprocess.Popen(["/home/iuliia.proskurnia/stanford-parser-2012-11-12/lexparser.sh", fh.name], stdout=subprocess.PIPE)\
                            .stdout.read().decode("utf-8").encode('ascii', 'ignore')
		os.unlink(filename)
                if debug == 1:
                    print parse_tree
                print('%s%s%d_%d%s%s%s%s' % (line, separator, index, sorted_tag_list[k][2], separator, sen.replace('\n', '_'), separator, parse_tree.replace('\n', ' ')))
            i += 1

if __name__ == "__main__":
    main(debug=0)
