import pandas as pd
import app.perplexity as perplexity
import app.repititions as repititions


def check_cohession(essay, topic):
	t=essay
	title=topic
	#for i in var1:
	     # print(i)
	      #trychecking.OnClick(i)

	p_rep=repititions.phrase_rep(t)
	#print('Phrase repitions=',p_rep)
	s_rep=repititions.sent_repitition(t)
	#print('Sentence repitions=',s_rep)
	res=perplexity.get_score(t)
	dictionary_of_paras=perplexity.RunThis(t)   # add to the know more part
	statusp=''
	if res==0:
	    statusp='PASS'
	else:
	    statusp='FAIL'
	#print('Preplexity score=',status)
	relevance=repititions.check_relevance(t,title)
	#print('RElevance Score=',relevance)
	result=repititions.paragraph(t)
	if result==0:
	    status='PASS'
	else:
	    status='FAIL'
	#print('Paragraphs=',status)
	dictnory = {
				'Phrase repitions':p_rep,
				'Sentence repitions':s_rep,
				'Preplexity score':statusp,
				'RElevance Score':relevance,
				'Paragraphs':status,
				'dictionary':dictionary_of_paras
	}
	return dictnory
