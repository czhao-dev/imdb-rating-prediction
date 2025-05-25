import itertools
import re

# Read actor_movies.txt and build act<->movie dictionaries while reading the file
actor_movies_file = open("actor_movies.txt", "r")
act2movie_dict = {}
movie2act_dict = {}
for line in actor_movies_file:
    line_split = line.split("\t")
    line_split = [s for s in line_split if s !='']
    actor_name = line_split[0]

    if (len(line_split) >= 6):
        for i in range(1, len(line_split)):
            while line_split[i].endswith(' ') or line_split[i].endswith('\n'):
                line_split[i] = (line_split[i])[:-1]

            if line_split[i] not in movie2act_dict:
                movie2act_dict[line_split[i]] = [actor_name]
            else:
                movie2act_dict[line_split[i]].append(actor_name)

        movies = line_split[1:]
        act2movie_dict[actor_name] = movies

actor_movies_file.close()

# Read actress_movies.txt and build act<->movie dictionaries while reading the file
actress_movies_file = open("actress_movies.txt", "r")
for line in actress_movies_file:
    line_split = line.split("\t")
    line_split = [s for s in line_split if s !='']
    actress_name = line_split[0]

    if (len(line_split) >= 6):
        for i in range(1, len(line_split)):
            while line_split[i].endswith(' ') or line_split[i].endswith('\n'):
                line_split[i] = (line_split[i])[:-1]

            if line_split[i] not in movie2act_dict:
                movie2act_dict[line_split[i]] = [actress_name]
            else:
                movie2act_dict[line_split[i]].append(actress_name)

        movies = line_split[1:]
        act2movie_dict[actress_name] = movies

actress_movies_file.close()

# Sort all the keys in both dictionaries and build hash tables mapping the indices of the keys
sorted_act_names = sorted(act2movie_dict.keys())
sorted_movie_names = sorted(movie2act_dict.keys())
hashtable_act_name2index = {}
hashtable_movie_name2index = {}
for i in range(len(sorted_act_names)):
    hashtable_act_name2index[sorted_act_names[i]] = i

for i in range(len(sorted_movie_names)):
    hashtable_movie_name2index[sorted_movie_names[i]] = i


print("...Reading movie rating...")
movie_genre_file = open("movie_rating.txt", "r")
movie2genre_dict = {}
line_num1 = 1
for line in movie_genre_file:
    line_split = line.split("\t")
    line_split = [s for s in line_split if s !='']
    movie_name = line_split[0]
    genre = line_split[1][:-1]
    movie2genre_dict[movie_name] = genre

movie_genre_file.close()


print("...Constructing movie_id rating...")
output_file = open('movie_id_rating.txt', 'w')
movie_id2genre_dict = {}
for movie_name,movie_genre in movie2genre_dict.items():

    actors = movie2act_dict.get(movie_name)

    if (actors is not None) and (len(actors)>=5):
        movie_index = hashtable_movie_name2index[movie_name]
        movie_id2genre_dict[movie_index] = movie_genre

        entry = [movie_index, movie_genre]
        text = "\t".join(str(x) for x in entry) + '\n'
        output_file.write(text)

output_file.close()