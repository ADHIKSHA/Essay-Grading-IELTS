from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from nltk import sent_tokenize
import sys
import csv
import nltk
from nltk.corpus import wordnet
from itertools import groupby
s=nltk.download('punkt')
r=nltk.download('wordnet')
def sent_repitition (t):
    t=t.upper()
    sentence=sent_tokenize(t)
    dict={}
    count=0
    for sent in sentence:
        if sent not in dict:
            dict[sent]=1
        else:
            dict[sent]+=1
    for key, value in dict.items():
        if value>1:
            count+=1
    
    return count

def paragraph(lines):
    para=lines.split("\n")
    no_of_para=len(para)
    #print(para,no_of_para)
    if no_of_para>4:
        flag=0
    else:
        flag=1
    return flag


def phrase_rep(t):
    s=''
    t=t.upper()
    text = word_tokenize(t)
    num_tokens = len(text)
    if num_tokens<3:
        return 0
    dict={}
    count=0
    for j in range(0,num_tokens-3):
        s=''
        for i in range(j,j+2):
            s=s+text[i]
        if s not in dict:
            dict[s]=1
        else:
            dict[s]+=1

    for key,value in dict.items():
        if len(key)>3 and value>3:
            count+=1
            
    return count

   
def check_relevance(t,title):
    t=t.upper()
    title=title.upper()
    text = word_tokenize(t)
    num_tokens = len(text)
    if num_tokens<10:
        return 0
    dict={}
        
    for i in text:
        if i not in dict:
            dict[i]=1
        else:
            dict[i]+=1
    max=0
    imp_word=[]
    done=[]
    for i in text:
        if len(i)<5:
            dict[i]=0
    sorted(dict.items(), key=lambda x: x[1], reverse=True)
    #print(dict)
    p=0
    l=0
    title_word=word_tokenize(title)
    for i in title_word:
        l+=1
        imp_word.append(i)
        
    for key in dict:
        if p==10:
            break
        else:
            imp_word.append(key)
            p+=1
            
    
    #print(imp_word)
    synonyms = [] 
    antonyms = [] 
    for i in range (1,10+l):
        for syn in wordnet.synsets(imp_word[i]): 
            for l in syn.lemmas(): 
                synonyms.append(l.name()) 
                if l.antonyms(): 
                    antonyms.append(l.antonyms()[0].name()) 
      
    len_of_synonyms=len(synonyms)
    len_of_antonyms=len(antonyms)
    for i in range(0,len_of_synonyms):
        synonyms[i]=synonyms[i].upper()
        
    for i in range(0,len_of_antonyms):
        antonyms[i]=antonyms[i].upper()
    #print(synonyms)
    #print(antonyms)
    
    count=0

    for i in synonyms:
        for key in dict:
            if key==i and i not in imp_word:
                count+=1
                #print(key,i)
    #print(count)
    if count >10:
        status="PASS"
    else:
        status="FAIL"
    return status   # the number of synonyms used in the essay(proper relevant words used)


