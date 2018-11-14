from defaults import *


def get_oov_word(word):
    if any(char.isdigit() for char in word):
        return '<UNK_NUMBER>'

    if any(char in punct for char in word):
        return '<UNK_PUNCT>'

    if any(char.isupper() for char in word):
        return '<UNK_CAP>'

    if any(word.endswith(suffix) for suffix in suffix_NOUN):
        return '<UNK_NOUN>'

    if any(word.endswith(suffix) for suffix in suffix_VERB):
        return '<UNK_VERB>'

    if any(word.endswith(suffix) for suffix in suffix_ADJ):
        return '<UNK_ADj>'

    if any(word.endswith(suffix) for suffix in suffix_ADV):
        return '<UNK_ADV>'

    return '<UNKNOWN>'


def get_vocab(file, min_freq=2):
    vocab = {}
    with open(file, 'r') as inputFile:
        content = inputFile.readlines()

        for line in content:
            if not line.strip():
                continue
            else:
                word, _ = line.strip().split("\t")

                # add to vocab
                vocab[word] = vocab.get(word, 0) + 1

        vocab = [k for k, v in vocab.items() if v >= min_freq]
        vocab.extend(UNK_WORDS)
        vocab = dict.fromkeys(sorted(vocab))

    return vocab


def initialize(file, vocab):
    POS_WORD = {}
    POS_POS = {}

    with open(file, 'r') as inputFile:
        content = inputFile.readlines()

        previous = "<START_END>"
        for line in content:

            if not line.strip():
                word, tag = '<NEWLINE>', "<START_END>"
            else:
                word, tag = line.strip("\n").split("\t")
                if word not in vocab:
                    word = get_oov_word(word)

            # populates the word dictionary
            POS_WORD[tag] = POS_WORD.get(tag, {})
            POS_WORD[tag][word] = POS_WORD[tag].get(word, 0) + 1

            # populates the POS dictionary for emission with values following it:
            POS_POS[previous] = POS_POS.get(previous, {})
            POS_POS[previous][tag] = POS_POS[previous].get(tag, 0) + 1

            previous = tag

        TRANS = makeTransitionTable(POS_POS)
        EMISS = makeLikelihoodTable(POS_WORD, vocab)

    return EMISS, TRANS


def makeTransitionTable(POS_POS):
    TRANS = {}
    pos_num = len(POS_POS)
    for prev in POS_POS.keys():
        TRANS[prev] = {}
        total = sum(POS_POS[prev].values())
        for next in POS_POS.keys():
            next_count = POS_POS[prev].get(next, 0)
            TRANS[prev][next] = (next_count + ALPHA) / (total + ALPHA * pos_num)

        probs_sum = 0.0
        for next in POS_POS.keys():
            probs_sum += TRANS[prev][next]

        assert (abs(probs_sum - 1) < 1e-8)

    return TRANS


def makeLikelihoodTable(POS_WORD, vocab):
    EMISS = {}
    word_num = len(vocab)
    for pos in POS_WORD.keys():
        EMISS[pos] = {}
        total = sum(POS_WORD[pos].values())
        for word in vocab.keys():
            pos_word_count = POS_WORD[pos].get(word, 0)
            EMISS[pos][word] = (pos_word_count + ALPHA) / (total + ALPHA * word_num)

        probs_sum = 0.0
        for word in vocab.keys():
            probs_sum += EMISS[pos][word]

        assert (abs(probs_sum - 1) < 1e-8)

    return EMISS
