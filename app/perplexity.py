import math
import app.util
import nltk
from nltk import trigrams
from nltk import bigrams
from nltk import everygrams
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
s=nltk.download('punkt')

# class that implements functionality for calculating perplexity of essay with Laplace smoothing
class Perplexity:
        
        def __init__(self):
                self.num_words = None
                self.counts = None
                self.vectorizer = None

        def create_counts(self, compressed_essays):
                self.vectorizer = CountVectorizer().fit(compressed_essays)
                self.counts = self.vectorizer.transform(compressed_essays).toarray()[0]

                # length added for LaPlace smoothing
                self.num_words = float(sum(self.counts) + len(self.counts))

        def fill_perplexity_columns(self, train_df, valid_df):
               # print ("Creating ngram counts...")
                self.create_counts(util.perplexity_clean(train_df))

                train_clean = util.vectorizer_clean(train_df)
                valid_clean = util.vectorizer_clean(valid_df)

                dfs = [train_clean, valid_clean]

                for j, df in enumerate(dfs):
                        for i in xrange(df.shape[0]):
                                if i % 100 == 0:
                                        essay_set = None
                                        if j == 0:
                                                essay_set = "Train"
                                        else:
                                                essay_set = "Validation"
                                        
                                        print (essay_set , " essay " , str(i) , " of " , str(df.shape[0]))
                                essay = df.get_value(i, 'essay')
                                perp = self.perplexity(essay)

                                df = df.set_value(i, 'perplexity', perp)

                train_df['perplexity'] = train_clean['perplexity']
                valid_df['perplexity'] = valid_clean['perplexity']

                return util.append_standardized_column(train_df, valid_df, 'perplexity')

        # After having already fit model on a set of training essays, calculates the
        # perplexity of a student's essay based from the model, and returns this
        # perplexity to be used as a feature
        def perplexity(self, test_essay):
                log_prob = 0.0
                word_list = test_essay.split()
                if len(word_list)==0:
                        return 0
                for word in word_list:
                        if word in self.vectorizer.vocabulary_:
                                log_prob += math.log( (self.counts[self.vectorizer.vocabulary_[word]] + 1.0) / self.num_words)
                        else:
                                log_prob += math.log (1.0 / self.num_words)

                return math.pow(2.0, -log_prob / len(word_list))

def RunThis(text):
        result={}
        sentences= nltk.sent_tokenize(text)
        train_essays=[]
        train_es=""
        if len(sentences)<5:
                result['Less than 5 sentences']=[0,'Fail']
                return result

        for i in range(0,5):
                train_es+=sentences[i]
        train_essays.append(train_es)
        #print(train_essays)
        f=5
        l=len(sentences)
        #print('total no of sentences=',l)
        count=0
        value=int(l/5)+1
        test_essays=[]
        for index in range(0,value):
                test_essays.append("")

        
        while f<l:
                
                if l-f >=5:
                        for j in range(f,f+5):
                                test_essays[count]+= sentences[j]
                        #print('Essay number : ',count,' is :\n',test_essays[count])
                        f+=5
                        count+=1
                else:
                        for j in range(f,l-f):
                                test_essays[count]+=sentences[j]
                        #print('Essay number : ',count,' is :\n',test_essays[count])
                        count+=1
                        f=l


        perp = Perplexity()

        counts = perp.create_counts(train_essays)

        #print (perp.vectorizer.vocabulary_)
        
        list_of_dev=[]
        for i in range (0,count):
                deviation_rate=perp.perplexity(test_essays[i])
                #print ('The deviation of paragraph number : ',i,' is :',deviation_rate)
                if len(test_essays[i]) !=0:
                        result[test_essays[i]]=[]
                        result[test_essays[i]].append(deviation_rate)
                        list_of_dev.append(deviation_rate)
                #print (perp.vectorizer.vocabulary_)
                #print (perp.counts)
                #print (perp.num_words)
                #print (perp.counts[perp.vectorizer.vocabulary_['hi']])
        if len(list_of_dev)==0:
                result['Less than 5 sentences']=[0,'Fail']
                return result
        average_of_dev= sum(list_of_dev)/len(list_of_dev)
        high='High Deviation'
        low='Low Deviation'
        for key,val in result.items():
                if (val[0]-average_of_dev) >= 0.5:
                        val[0]=val[0]-average_of_dev
                        result[key].append(high)
                else:
                        val[0]=val[0]-average_of_dev
                        result[key].append(low)
        #print(result)
        
        return result                                                                 #return a dictionary



def get_score(text):                                                    #returns the score
        dict=RunThis(text)
        count=0
        flag=0 
                                                                # 0 means PASS and 1 means FAIL
        for key,value in dict.items():
                if value[1]=='Fail':
                        return flag

                if value[1]=='High Deviation':
                        count+=1

        if count>1:
                flag=1

        return flag