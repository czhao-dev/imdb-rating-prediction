################################################# QUESTION 8 ###########################################################
# Note: 1. Make sure to have the following files in the current directory before running the code:
#           (1) sorted_pagerank_scores.pcy
#           (2) hashtable_act_name2index.pcy
#           (3) movie2act_dict.txt
#           (4) director_100_last_first.txt
#           (5) director_movies.txt
#           (6) movie_rating.txt
#       2. Make sure to have the following libraries installed for your version of python before running the code:
#           (1) pickle
#           (2) time
#           (3) sklearn
#           (4) re
#           (5) numpy
#       3. At the end of its execution, the program will generate the following files:
#           (1) movie2act_pr_dict.pcy
#           (2) movie_parameters_pickle.pcy
#           (3) movie_ratings_pickle.pcy
#           (4) movie_rating_dict.pcy
#           (5) test_movies_pickle.pcy
#-----------------------------------------------------------------------------------------------------------------------

import pickle
import time
from sklearn import linear_model
import re
import numpy as np

start = time.clock()
print '(Step 1 of 14) Read sorted_pagerank_scores from pickle.'
pagerank_pickle = open('sorted_pagerank_scores.pcy', 'r')
sorted_pr_table = pickle.load(pagerank_pickle)
pagerank_pickle.close()


print '(Step 2 of 14) Read hashtable_act_name2index from pickle.'
hashtable_act_name2index_pickle = open('hashtable_act_name2index.pcy', 'r')
hashtable_act_names2index = pickle.load(hashtable_act_name2index_pickle)
hashtable_act_name2index_pickle.close()


print '(Step 3 of 14) Read movie2act_dict.txt.'
movie2act_dict_file = open('movie2act_dict.txt', 'r')
movie2act_pr_dict_pickle = open('movie2act_pr_dict.pcy', 'w')
movie2act_pr_dict = {}
line_num = 1
for line in movie2act_dict_file:
    line_split = [s for s in line.split("\t") if s != '']
    line_split[len(line_split)-1] = (line_split[len(line_split)-1])[:-1]
    movie_name = line_split[0]
    act_pr_scores = []
    for i in range(1, len(line_split)):
        act_name = line_split[i]
        act_index = hashtable_act_names2index.get(act_name)
        act_pr = sorted_pr_table.get(act_index)
        act_pr_scores.append(act_pr)
    act_pr_scores = sorted(act_pr_scores, reverse=True)
    if len(act_pr_scores) >= 5:
        movie2act_pr_dict[movie_name] = act_pr_scores[0:5]


print '(Step 4 of 14) Save movie2act_pr_dict as pickle.'
pickle.dump(movie2act_pr_dict, movie2act_pr_dict_pickle)
movie2act_dict_file.close()
movie2act_pr_dict_pickle.close()


print '(Step 5 of 14) Read in top 100 directors.'
director100_file = open('director_100_last_first.txt', 'r')
director100_set = set()
for line in director100_file:
    director100_set.update([line[:-1]])


print '(Step 6 of 14) Read in director_movies.txt.'
director100_movies_set = set()
director_movies_file = open('director_movies.txt', 'r')
for line in director_movies_file:
    noname_movies = {'(2006)', '(1967)', '(1971)', '(1993)', '(1995)', '(1996)', '(2001)', '(2002)', '(2005)', '(2006)', '(2009)', '(2010)', '(2012)', '(2013)', '(2014)'}
    line_split = [s for s in line.split('\t') if s != '']
    if line_split[0] in director100_set:
        for i in xrange(1, len(line_split)):
            line_split[i] = re.sub(r'\([^0-9)]*\)', '', line_split[i])
            line_split[i] = re.sub('{{.*?}}', '', line_split[i])

            while line_split[i].startswith(' '):
                line_split[i] = (line_split[i])[1:]

            while line_split[i].endswith(' ') or line_split[i].endswith('\n'):
                line_split[i] = (line_split[i])[:-1]

            if line_split[i] not in noname_movies:
                director100_movies_set.update([line_split[i]])
director_movies_file.close()


print '(Step 7 of 14) Read movie_rating.txt.'
movie_director100_dict = {}     # contains 1/0 booleans values (1 if the movie's director in top 100 list, 0 otherwise)
movie_rating_dict = {}          # contains movie names and their ratings
rating_file = open('movie_rating.txt', 'r')
for line in rating_file:
    line_split = [s for s in line.split('\t\t') if s != '']
    if line_split[0] in director100_movies_set:
        movie_director100_dict[line_split[0]] = 1
    else:
        movie_director100_dict[line_split[0]] = 0
    movie_rating_dict[line_split[0]] = float((line_split[1])[:-1])
rating_file.close()


print '(Step 8 of 14) Create numpy arrays of movie parameters and ratings.'
movie_parameters_pickle = open('movie_parameters_pickle.pcy', 'w')
movie_ratings_pickle = open('movie_ratings_pickle.pcy', 'w')
movie_parameters = []
movie_ratings = []
for k, v in movie2act_pr_dict.items():
    if movie_director100_dict.has_key(k):
        arr = v + [movie_director100_dict[k]]
        movie_parameters.append(arr)
        movie_ratings.append(movie_rating_dict.get(k))


print '(Step 9 of 14) Save movie parameters and ratings to pickle.'
# convert python lists to numpy arrays
movie_parameters_np = np.asarray(movie_parameters)
pickle.dump(movie_parameters_np, movie_parameters_pickle)
movie_ratings_np = np.asarray(movie_ratings)
movie_ratings_np = np.transpose(movie_ratings_np)
pickle.dump(movie_ratings_np, movie_ratings_pickle)
movie_rating_dict_pickle = open('movie_rating_dict.pcy', 'w')
pickle.dump(movie_rating_dict, movie_rating_dict_pickle)


print '(Step 10 of 14) Collect test movies data.'
test_movies = ['Batman v Superman: Dawn of Justice (2016)', 'Mission: Impossible - Rogue Nation (2015)', 'Minions (2015)']
test_movies_directors = ['Snyder, Zack', 'McQuarrie, Christopher', 'Balda, Kyle']
test_movies_data = []
test_movies_pickle = open('test_movies_pickle.pcy', 'w')
for i in range(len(test_movies)):
    arr = movie2act_pr_dict[test_movies[i]]
    if test_movies_directors[i] not in director100_set:
        arr = arr + [0]
    else:
        arr = arr + [1]
    test_movies_data.append(arr)
test_movies_data_np = np.asarray(test_movies_data)

print '(Step 11 of 14) Save test movies data to pickle.'
pickle.dump(test_movies_data_np, test_movies_pickle)


print '(Step 12 of 14) Build nonlinear regression model.'
reg = linear_model.LinearRegression()
# Traing values X is movie_parameters_np
# Target values y is movie_ratings_np
reg.fit(movie_parameters_np, movie_ratings_np)


print '(Step 13 of 14) Predict ratings.\n'
predict_scores = reg.predict(test_movies_data_np)
for i in range(len(test_movies)):
    print test_movies[i], ':', predict_scores[i]


print '(Step 14 of 14) Calculate goodness of fit.\n'
r2 = reg.score(movie_parameters_np, movie_ratings_np)
print 'R-squared value =', r2


end = time.clock()
print '\nProcess done. Program run-time in your CPU: ' + str(int(end - start)) + ' seconds.'

################################################ END OF QUESTION 8 #####################################################
