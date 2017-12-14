# -*- coding: utf-8 -*-


import os
import smoothing
import semantic




'''semantic.filterBadTweets("MEltedTweets6_short.melt")'''
semantic.filterNegation("resultat.conll")


'''os.system("rm MEltedTweets.melt")
os.system("rm badTweets.melt")
smoothing.correctCorpus("Corpus_Apprentissage/corpus_apprentissage_05-12-2017_04h05.txt")
os.system("cat correctedCorpus.txt | MElt -L -T >> MEltedTweets5.melt")
semantic.filterBadTweets("MEltedTweets1.melt")'''





''' 

from subprocess import Popen,PIPE,STDOUT,run

clean_tweet = "bonjour je m'appel gentil"

proc=run(["echo "+str(clean_tweet)+" | MElt -L -T"], shell=True, stdout=PIPE)
print("Comande is :"+str(proc.stdout))


def cmdline(command):
    process = subprocess.Popen(args=command,stdout=subprocess.PIPE,shell=True)
    return process

print(cmdline("echo "+clean_tweet+" | MElt -L -T"))


result = subprocess.run(["MElt -L -T", clean_tweet], stdout=subprocess.PIPE, shell=True)
print(result.stdout)

tweetmelte = os.system("echo "+clean_tweet+" | MElt -L -T")

print(semantic.isBadTweet("Cette Pute"))
smoothing.correctCorpus("Corpus_Apprentissage/corpus_apprentissage_21-11-2017_10h14.txt")
smoothing.majUnigrams()
smoothing.majBigrams()
semantic.filterBadTweets("correctedCorpus.txt")

os.system("grew -det -grs POStoSSQ/grs/surf_synt_main.grs -strat full -i melt_badword.melt -f badword.conll -old_grs")

os.system("cat badTweets.txt | MElt -L -T > melt_badword.melt")

os.system("cat badTweets.txt | MElt -L -T > melt_badword.melt")

'''