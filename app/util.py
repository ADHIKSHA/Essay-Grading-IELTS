import numpy as np
import pandas as pd
import re
import string

# Useful functions go here

def move_column_last(df, column_name):
	column = df[column_name]
	df = df.drop(column_name, axis=1)
	df[column_name] = column
	return df

# returns a column to place data
def append_zeros_column(df, title):
	df[title] = pd.Series([0.0] * df.shape[0], index=df.index)
	return df

# non standardized column must be already included in dfs
def append_standardized_column(train_df, valid_df, non_std_col_name):
	std_col_name = "std_" + non_std_col_name
	train_df = append_zeros_column(train_df, std_col_name)
	valid_df = append_zeros_column(valid_df, std_col_name)

	std_data = create_standardization_data(train_df, non_std_col_name)

	dfs = [train_df, valid_df]
	for df in dfs:
		for i in xrange(df.shape[0]):
			essay_set = df.get_value(i, 'essay_set')
			non_std_val = df.get_value(i, non_std_col_name)
			df = df.set_value(i, std_col_name, (non_std_val - std_data[essay_set - 1][0]) / std_data[essay_set - 1][1])

	return train_df, valid_df

# Calculates the mean and standard deviation for column_name in train_df
# Can be generalized to different columns
def create_standardization_data(train_df, column_name):
    #getting the number of datasets
    max_essay_set = max(train_df['essay_set'])
    #list of the standardized values
    standardization_data = []
    for i in range(1, max_essay_set+1):
        mean = np.mean((train_df[train_df['essay_set'] == i])[column_name])
        std = np.std((train_df[train_df['essay_set'] == i])[column_name])
        standardization_data.append([mean, std])
    return standardization_data

def get_training_data(filename):
	# Read in training data
	# Note that for essay set 2, score becomes average of 2 domain scores
	train_cols = ['essay_id', 'essay_set', 'essay', 'domain1_score', 'domain2_score']
	train_df = pd.read_csv(filename, delimiter='\t', usecols=train_cols, encoding='ISO-8859-1')
	for i in xrange(train_df.shape[0]):
	    if not np.isnan(train_df.get_value(i, 'domain2_score')):
	        assert train_df.get_value(i, 'essay_set') == 2
	        new_val = train_df.get_value(i, 'domain1_score') + train_df.get_value(i, 'domain2_score')
	        train_df.set_value(i, 'domain1_score', new_val) 
	train_df = train_df.drop('domain2_score', axis=1)
	train_df = train_df.rename(columns={'domain1_score': 'score'})

	return train_df

def get_validation_data(filename):
	# Read in validation data
	valid_cols = ['essay_id', 'essay_set', 'essay', 'domain1_predictionid', 'domain2_predictionid']
	valid_df = pd.read_csv(filename, delimiter='\t', usecols=valid_cols, encoding='ISO-8859-1')
	valid_df['score'] = pd.Series([0] * valid_df.shape[0], index=valid_df.index)

	# scores are stored in separate data set, we'll put them in same one
	valid_scores = pd.read_csv('../data/valid_sample_submission_5_column.csv', delimiter=',')

	# put each score in our data set, and make sure to handle essay set 2
	for i in xrange(valid_df.shape[0]):
	    dom1_predid = valid_df.get_value(i, 'domain1_predictionid')
	    row = valid_scores[valid_scores['prediction_id'] == dom1_predid]
	    score = row.get_value(row.index[0], 'predicted_score')
	    
	    dom2_predid = valid_df.get_value(i, 'domain2_predictionid')
	    if not np.isnan(dom2_predid):
	        assert valid_df.get_value(i, 'essay_set') == 2
	        rowB = valid_scores[valid_scores['prediction_id'] == dom2_predid]
	        scoreB = rowB.get_value(rowB.index[0], 'predicted_score')
	        score += scoreB
	        
	    valid_df.set_value(i, 'score', score)
	        
	valid_df = valid_df.drop(['domain1_predictionid', 'domain2_predictionid'], axis=1)

	# assert no missing data
	assert not valid_df.isnull().any().any()

	return valid_df

# returned a copy of old_df, with essays cleaned for count vectorizer
# cleaning returns essay with only lowercase words separated by space
def vectorizer_clean(old_df):
    new_df = old_df.copy()
    for i in xrange(new_df.shape[0]):
        new_df.set_value(i, 'essay', " ".join(re.sub('[^a-zA-Z\d\s]', '', new_df['essay'].iloc[i]).lower().split())) 
    return new_df

# return essay set as one string in a list
# cleaning returns essay with only lowercase words separated by space
def perplexity_clean(df):
    essays_string = ""
    for i in xrange(df.shape[0]):
    	essay = df.get_value(i, 'essay') 
    	essays_string += (" ".join(re.sub('[^a-zA-Z\d\s]', '', essay).lower().split()))
    return [essays_string]

# clean vectorizer for spelling feature
def vectorizer_clean_spelling(old_df):
    new_df = old_df.copy()
    for i in xrange(new_df.shape[0]):
    	regex = re.compile('[%s]' % re.escape(string.punctuation))
    	out = regex.sub(' ', new_df['essay'].iloc[i])
    	new_df.set_value(i, 'essay', out)

        #new_df.set_value(i, 'essay', " ".join(re.sub('[^a-zA-Z\d\s]', '', new_df['essay'].iloc[i]).lower().split())) 
    return new_df