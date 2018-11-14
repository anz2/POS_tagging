from initialize import get_oov_word, initialize, get_vocab
from math import log


def viterbi(POS, WORDS, EMISS, TRANS):
    state_prob = dict.fromkeys(POS)
    previous_pos = dict.fromkeys(POS)

    T = len(WORDS)

    # initial transitions from start
    for pos in POS:
        state_prob[pos] = [0] * T
        previous_pos[pos] = [0] * T

    # Prepare For Forward Pass
    for pos in POS:
        if abs(TRANS['<START_END>'][pos] - 0) < 1e-7:
            state_prob[pos][0] = float('-inf')
        else:
            state_prob[pos][0] = log(TRANS['<START_END>'][pos]) + log(EMISS[pos][WORDS[0]])

        previous_pos[pos][0] = "<START_END>"

    # Forward Pass
    for j, word in enumerate(WORDS[1:]):

        if j + 1 % 100 == 0:
            print(f'{j+1}/{len(WORDS)} done...')

        for curr_pos in POS:

            max_prob = float('-inf')
            max_prob_pos = ""

            for prev_pos in POS:
                cur_prob = state_prob[prev_pos][j] + log(TRANS[prev_pos][curr_pos]) + log(EMISS[curr_pos][word])

                if max_prob < cur_prob:
                    max_prob = cur_prob
                    max_prob_pos = prev_pos

            state_prob[curr_pos][j + 1] = max_prob
            previous_pos[curr_pos][j + 1] = max_prob_pos

    # Find Last Pos
    best_path_prob = float('-inf')
    last_pos = ""
    for cur_pos in POS:
        cur_prob = state_prob[cur_pos][T - 1]
        if best_path_prob < cur_prob:
            best_path_prob = cur_prob
            last_pos = cur_pos

    # Backward Pass
    best_path = [last_pos]
    curr_pos = last_pos
    for j in range(T - 1, 0, -1):
        best_path.append(previous_pos[curr_pos][j])

    return {'tags': best_path[-1::-1]}


def read_file(filename, vocab):
    with open(filename, 'r') as file:
        words, orig_words, tags = [], [], []

        for line in file.readlines():
            if not line.strip():
                word = '<NEWLINE>'
            elif line.strip() not in vocab:
                word = get_oov_word(line.strip())
            else:
                word = line.strip()

            orig_words.append(line.strip())
            words.append(word)

    return orig_words, words


def write_file(filename, text):
    with open(filename, 'w') as file:
        for word, tag in zip(text['words'], text['tags']):
            if not word:
                file.write('\n')
            else:
                file.write(word + '\t' + tag + '\n')


if __name__ == '__main__':
    train_file = 'WSJ_02-21.pos'
    # train_file ='wsj_train.pos'
    # train_file = "trainingFile.pos"
    test_file = "WSJ_24.words"
    results_file = 'new_results.pos'

    vocab = get_vocab(train_file)
    EMISS, TRANS = initialize(train_file, vocab)
    pos = list(EMISS.keys())

    orig_words, words = read_file(test_file, vocab)

    result = viterbi(pos, words, EMISS, TRANS)

    result['words'] = orig_words

    print(f'saving results...')
    write_file(results_file, result)
