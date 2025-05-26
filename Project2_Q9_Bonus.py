################################################# QUESTION 9 ###########################################################
# Note: 1. Make sure to have the following files in the current directory before running the code:
#           (1) act2movie_dict.pcy
#           (2) movie_rating_dict.pcy
#       2. Make sure to have the following libraries installed for your version of python before running the code:
#           (1) pickle
#           (2) time
#           (3) igraph
#           (4) statistics
#-----------------------------------------------------------------------------------------------------------------------

import pickle
import time
import igraph
import statistics

start = time.clock()

print '(Step 1 of 5) Load act2movie_dict from pickle file.'
act2movie_dict_pickle = open('act2movie_dict.pcy', 'r')
act2movie_dict = pickle.load(act2movie_dict_pickle)


print '(Step 2 of 5) Load movie_rating_dict from pickle file.'
movie_rating_dict_pickle = open('movie_rating_dict.pcy', 'r')
movie_rating_dict = pickle.load(movie_rating_dict_pickle)


print '(Step 3 of 5) Create edgelist of actors/actress IDs and movie IDs and assign a score to each actor/actress.'
types_arr = []
edges_arr = []
act_score_dict = {}
vertex_id = 0
vertex2act_name = {}
movie_name2vertex = {}

for k, v in act2movie_dict.items():
    act_vertex_id = vertex_id
    vertex2act_name[act_vertex_id] = k
    types_arr.append(0)
    vertex_id = vertex_id + 1
    act_movie_rating_arr = []
    act_score = 0.0

    for movie in v:
        # look for movie's rating
        if movie_rating_dict.has_key(movie):
            act_movie_rating_arr.append(movie_rating_dict[movie])
        # create edge
        movie_vertex_id = vertex_id
        movie_name2vertex[movie] = movie_vertex_id
        types_arr.append(1)
        edge = (act_vertex_id, movie_vertex_id)
        edges_arr.append(edge)
        vertex_id = vertex_id + 1

    if len(act_movie_rating_arr) > 5:
        sorted_ratings = sorted(act_movie_rating_arr, reverse=True)
        act_score = 0.9*statistics.mean(sorted_ratings[0:5])
    elif len(act_movie_rating_arr) != 0:
        act_score = statistics.mean(act_movie_rating_arr)
    else:
        act_score = 5.0
    act_score_dict[k] = act_score


print '(Step 4 of 5) Create bipartite graph.'
g = igraph.Graph.Bipartite(types=types_arr, edges=edges_arr, directed=False)
num_vertices = g.vcount()
num_edges = g.ecount()
print 'Graph g has', num_vertices, 'vertices and', num_edges, 'edges.'


# Predict ratings of new movies
print '(Step 5 of 5) Predict rating of new movies.\n'
new_movies = ['Batman v Superman: Dawn of Justice (2016)', 'Mission: Impossible - Rogue Nation (2015)', 'Minions (2015)']
for m in new_movies:
    movie_vertex_id = movie_name2vertex[m]
    act_vertex_ids = g.neighbors(movie_vertex_id)
    act_names = [vertex2act_name[v] for v in act_vertex_ids]
    act_scores = [act_score_dict[n] for n in act_names if act_score_dict[n] != 0]
    predicted_rating = statistics.mean(act_scores)
    print m, ':', predicted_rating


end = time.clock()
print '\nProcess done. Program run-time in your CPU: ' + str(int(end - start)) + ' seconds.'

################################################ END OF QUESTION 9 #####################################################
