import string

punct = dict.fromkeys(string.punctuation)

suffix_NOUN = ["action", "age", "ance", "cy", "dom", "ee", "ence", "er", "hood", "ion", "ism", "ist", "ity", "ling",
               "ment", "ness", "or", "ry", "scape", "ship", "ty"]
suffix_VERB = ["ate", "ify", "ise", "ize"]
suffix_ADJ = ["able", "ese", "ful", "i", "ian", "ible", "ic", "ish", "ive", "less", "ly", "ous"]
suffix_ADV = ["ward", "wards", "wise"]

UNK_WORDS = ['<UNK_CAP>', '<UNK_PUNCT>', '<UNK_NUMBER>', '<UNK_VBD>', '<UNK_VERB>', '<UNK_NOUN>', '<UNK_ADV>',
             '<UNK_ADj>', '<UNKNOWN>', '<NEWLINE>']

ALPHA = 0.001
