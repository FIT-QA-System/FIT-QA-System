import pickle
# import spacy
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
from nltk import word_tokenize, \
    pos_tag  ##implementation of similarity() from http://nlpforhackers.io/wordnet-sentence-similarity/
from nltk import word_tokenize, pos_tag, ne_chunk

# news_path = 'data/news.txt'
news_path = './QA/data/news.txt'


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def pathsim(ss1, ss2):
    if ss1.path_similarity(ss2) is None:
        return 0
    return ss1.path_similarity(ss2)


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    NoneType = type(None)
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence1nv = []
    sentence2 = pos_tag(word_tokenize(sentence2))
    sentence2nv = []
    # Get the synsets for the tagged words
    synsets1 = []
    count1 = 0
    count2 = 0
    tup = ()
    synsetnone1 = []
    for tagged_word in sentence1:
        if type(tagged_to_synset(*tagged_word)) == NoneType and tagged_word[0][0].isupper() and penn_to_wn(
                tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
            synsetnone1.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
    synsets2 = []
    tup = ()
    synsetnone2 = []
    for tagged_word in sentence2:
        if type(tagged_to_synset(*tagged_word)) == NoneType and tagged_word[0][0].isupper() and penn_to_wn(
                tagged_word[1]) == 'n':
            count2 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
            synsetnone2.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count2 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
    synsets1 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence1nv]
    synsets2 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence2nv]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if not type(ss) == NoneType]
    synsets2 = [ss for ss in synsets2 if not type(ss) == NoneType]
    score = 0.0
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets2 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets2])
            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synset in synsets2:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets1 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets1])
            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synsetnone in synsetnone2:
        if synsetnone in synsetnone1:
            score += 1
    for synsetnone in synsetnone1:
        if synsetnone in synsetnone2:
            score += 1
    # Average the values
    score /= (count1 + count2)
    return score


def match(words, line):
    hit = 0
    qs = line.split()
    n = len(words)
    for word in words:
        if word == None:
            n = n - 1
            continue
        if word in line:
            hit = hit + 1
    return hit / n


def answernews(question):
    # nlp = spacy.load("en")
    # who, when, where
    if "who" in question or "Who" in question:  # named entity checking
        words = question.split()
        qs = pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i] = None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open(news_path, 'r').readlines()):
            if match(words, line) > 0.75:
                # print(match(words,line))
                # print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label() == "PERSON":
                        name = ""
                        for leaf in subtree.leaves():
                            name = name + leaf[0] + ' '
                        return name
                return line
    if "when" in question or "When" in question:
        words = question.split()
        qs = pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i] = None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open(news_path, 'r').readlines()):
            if match(words, line) > 0.70:
                # print(match(words,line))
                # print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label() == "CD":
                        place = ""
                        for leaf in subtree.leaves():
                            place = place + leaf[0]
                        return place
                return line
    if "where" in question or "Where" in question:
        words = question.split()
        qs = pos_tag(word_tokenize(question))
        for i in range(len(words)):
            if penn_to_wn(qs[i][1]) != 'n':
                words[i] = None
            elif words[i][0].isupper:
                words.append(words[i])
        for index, line in enumerate(open(news_path, 'r').readlines()):
            if match(words, line) > 0.70:
                # print(match(words,line))
                # print(ne_chunk(pos_tag(word_tokenize(line))))
                for subtree in ne_chunk(pos_tag(word_tokenize(line))).subtrees():
                    if subtree.label() == "GPE" or subtree.label() == "ORGANIZATION":
                        place = ""
                        for leaf in subtree.leaves():
                            place = place + leaf[0] + ' '
                        return place
                return line
    else:
        for index, line in enumerate(open(news_path, 'r').readlines()):
            if sentence_similarity(line, question) > 0.70:
                return line


def filt(x):
    return x.label() == 'Person'


if __name__ == "__main__":
    news_path = 'data/news.txt'
    print(answernews("who is the president of Florida Tech"))
    print(answernews("who is the city attorney for the city of Melbourne"))
    print(answernews("who is the Athletic Director"))
    print(answernews("where does F. Alan Smith live"))
    print(answernews("where is the hands-on approach to education event"))
    print(answernews("who is awarded the FAS Medal"))
    print(answernews("when is Hope X"))
    # load / save models
