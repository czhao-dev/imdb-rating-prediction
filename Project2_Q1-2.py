########################################### QUESTION 1 AND 2 ###########################################################
# Note: 1. Make sure to have the following files in the current directory before running the code:
#           (1) actor_movies.txt
#           (2) actress_movies.txt
#       2. Make sure to have the following libraries installed for your version of python before running the code:
#           (1) itertools
#           (2) re
#           (3) time
#           (4) pickle
#       3. At the end of its execution, the program will generate the following files:
#           (1) act2movie_dict.pcy
#           (2) movie2act_dict.pcy
#           (3) movie2act_dict.txt
#           (4) hashtable_act_name2index.txt
#           (5) hashtable_act_name2index.pcy
#           (6) hashtable_movie_name2index.txt
#           (7) hashtable_movie_name2index.pcy
#           (8) act_edgelist.txt
#-----------------------------------------------------------------------------------------------------------------------


import itertools
import re
import time
import pickle

start = time.clock()
# Read actor_movies.txt and build act<->movie dictionaries while reading the file
actor_movies_file = open("actor_movies.txt", "r")
act2movie_dict = {}
movie2act_dict = {}
line_num1 = 1
print '(Step 1 of 8) Read act_movies.txt and build act_name<->movie_name dictionaries. (This may take up to 3 minutes.)'
for line in actor_movies_file:
    noname_movies = {'(2006)', '(1967)', '(1971)', '(1993)', '(1995)', '(1996)', '(2001)', '(2002)', '(2005)', '(2006)', '(2009)', '(2010)', '(2012)', '(2013)', '(2014)'}
    line_split = [s for s in line.split("\t") if len(s) > 2]
    line_split = [re.sub('[!@#$&.*\']', '', s) for s in line_split]
    if len(line_split) > 5:
        actor_name = line_split[0]

        movies = []
        for i in xrange(1, len(line_split)):
            line_split[i] = re.sub(r'\([^0-9)]*\)', '', line_split[i])
            line_split[i] = re.sub('{{.*?}}', '', line_split[i])

            while line_split[i].startswith(' '):
                line_split[i] = (line_split[i])[1:]

            while line_split[i].endswith(' ') or line_split[i].endswith('\n'):
                line_split[i] = (line_split[i])[:-1]

            if line_split[i] not in noname_movies:
                movies.append(line_split[i])

                if line_split[i] not in movie2act_dict:
                    movie2act_dict[line_split[i]] = [actor_name]
                else:
                    movie2act_dict[line_split[i]].append(actor_name)

        act2movie_dict[actor_name] = movies

    #print "Reading actor_movies.txt...........", (float(line_num1) / 2167654) * 100, '%'
    line_num1 = line_num1 + 1
actor_movies_file.close()


print '(Step 2 of 8) Read actress_movies.txt and build act_name<->movie_name dictionaries. (This may take up to 2 minutes.)'
# Read actress_movies.txt and build act<->movie dictionaries while reading the file
actress_movies_file = open("actress_movies.txt", "r")
line_num2 = 1
for line in actress_movies_file:
    noname_movies = {'(2006)', '(1967)', '(1971)', '(1993)', '(1995)', '(1996)', '(2001)', '(2002)', '(2005)', '(2006)', '(2009)', '(2010)', '(2012)', '(2013)', '(2014)'}
    line_split = [s for s in line.split("\t") if len(s) > 2]
    line_split = [re.sub('[!@#$&.*\']', '', s) for s in line_split]
    if len(line_split) > 5:
        actress_name = line_split[0]
        #line_split = [re.sub('[^A-Za-z0-9]+', '', s) for s in line_split]

        movies = []
        for i in xrange(1, len(line_split)):
            line_split[i] = re.sub(r'\([^0-9)]*\)', '', line_split[i])
            line_split[i] = re.sub('{{.*?}}', '', line_split[i])

            while line_split[i].startswith(' '):
                line_split[i] = (line_split[i])[1:]

            while line_split[i].endswith(' ') or line_split[i].endswith('\n'):
                line_split[i] = (line_split[i])[:-1]

            if line_split[i] not in noname_movies:
                movies.append(line_split[i])

                if line_split[i] not in movie2act_dict:
                    movie2act_dict[line_split[i]] = [actress_name]
                else:
                    movie2act_dict[line_split[i]].append(actress_name)

        act2movie_dict[actress_name] = movies

    #print "Reading actress_movies.txt...........", (float(line_num2) / 1182814) * 100, '%'
    line_num2 = line_num2 + 1
actress_movies_file.close()

