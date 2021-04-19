from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import io
import urllib, base64

def generate_wordcloud(text):
	df = text
	comment_words = ' '
	stopwords = set(STOPWORDS) 

	# iterate through the csv file 
	for val in df: 
		
		# typecaste each val to string 
		val = str(val) 

		# split the value 
		tokens = val.split() 
		
		# Converts each token into lowercase 
		for i in range(len(tokens)): 
			tokens[i] = tokens[i].lower() 
			
		for words in tokens: 
			comment_words = comment_words + words + ' '

	#print(comment_words)
	wc = WordCloud(width = 800, height = 800, 
					background_color ='white', 
					stopwords = stopwords, 
					min_font_size = 10).generate(text.lower())
	plt.figure(figsize=(32,18))
	plt.imshow(wc, interpolation="bilinear", aspect='auto')
	fig = plt.gcf()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = 'data:image/png;base64,' + urllib.parse.quote(string)
	return uri