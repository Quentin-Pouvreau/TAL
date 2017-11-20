import enchant
import re

corpusUnigram = dict()
corpusUnigramTxt = open("corpusUnigram.txt", 'r', encoding="utf8")
for line in corpusUnigramTxt:
    try:
        corpusUnigram[line.split("=")[0]] = int(line.split("=")[1])
    except:
        None
corpusUnigramTxt.close()

corpusBigram = dict()
corpusBigramTxt = open("corpusBigram.txt", 'r', encoding="utf8")
for line in corpusBigramTxt:
    try:
        corpusBigram[line.split("=")[0]] = int(line.split("=")[1])
    except:
        None
corpusBigramTxt.close()

chkr = enchant.Dict("fr_FR")
V = len(corpusUnigram)

corpus = open("corpus_test.txt", 'r', encoding="utf8")
for line in corpus:
    prev_word = None
    for word in line.split(" "):
        word = re.sub(r"[^a-zA-Z0-9ÀÂÄÇÈÉÊËÎÏÙÚÛÜàâäçèéêëîïùúûüœ ’`'-]", "", word)
        try:
            if word in corpusUnigram:
                corpusUnigram[word] = corpusUnigram[word] + 1
            elif chkr.check(word) is True:
                corpusUnigram[word] = 1
        except:
            None
        if prev_word is not None:
            bigram = prev_word + " " + word
            print(bigram)
            try:
                if bigram in corpusBigram:
                    corpusBigram[bigram] = corpusBigram[bigram] + 1
                elif chkr.check(word) is True & chkr.check(prev_word) is True:
                    corpusBigram[bigram] = 1
                elif chkr.check(word) is not True:
                    print("Error : " + word)
                    max_prob = 0
                    correct_word = None
                    suggestions = chkr.suggest(word)
                    print(suggestions)
                    for suggestion in suggestions:
                        bigram = prev_word + " " + suggestion
                        if bigram in corpusBigram:
                            try:
                                prob = corpusBigram[bigram] + 1
                                prob = prob/(corpusUnigram[prev_word] + V)
                                if prob > max_prob:
                                    max_prob = prob
                                    correct_word = suggestion
                            except:
                                print("CALC PROB ERROR")
                    if correct_word is not None:
                        print("Correction : " + correct_word)
                        '''answer = input("Is that correct ? [Y/n] ").lower()
                        while answer != 'y' & answer != 'n':
                            answer = input("Please, answer by 'y' or 'n' ").lower()
                        if answer == 'y':'''
                        word = correct_word
                        bigram = prev_word + " " + word
                        if word in corpusUnigram:
                            corpusUnigram[word] += 1
                        else:
                            corpusUnigram[word] = 1
                        if bigram in corpusBigram:
                            corpusBigram[bigram] += 1
                        else:
                            corpusBigram[bigram] = 1
                    else:
                        print("NO CORRECTION")
            except:
                None
        prev_word = word
corpus.close()

print(len(corpusUnigram))

corpusUnigramTxt = open("corpusUnigram.txt", 'w', encoding="utf8")
'''corpusUnigramTxt.write("\n")'''
for key in corpusUnigram:
    corpusUnigramTxt.write(key + "=" + str(corpusUnigram[key]) + "\n")
corpusUnigramTxt.close()

corpusBigramTxt = open("corpusBigram.txt", 'w', encoding="utf8")
'''corpusBigramTxt.write("\n")'''
for key in corpusBigram:
    corpusBigramTxt.write(key + "=" + str(corpusBigram[key]) + "\n")
corpusBigramTxt.close()