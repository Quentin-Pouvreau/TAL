import os
import smoothing
import semantic


clean_tweet = "je suis un tweet"

tweetmelte = os.system("echo "+clean_tweet+" | MElt -L -T")
print(tweetmelte)

''' print(semantic.isBadTweet("Cette Pute"))
smoothing.correctCorpus("Corpus_Apprentissage/corpus_apprentissage_21-11-2017_10h14.txt")
smoothing.majUnigrams()
smoothing.majBigrams()
semantic.filterBadTweets("correctedCorpus.txt")
os.system("cat badTweets.txt | MElt -L -T > melt_badword.melt")
os.system("grew -det -grs POStoSSQ/grs/surf_synt_main.grs -strat full -i melt_badword.melt -f badword.conll -old_grs")'''