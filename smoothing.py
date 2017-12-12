import enchant
import re

''' Global variables'''
unigrams = dict()
unigramsTxt = open("unigrams.txt", 'r', encoding="utf8")
for line in unigramsTxt:
    if "=" in line:
        unigrams[line.split("=")[0]] = int(line.split("=")[1])
unigramsTxt.close()

bigrams = dict()
bigramsTxt = open("bigrams.txt", 'r', encoding="utf8")
for line in bigramsTxt:
    if "=" in line:
        bigrams[line.split("=")[0]] = int(line.split("=")[1])
bigramsTxt.close()

chkr = enchant.Dict("fr_FR")

''' Methods '''
commonPatterns = dict()
commonPatterns["ya"] = "il y a"
commonPatterns["y'a"] = "il y a"
commonPatterns["il ya"] = "y a"
commonPatterns["1er"] = "premier"
commonPatterns["1 er"] = "premier"
commonPatterns["qd"] = "quand"
commonPatterns["pcq"] = "parce que"
commonPatterns["pq"] = "pourquoi"
commonPatterns["c"] = "c'est"
commonPatterns["ct"] = "c'était"
commonPatterns["dla"] = "de la"
commonPatterns["t'façon"] = "de toute façon"
commonPatterns["tjr"] = "toujours"
commonPatterns["tjrs"] = "toujours"
commonPatterns["t"] = "tu es"
commonPatterns["d"] = "des"
commonPatterns["jms"] = "jamais"
commonPatterns["alr"] = "alors"
commonPatterns["vrmt"] = "vraiment"
commonPatterns["apres"] = "après"
commonPatterns["bo"] = "beau"
commonPatterns["en +"] = "plus"

def tryPattern(previousWord, word):
    bigram = previousWord + " " + word
    if bigram in commonPatterns:
        return commonPatterns[bigram]
    elif word in commonPatterns:
        return commonPatterns[word]
    else:
        return word


accents = dict()
accents['a'] = ('à', 'â', 'ä')
accents['c'] = ('ç',)
accents['e'] = ('è', 'é', 'ê', 'ë')
accents['i'] = ('î', 'ï')
accents['u'] = ('ù', 'û', 'ü')
accents['A'] = ('À', 'Â', 'Ä')
accents['C'] = ('Ç',)
accents['E'] = ('È', 'É', 'Ê', 'Ë')
accents['I'] = ('Î', 'Ï')
accents['U'] = ('Ù', 'Û', 'Ü')


def correctAccent(word):
    for letter in word:
        if letter in accents:
            for accent in accents[letter]:
                correctedWord = word.replace(letter, accent)
                if chkr.check(correctedWord) is True:
                    word = correctedWord
                    break
    return word


def smoothing(previousWord, suggestions):
    correctedWord = None
    max_prob = 0
    for suggestion in suggestions:
        bigram = previousWord + " " + suggestion
        if bigram in bigrams:
            prob = bigrams[bigram] + 1
            prob = prob / (unigrams[previousWord] + len(unigrams))
            if prob > max_prob:
                max_prob = prob
                correctedWord = suggestion
    if correctedWord is None:
        return suggestions[0]
    return correctedWord


def correctUnigram(word):
    if re.search(r"\d+", word) is not None:
        return re.sub(r"(\d+)", r"\1 ", word)
    capitalizedWord = word.capitalize()
    if chkr.check(capitalizedWord) is True:
        return capitalizedWord
    return correctAccent(word)


def correctBigram(previousWord, word):
    word = tryPattern(previousWord, word)
    if chkr.check(word) is not True:
        suggestions = chkr.suggest(word)
        if len(suggestions) > 0:
            return smoothing(previousWord, suggestions)
    return word


def correct(previousWord, word):
    word = correctUnigram(word)
    if chkr.check(word) is not True:
        if previousWord is None:
            suggestions = chkr.suggest(word)
            if len(suggestions) > 0:
                return suggestions[0]
        else:
            return correctBigram(previousWord, word)
    return word


def addUnigram(unigram):
    if unigram in unigrams:
        unigrams[unigram] += 1
    else:
        unigrams[unigram] = 1


def addBigram(bigram):
    if bigram in bigrams:
        bigrams[bigram] += 1
    else:
        bigrams[bigram] = 1


def isCorrect(word):
    if chkr.check(word) is True or word in unigrams:
        return True
    return False


def correctCorpus(corpus):
    corpus = open(corpus, 'r', encoding="utf8")
    correctedCorpus = open("correctedCorpus.txt", 'w', encoding="utf8")
    for line in corpus:
        previousWord = None
        correctedWords = list()
        for word in line.strip().split(" "):
            word.strip()
            if re.search(r"[a-zA-Z0-9ÀÂÄÇÈÉÊËÎÏÙÛÜàâäçèéêëîïùûüœ+]", word) is not None:
                coma = False
                dot = False
                if isCorrect(word) is not True:
                    if word[len(word) - 1] == ',':
                        coma = True
                    elif word[len(word) - 1] == '.':
                        dot = True
                    word = re.sub(r"[^a-zA-Z0-9ÀÂÄÇÈÉÊËÎÏÙÛÜàâäçèéêëîïùûüœ’`'-+]", "", word)
                    word = correct(previousWord, word)
                lowerWord = word.lower()
                if chkr.check(lowerWord) is True:
                    word = lowerWord
                addUnigram(word)
                if previousWord is not None:
                    addBigram(previousWord + " " + word)
                previousWord = word
                if coma:
                    word += ','
                elif dot:
                    word += '.'
            else:
                previousWord = None
            correctedWords.append(word)
        correctedWords[0] = correctedWords[0].capitalize()
        s = " "
        correctedLine = s.join(correctedWords)
        correctedCorpus.write(correctedLine + "\n")
    correctedCorpus.close()
    corpus.close()


def majUnigrams():
    unigramsTxt = open("unigrams.txt", 'w', encoding="utf8")
    for key in unigrams:
        unigramsTxt.write(key + "=" + str(unigrams[key]) + "\n")
    unigramsTxt.close()


def majBigrams():
    bigramsTxt = open("bigrams.txt", 'w', encoding="utf8")
    for key in bigrams:
        bigramsTxt.write(key + "=" + str(bigrams[key]) + "\n")
    bigramsTxt.close()