library(igraph)

fileName = "/Users/seansea/npm-global/demo-app/npm-demo-pkg/ee232e/Project 2/movie_id_rating.txt"
file_rating = file(fileName,open = "r")
lines_rating = readLines(file_rating)
# print(length(lines_rating))
name_list = rep(0,length(lines_rating))
rating_list = rep(0,length(lines_rating))

for (i in 1:length(lines_rating)) {
  each_rating = strsplit(lines_rating[i],"\t")
  name_list[i]=each_rating[[1]][1]
  rating_list[i]=each_rating[[1]][2]
}

#selected by edge weight, and find the candidate also in same community,choose top 500 
tops_Batman <- order(Batman_edge_list[,3],decreasing = TRUE)[1:500]
tops_Mission <- order(Mission_edge_list[,3],decreasing = TRUE)[1:500]
tops_Minions <- order(Minions_edge_list[,3],decreasing = TRUE)[1:500]

tops_Batman_movie <- Batman_edge_list[tops_Batman, ]
tops_Mission_movie <- Mission_edge_list[tops_Mission, ]
tops_Minions_movie <- Minions_edge_list[tops_Minions, ]
# print(tops_Batman_movie)
# print(tops_Mission_movie)
# print(tops_Minions_movie)

############################Batman v Superman: Dawn of Justice (2016)########################
candidate_list_batman=rep(0,500)

#batman community is No.2
comm_batman=membership(fgc)['73395']
print(comm_batman)

#predict batman(73395) rating
for (i in 1:500){
  if (tops_Batman_movie[,1][i] != 73395){
    candidate_list_batman[i]=tops_Batman_movie[,1][i]
  }
  else {
    candidate_list_batman[i]=tops_Batman_movie[,2][i]
  }
}

#get the first avaiable X(10,30,50) ratings of top500 weighted movies related to batman
counter=0 #whileloop
counter1=1#fakeForloop
batman_movieID=rep(0,50)
score_count=0
while(counter<length(batman_movieID)){
  index=which(name_list == candidate_list_batman[counter1])
  if ((length(index)!=0) & (membership(fgc)[as.character(candidate_list_batman[counter1])]==comm_batman)){
    counter=counter+1
    batman_movieID[counter]=candidate_list_batman[counter1]
    score_count=score_count+as.numeric(rating_list[index])
    print(score_count)
  }
  counter1=counter1+1
}
print(batman_movieID)
print(score_count)
batman_rating=score_count/length(batman_movieID)
#get final rating
print(batman_rating)


############################Mission: Impossible - Rogue Nation (2015)########################
candidate_list_mission=rep(0,500)

#mission community is No.2
comm_mission=membership(fgc)['455280']
print(comm_mission)

#predict mission(455280) rating
for (i in 1:500){
  if (tops_Mission_movie[,1][i] != 455280){
    candidate_list_mission[i]=tops_Mission_movie[,1][i]
  }
  else {
    candidate_list_mission[i]=tops_Mission_movie[,2][i]
  }
}

#get the first avaiable X ratings of top500 weighted movies related to mission
counter=0 #whileloop
counter1=1#fakeForloop
mission_movieID=rep(0,50)
score_count=0
while(counter<length(mission_movieID)){
  index=which(name_list == candidate_list_mission[counter1])
  if ((length(index)!=0) & (membership(fgc)[as.character(candidate_list_mission[counter1])]==comm_mission)){
    counter=counter+1
    mission_movieID[counter]=candidate_list_mission[counter1]
    score_count=score_count+as.numeric(rating_list[index])
    print(score_count)
  }
  counter1=counter1+1
}
print(mission_movieID)
print(score_count)
mission_rating=score_count/length(mission_movieID)
#get final rating
print(mission_rating)


#######################################Minions (2015)##########################################
candidate_list_minions=rep(0,500)

#minions community is No.2
comm_minions=membership(fgc)['453038']
print(comm_minions)

#predict mission(453038) rating
for (i in 1:500){
  if (tops_Minions_movie[,1][i] != 453038){
    candidate_list_minions[i]=tops_Minions_movie[,1][i]
  }
  else {
    candidate_list_minions[i]=tops_Minions_movie[,2][i]
  }
}

#get the first avaiable X ratings of top500 weighted movies related to minions
counter=0 #whileloop
counter1=1#fakeForloop
minions_movieID=rep(0,50)
score_count=0
while(counter<length(minions_movieID)){
  index=which(name_list == candidate_list_minions[counter1])
  if ((length(index)!=0) & (membership(fgc)[as.character(candidate_list_minions[counter1])]==comm_minions)){
    counter=counter+1
    minions_movieID[counter]=candidate_list_minions[counter1]
    score_count=score_count+as.numeric(rating_list[index])
    print(score_count)
  }
  counter1=counter1+1
}
print(minions_movieID)
print(score_count)
minions_rating=score_count/length(minions_movieID)
#get final rating
print(minions_rating)
