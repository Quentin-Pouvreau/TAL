import os
import smoothing
import semantic

smoothing.correctCorpus("Corpus_Apprentissage/corpus_apprentissage_07-12-2017_09h25.txt")
semantic.filterBadTweets("correctedCorpus.txt")
os.system("cat badTweets.txt | MElt -L -T > melt_badword.melt")







