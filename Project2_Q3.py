################################################# QUESTION 3 ###########################################################
# Note: 1. Make sure to have the following files in the current directory before running the code:
#           (1) act_edgelist.txt
#           (2) movie2act_dict.pcy
#           (3) hashtabletable_act_name2index.pcy
#       2. Make sure to have the following libraries installed for your version of python before running the code:
#           (1) time
#           (2) igraph
#           (3) pickle
#           (4) OrderedDict
#       3. At the end of its execution, the program will generate the following files:
#           (1) sorted_pagerank_scores.txt
#           (2) sorted_pagerank_scores.pcy
#           (3) movie2act_pr_dict.txt
#           (4) movie2act_pr_dict.pcy
#-----------------------------------------------------------------------------------------------------------------------

import time
import igraph
import pickle
from collections import OrderedDict

start = time.clock()

print '(Step 1 of 10) Construct actors/actresses graph from act_edgelist.txt. (This may take up to 5 minutes.)'
g = igraph.read(filename='act_edgelist.txt', format='ncol', directed=True)
print 'Finished constructing graph.'
#break1 = time.clock()
#print 'Graph construction used CPU time ' + str(int(break1 - start)) + ' seconds.'
print 'Calculating number of edges and vertices.'
num_v = g.vcount()
num_e = g.ecount()
print num_v, ',', num_e

print '(Step 2 of 10) Calculate PageRank for each actor/actress. (This may take up to 2 hours.)'
pr = g.pagerank(vertices=g.vs, directed=True, weights=g.es['weight'])


print '(Step 3 of 10) Store PageRank score to a hash table.'
pr_table = {}
for i in range(len(pr)):
    pr_table[(g.vs['name'])[i]] = pr[i]
    #print 'Hashing PageRank..........', (float(i)/len(pr))*100, '%'


print '(Step 4 of 10) Sort these PageRank scores.'
sorted_pr_table = OrderedDict(sorted(pr_table.items(), key=lambda x: x[1]))
pr_table.clear()
del g
del pr[:]


print '(Step 5 of 10) Save sorted PageRank scores in a text file sorted_pagerank_scores.txt.'
pagerank_file = open('sorted_pagerank_scores.txt', 'w')
for k, v in sorted_pr_table.items():
    entry = [k, v]
    text = '\t'.join(str(x) for x in entry) + '\n'
    pagerank_file.write(text)
pagerank_file.close()


print '(Step 6 of 10) Save sorted PageRank scores in a pickle file sorted_pagerank_scores.pcy.'
sorted_pagerank_scores_pickle = open('sorted_pagerank_scores.pcy', 'w')
pickle.dump(sorted_pr_table, sorted_pagerank_scores_pickle)


print '(Step 7 of 10) Load pickle files movie2act_dict.pcy and hashtabletable_act_name2index.pcy.'
movie2act_dict_pickle = open('movie2act_dict.pcy', 'r')
hashtable_act_name2index_pickle = open('hashtable_act_name2index.pcy', 'r')
movie2act_dict = pickle.load(movie2act_dict_pickle)
hashtable_act_name2index = pickle.load(hashtable_act_name2index_pickle)


print '(Step 8 of 10) Find corresponding PageRank for each actor/actress in movie2act_dict.'
movie2act_pr_file = open('movie2act_pr_dict.txt', 'w')
for k, v in movie2act_dict.items():
    entry = [k]
    for act_name in v:
        act_index = hashtable_act_name2index.get(act_name)
        act_pr = sorted_pr_table.get(str(act_index))
        entry.append(act_pr)
    text = "\t".join(str(x) for x in entry) + '\n'
    movie2act_pr_file.write(text)
movie2act_pr_file.close()


print '(Step 9 of 10) Save movie2act_pr_dict in a pickle file.'
movie2act_pr_pickle = open('movie2act_pr_dict.pcy', 'w')
pickle.dump(movie2act_dict, movie2act_pr_pickle)


print '(Step 10 of 10) Clean up memory.'
sorted_pr_table.clear()
hashtable_act_name2index.clear()
movie2act_dict.clear()


end = time.clock()
print '\nProcess done. Program run-time in your CPU: ' + str(int(end - start)) + ' seconds.'

################################################ END OF QUESTION 3 #####################################################
