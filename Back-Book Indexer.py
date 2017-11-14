from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import nltk, collections
from nltk.collocations import *
from nltk.corpus import stopwords
import string

def convert(infile, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    converter.close()
    text = output.getvalue()
    output.close
    return text

mainlist=[]
index = {}
for alpha in range(ord('a'), ord('z') + 1):
    index[alpha] = []
infile = file(sys.argv[1], 'rb')
stop_words = set(stopwords.words('english'))
extra_stop_words = ['et', 'al', 'yes', 'no']
for word in extra_stop_words:
    stop_words.add(word)
print 'processing page : '
for i in range(int(sys.argv[2]), int(sys.argv[3])):
    print i
    content = convert(infile, [i])
    content = content.translate(None, string.punctuation)
    content = content.lower()

    frequencies = collections.Counter()
    words = nltk.word_tokenize(content)

    filtered_sentence = [w for w in words if not w in stop_words]

    for w in filtered_sentence:
        frequencies[w] += 1

    bigram=nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(filtered_sentence)
    finder.apply_freq_filter(3)
    bigram_list = finder.nbest(bigram.pmi, 3)
    bigram_list=list(set(bigram_list) - set(mainlist))
    mainlist = mainlist + bigram_list
    #bigram_list=list(set(bigram_list)-set(mainlist))
    print set(bigram_list)
    print set(mainlist)

    if bigram_list:
        for b in bigram_list:
            index[ord(b[0][0])].append((b, i))
infile.close()
f = open('index.txt', 'w')
for alpha in range(ord('a'), ord('z') + 1):
    if len(index[alpha]):
        f.write(chr(alpha).upper() + '_' * 40 + '\n')
        for bigram in index[alpha]:
            length = len(bigram[0][0]) + 1 + len(bigram[0][1])
            f.write(str(bigram[0][0]) + ' ' + str(bigram[0][1]) + ' ' * (30 - length) + str(bigram[1]) + '\n')
f.close()
