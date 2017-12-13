import enchant
import re

''' Global variables'''
unigrams = dict()
unigramsTxt = open("unigrams.txt", 'r', encoding="utf8")
for line in unigramsTxt:
    line = line.strip()
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
commonPatterns["pr"] = "pour"
commonPatterns["qqn"] = "quelqu'un"
commonPatterns["qqc"] = "quelque chose"
commonPatterns["svp"] = "s'il vous plaît"
commonPatterns["stp"] = "s'il te plaît"
commonPatterns["slt"] = "salut"
commonPatterns["c"] = "c'est"
commonPatterns["ct"] = "c'était"
commonPatterns["dla"] = "de la"
commonPatterns["t'façon"] = "de toute façon"
commonPatterns["tfaçon"] = "de toute façon"
commonPatterns["t'facon"] = "de toute façon"
commonPatterns["tfacon"] = "de toute façon"
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
commonPatterns["sms"] = "message"


def tryPattern(word, previousWord):
    word = word.lower()
    if previousWord is not None:
        bigram = previousWord + " " + word
        if bigram in commonPatterns:
            return commonPatterns[bigram]
    if word in commonPatterns:
        return commonPatterns[word]
    return None


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
    return correctedWord


def correctUnigram(word):
    capitalizedWord = word.capitalize()
    if chkr.check(capitalizedWord) is True:
        return capitalizedWord
    return correctAccent(word)


def correctWord(previousWord, word):
    correctedWord = tryPattern(word, previousWord)
    if correctedWord is not None:
        return correctedWord
    word = correctUnigram(word)
    if chkr.check(word) is not True:
        suggestions = chkr.suggest(word)
        if previousWord is None:
            if len(suggestions) > 0:
                return suggestions[0]
        else:
            correctedWord = smoothing(previousWord, suggestions)
            if correctedWord is not None:
                return correctedWord
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


def correctTweet(tweet):
    previousWord = None
    correctedWords = list()
    for word in tweet.strip().split(" "):
        if word != "" and word != " " and word is not None:
            word.strip()
            if re.search(r"[a-zA-Z0-9ÀÂÄÇÈÉÊËÎÏÔÙÛÜàâäçèéêëîïôùûüœ+]", word) is not None:
                firstQuote = False
                lastQuote = False
                if word[0] == '"':
                    firstQuote = True
                if word[len(word) - 1] == '"':
                    lastQuote = False
                word = re.sub(r'"', "", word)
                if chkr.check(word) is not True:
                    word = correctWord(previousWord, word)
                if " " in word:
                    for unigram in word.split(" "):
                        addUnigram(unigram)
                addUnigram(word)
                if previousWord is not None:
                    addBigram(previousWord + " " + word)
                previousWord = word
                if firstQuote:
                    word = '"' + word
                    previousWord = None
                if lastQuote:
                    word += '"'
                    previousWord = None
            else:
                previousWord = None
            correctedWords.append(word)
    if len(correctedWords) > 0:
        correctedWords[0] = correctedWords[0].capitalize()
    s = " "
    correctedTweet = s.join(correctedWords)
    return correctedTweet


def correctCorpus(corpus):
    corpus = open(corpus, 'r', encoding="utf8")
    correctedCorpus = open("correctedCorpus.txt", 'w', encoding="utf8")
    for line in corpus:
        correctedLine = correctTweet(line)
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