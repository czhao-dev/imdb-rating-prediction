import itertools

# Read actor_movies.txt and build act<->movie dictionaries while reading the file
actor_movies_file = open("actor_movies.txt", "r")
act2movie_dict = {}
movie2act_dict = {}
line_num1 = 1
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
    # print("Reading actor_movies.txt...........", (line_num1/2167654)*100, '%', flush=True)
    line_num1 = line_num1 + 1

actor_movies_file.close()

# Read actress_movies.txt and build act<->movie dictionaries while reading the file
actress_movies_file = open("actress_movies.txt", "r")
line_num2 = 1
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

        # print("Reading actress_movies.txt...........", (line_num2 /1182814) * 100, '%', flush=True)
    line_num2 = line_num2 + 1

actress_movies_file.close()

# Sort all the keys in both dictionaries and build hash tables mapping the indices of the keys
sorted_act_names = sorted(act2movie_dict.keys())
sorted_movie_names = sorted(movie2act_dict.keys())
hashtable_act_name2index = {}
hashtable_movie_name2index = {}
for i in range(len(sorted_act_names)):
    hashtable_act_name2index[sorted_act_names[i]] = i
    # print("Building hashtable_act_name2index...........", (float(i)/len(sorted_act_names))*100, '%')

for i in range(len(sorted_movie_names)):
    hashtable_movie_name2index[sorted_movie_names[i]] = i
    # print("Building hashtable_movie_name2index...........", (float(i)/len(sorted_movie_names))*100, '%')


# Process the actors/actresses edgelist and write to a text file
print("Constructing edgelist...")
output_file = open('movie_edgelist.txt', 'w')
movie_combs_dict = {}

# i = 0
for act_name in sorted_act_names:
    movie_list = act2movie_dict[act_name]
    movie_num = len(movie_list)
    if movie_num > 1:
        for pair in itertools.combinations(movie_list, 2):
            movie1_name = pair[0]
            movie2_name = pair[1]
            movie1_index = hashtable_movie_name2index[movie1_name]
            movie2_index = hashtable_movie_name2index[movie2_name]
            if (movie_combs_dict.get(movie1_index) is None) or (movie2_index not in movie_combs_dict.get(movie1_index)):

                movie1_actors = movie2act_dict.get(movie1_name)
                movie2_actors = movie2act_dict.get(movie2_name)
                if (len(movie1_actors)>=5) and (len(movie2_actors)>=5):
                    overlap_actors = len(set(movie1_actors) & set(movie2_actors))
                    total_actors = len(set(movie1_actors) | set(movie2_actors))

                    entry = [movie1_index, movie2_index, float(overlap_actors)/total_actors]
                    text = "\t".join(str(x) for x in entry) + '\n'
                    output_file.write(text)
                   
            if movie_combs_dict.get(movie1_index) is None:
                movie_combs_dict[movie1_index] = [movie2_index]
            else:
                movie_combs_dict[movie1_index].append(movie2_index)

            if movie_combs_dict.get(movie2_index) is None:
                movie_combs_dict[movie2_index] = [movie1_index]
            else:
                movie_combs_dict[movie2_index].append(movie1_index)

    i=i + 1
    print i

output_file.close()