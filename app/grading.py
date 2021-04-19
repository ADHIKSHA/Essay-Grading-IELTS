#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
def Main_fun(text):

    train = pd.read_csv("testtraining.csv")


    # In[2]:


    #train


    # In[3]:


    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import train_test_split
    train1 = train.copy()
    feature_df = train1[["NoWrd","NoSent","ADJ","ADP","ADV","CONJ","DET","NOUN","NUM","PRT","PRON", "VERB",".","X"]]
    x = np.asarray(feature_df)
    y = np.asarray(train["NScr"].astype('int'))
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 5)


    # In[4]:


    def train_model(x_train, y_train, x_test, y_test, classifier, **kwargs):
        
        
        # instantiate model
        model = classifier(**kwargs)
        
        # train model
        model.fit(x_train,y_train)
        y_pred = model.predict(x_test)
        #from sklearn.metrics import confusion_matrix
        #print("Confusion matrix")
        #print(confusion_matrix(y_test,y_pred))

        
        ### check accuracy and print out the results
        #fit_accuracy = model.score(x_train, y_train)
        #test_accuracy = model.score(x_test, y_test)
        
        #print(f"Train accuracy: {fit_accuracy:0.2%}")
        #print(f"Test accuracy: {test_accuracy:0.2%}")
        
        return model


    # In[5]:


    model = train_model(x_train, y_train, x_test, y_test, GaussianNB)
    #from sklearn.svm import SVC
    #model = train_model(x_train, y_train, x_test, y_test, SVC, C=0.05, kernel='linear')


    # In[6]:


    gnb = GaussianNB()


    # In[7]:


    gnb.partial_fit(x, y, np.unique(y))


    # In[8]:
    essay=text
# In[9]:


    import re
    NoWrd = len(re.findall(r'\w+', essay))
    NoWrd


# In[10]:


    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.probability import FreqDist

    UNIV_TAGS = ['ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRT', 'PRON', 'VERB', '.', 'X']
    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')


# In[11]:


    text = word_tokenize(essay)
    num_tokens = len(text)
#print("Number of Words",num_tokens)
    tagged_words = nltk.pos_tag(text, tagset='universal')
    tags_only = [tag for _, tag in tagged_words]
    fd = FreqDist(tags_only)
    tags_dict = {}
    for pos in UNIV_TAGS:
        tags_dict[pos] = float(fd[pos])


# In[12]:


    x=tags_dict['X']
    dot=tags_dict['.']
    verb=tags_dict['VERB']
    pron=tags_dict['PRON']
    prt=tags_dict['PRT']
    num=tags_dict['NUM']
    noun=tags_dict['NOUN']
    det=tags_dict['DET']
    conj=tags_dict['CONJ']
    adv =tags_dict['ADV']
    adp =tags_dict['ADP']
    adj =tags_dict['ADJ']


# In[13]:


    NoSent=re.split(r'[.!?]+', essay)
    NoSent=len(NoSent)

# In[25]:
 

    xyz=[[NoWrd , NoSent, adj, adp, adv, conj,det, noun, num, prt, pron, verb, dot, x]]

#arr= array.array('i',xyz)
    arr=[['NoWrd','NoSent','adj','adv','conj','det','noun','num','prt','pron','verb','dot','x'],[NoWrd , NoSent, adj, adp, adv, conj,det, noun, num, prt, pron, verb, dot, x]]
#arr.reshape(-1,1)
    #print(gnb.predict(xyz))

    x=gnb.predict(xyz)
    return x[0]

    #print(gnb.predict([[499,30,30,65,43,16,47,134,3,16,59,102,65,0]]))
    #print(final_result[0])