# Sort all the keys in both dictionaries and build hash tables mapping the indices of the keys
print '(Step 3 of 8) Sort act_names->movie_names and movie_names->act_names dictionaries.'
sorted_act_names = sorted(act2movie_dict.keys())
sorted_movie_names = sorted(movie2act_dict.keys())


print '(Step 4 of 8) Save both dictionaries as pickle files.'
act2movie_dict_pickle = open('act2movie_dict.pcy', 'w')
movie2act_dict_pickle = open('movie2act_dict.pcy', 'w')
pickle.dump(act2movie_dict, act2movie_dict_pickle)
pickle.dump(movie2act_dict, movie2act_dict_pickle)


print '(Step 5 of 8) Create act_name->index hash table and write to hashtable_act_name2index.txt file.'
hashtable_act_name2index = {}
hashtable_movie_name2index = {}
dict1_file = open('hashtable_act_name2index.txt', 'w')
dict2_file = open('hashtable_movie_name2index.txt', 'w')
dict3_file = open('movie2act_dict.txt', 'w')
for i in range(len(sorted_act_names)):
    hashtable_act_name2index[sorted_act_names[i]] = i
    entry = [i, sorted_act_names[i]]
    text = "\t".join(str(x) for x in entry) + '\n'
    dict1_file.write(text)
    #print "Writing file hashtable_act_name2index.txt...........", (float(i)/len(sorted_act_names))*100, '%'
dict1_file.close()


print '(Step 6 of 8) Create movie_name->index hash table and write to hashtable_movie_name2index.txt and movie2act_dict.txt files.'
for i in range(len(sorted_movie_names)):
    hashtable_movie_name2index[sorted_movie_names[i]] = i
    entry1 = [i, sorted_movie_names[i]]
    text1 = "\t".join(str(x) for x in entry1) + '\n'
    dict2_file.write(text1)

    entry2 = [sorted_movie_names[i]] + movie2act_dict[sorted_movie_names[i]]
    text2 = "\t".join(str(x) for x in entry2) + '\n'
    dict3_file.write(text2)
    #print "Write files hashtable_movie_name2index.txt and movie2act_dict.txt...........", (float(i) / len(sorted_movie_names))*100, '%'
dict2_file.close()
dict3_file.close()


print '(Step 7 of 8) Save both hash tables as pickle files.'
hashtable_act_name2index_pickle = open('hashtable_act_name2index.pcy', 'w')
hashtable_movie_name2index_pickle = open('hashtable_movie_name2index.pcy', 'w')
pickle.dump(hashtable_act_name2index, hashtable_act_name2index_pickle)
pickle.dump(hashtable_movie_name2index, hashtable_movie_name2index_pickle)


print '(Step 8 of 8) Process actors/actresses edge list and save it as act_edgelist.txt file. (This may take up to 10 minutes.)'
output_file = open('act_edgelist.txt', 'w')
act_combs_dict = {}

for i in xrange(0, len(sorted_movie_names)):
    movie_name = sorted_movie_names[i]
    act_list = movie2act_dict.get(movie_name)
    act_num = len(act_list)
    if act_num > 1:
        for pair in itertools.combinations(act_list, 2):
            act1_name = pair[0]
            act2_name = pair[1]
            act1_index = hashtable_act_name2index.get(act1_name)
            act2_index = hashtable_act_name2index.get(act2_name)
            if (act_combs_dict.get(act1_index) is None) or (act2_index not in act_combs_dict.get(act1_index)):
                act1_movies = act2movie_dict.get(act1_name)
                act2_movies = act2movie_dict.get(act2_name)
                if (act1_movies is not None) and (act2_movies is not None):
                    act1_movies_num = len(act1_movies)
                    act2_movies_num = len(act2_movies)
                    overlap_movies = len(set(act1_movies) & set(act2_movies))

                    entry1 = [act1_index, act2_index, float(overlap_movies) / act1_movies_num]
                    entry2 = [act2_index, act1_index, float(overlap_movies) / act2_movies_num]
                    output_file.write("\t".join(str(x) for x in entry1) + '\n')
                    output_file.write("\t".join(str(x) for x in entry2) + '\n')
                if act_combs_dict.get(act1_index) is None:
                    act_combs_dict[act1_index] = [act2_index]
                else:
                    act_combs_dict[act1_index].append(act2_index)

                if act_combs_dict.get(act2_index) is None:
                    act_combs_dict[act2_index] = [act1_index]
                else:
                    act_combs_dict[act2_index].append(act1_index)
    #print "Processing actors/actresses edge list..........", (float(i) / len(sorted_movie_names)) * 100, '%'
output_file.close()
act_combs_dict.clear()

end = time.clock()
print 'Process done. Program run-time in your CPU: ' + str(int(end - start)) + ' seconds.'

################################################ END OF QUESTION 1 AND 2 ###############################################
