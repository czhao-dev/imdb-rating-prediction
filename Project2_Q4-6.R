library(igraph)

g <- read.graph("H:/Courses_UCLA/232E/project2_v2/movie_edgelist.txt", format=c("ncol"), directed = FALSE)

movie_list <- names(V(g))

weight_arr <- E(g)$weight
fgc <- fastgreedy.community(g, weights=weight_arr)

save.image(file = 'H:/Courses_UCLA/232E/project2/p6.RData')
load('H:/Courses_UCLA/232E/project2/p6.RData')

# Read in the movie_id_genre
con <- file("H:/Courses_UCLA/232E/project2/movie_id_genre.txt", "rt")
movie_genre_content <- readLines(con)
close(con)
rm(con)
movie_genre_split <- unlist(strsplit(movie_genre_content, "[\n]"))
movie_list <- list()
genre_list <- list()
genre_set <- list()
genre_count <- 1
for(i in 1:length(movie_genre_split)){
  l_split <- unlist(strsplit(movie_genre_split[i], "[\t\t]"))
  movie_list[[i]]=l_split[1]
  genre_list[[i]]=l_split[2]
  if (is.element(l_split[2],genre_set) == FALSE) {
    genre_set[[genre_count]] = l_split[2]
    genre_count = genre_count + 1
  }
}

community_fgc <- communities(fgc)
genre_set_comm <- list()
for (n in 1:length(community_fgc)) {
  c_n = community_fgc[[n]]
  genre_set_copy <- as.list(rep(0,length(genre_set)))
  names(genre_set_copy) <- genre_set
  for (i in 1:length(c_n)){
    if(is.element(c_n[i],movie_list)){
      genre_i <- genre_list[which(movie_list==c_n[i])]
      genre_set_i <- which(names(genre_set_copy)==genre_i)
      genre_set_copy[[genre_set_i]] <- genre_set_copy[[genre_set_i]] + 1
    }
  }
  genre_set_comm[[n]] = unlist(genre_set_copy)
  print(n)
}

# Print out the genres for all the communities
for (i in 1:length(genre_set_comm)){
  print(i)
  print(max(unlist(genre_set_comm[[i]]))/length(community_fgc[[i]]))
  print(names(genre_set_comm[[i]][which(genre_set_comm[[i]]==max(genre_set_comm[[i]]))]))
  print('')
}


### Problem 6 ###

# Batman v Superman: Dawn of Justice (2016) --> 73395
# Mission: Impossible - Rogue Nation (2015) --> 455280
# Minions (2015) --> 453038

edge_list <- get.edgelist(g)
weight_list <- E(g)$weight

Batman_edge <- union(which(edge_list[,1]=='73395'),which(edge_list[,2]=='73395'))
Mission_edge <- union(which(edge_list[,1]=='455280'),which(edge_list[,2]=='455280'))
Minions_edge <- union(which(edge_list[,1]=='453038'),which(edge_list[,2]=='453038'))

Batman_edge_list <- matrix(rep(0,length(Batman_edge)*3), ncol = 3)
Mission_edge_list <- matrix(rep(0,length(Mission_edge)*3), ncol = 3)
Minions_edge_list <- matrix(rep(0,length(Minions_edge)*3), ncol = 3)


for (i in 1:length(Batman_edge)){
  edge_list_id <- Batman_edge[i]
  Batman_edge_list[i,1:2] <- as.numeric(edge_list[edge_list_id,])
  Batman_edge_list[i,3] <- weight_list[edge_list_id]
}
for (i in 1:length(Mission_edge)){
  edge_list_id <- Mission_edge[i]
  Mission_edge_list[i,1:2] <- as.numeric(edge_list[edge_list_id,])
  Mission_edge_list[i,3] <- weight_list[edge_list_id]
}
for (i in 1:length(Minions_edge)){
  edge_list_id <- Minions_edge[i]
  Minions_edge_list[i,1:2] <- as.numeric(edge_list[edge_list_id,])
  Minions_edge_list[i,3] <- weight_list[edge_list_id]
}

top5_Batman <- order(Batman_edge_list[,3],decreasing = TRUE)[1:5]
top5_Mission <- order(Mission_edge_list[,3],decreasing = TRUE)[1:5]
top5_Minions <- order(Minions_edge_list[,3],decreasing = TRUE)[1:5]

top5_Batman_movie <- Batman_edge_list[top5_Batman, ]
top5_Mission_movie <- Mission_edge_list[top5_Mission, ]
top5_Minions_movie <- Minions_edge_list[top5_Minions, ]
print(top5_Batman_movie)
print(top5_Mission_movie)
print(top5_Minions_movie)


  
