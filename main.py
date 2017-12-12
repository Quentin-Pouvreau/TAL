import os
import smoothing
import semantic

smoothing.correctCorpus("Corpus_Apprentissage/corpus_apprentissage_14_11_2017_07h51.txt")
smoothing.majUnigrams()
smoothing.majBigrams()
semantic.filterBadTweets("correctedCorpus.txt")
'''os.system("cat badTweets.txt | MElt -L -T > melt_badword.melt")'''







