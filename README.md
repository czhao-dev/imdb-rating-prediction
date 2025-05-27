# IMDb Graph Analysis and Movie Rating Prediction with Machine Learning

This project explores the IMDb movie database using graph theory and machine learning techniques. We analyze connections between actors, movies, and genres to derive insights and predict movie ratings.

## Project Structure

The project processes and analyzes five IMDb data files:

- `actor_movies.txt` – Actors and the movies they've appeared in
- `actress_movies.txt` – Actresses and the movies they've appeared in
- `director_movies.txt` – Directors and their filmographies
- `movie_genre.txt` – Movie genres
- `movie_rating.txt` – IMDb ratings of movies

## Objectives and Methodology

### 1. **Actor Data Preprocessing**
- Merge actor and actress lists.
- Retain only those with ≥5 movies.
- Build `act2movie_dict` and `movie2act_dict` for lookup.
- Store results using pickling for future steps.

### 2. **Actor Network Construction**
- Create a directed weighted graph:
  - Nodes: Actors/Actresses
  - Edge: Shared movie appearances
  - Weight: Normalized count of shared movies
- Built using Python and `igraph`.
- Network stats: 243,989 nodes, 57.8M edges.

### 3. **PageRank Analysis**
- Run PageRank on the actor network to rank influence.
- Compare top-ranked nodes with well-known celebrities.
- Observed discrepancy due to bias toward prolific actors in less-known roles.

### 4. **Movie Network Construction**
- Remove movies with <5 actors.
- Create undirected movie network:
  - Nodes: Movies
  - Edge: Shared actors
  - Weight: Jaccard index of actor sets
- Network stats: 253,744 nodes, 62.2M edges.

### 5. **Community Detection**
- Run Fast Greedy Newman algorithm to detect communities.
- Assign genre tags if genre appears in ≥20% of a community.
- Most frequent genres: Drama, Short.

### 6. **Neighbor Movie Analysis**
- For selected movies:
  - `Batman v Superman (2016)`
  - `Mission: Impossible - Rogue Nation (2015)`
  - `Minions (2015)`
- Find top 5 neighbors based on edge weights and shared community tags.

### 7. **Rating Prediction via Neighborhood Averaging**
- Predict movie ratings using average ratings of 10, 30, and 50 neighbors.
- Results:
  - Predictions fairly close to IMDb ratings.
  - Better performance with moderate training set size.

### 8. **Rating Prediction via Regression**
- Features:
  - Top 5 actor PageRank scores
  - Director isTop100 boolean (1/0)
- Trained linear regression with scikit-learn.
- R² ≈ 0.005 – weak correlation observed.

### 9. **Rating Prediction via Bipartite Graph**
- Bipartite graph: Actors ↔ Movies
- Actor score: Average of top 5 movie ratings
- Movie score: Average score of its actors
- Outperformed regression approach, especially for live-action films.

## Results Summary

| Method                      | Prediction Accuracy | Notes |
|----------------------------|---------------------|-------|
| PageRank Analysis          | N/A                 | Good for network centrality, not fame |
| Neighborhood Averaging     | Moderate            | Best with 30–50 neighbors |
| Linear Regression          | Low (R² = 0.005)    | Poor due to weak features |
| Bipartite Graph Averaging  | Strong              | Most accurate overall |

## How to Run

Install Python dependencies:
```bash
pip2 install -r requirements.txt
run run_all.sh
```

## Dependencies

- Python 2.7
- igraph (Python + R)
- scikit-learn
- Regular expressions (re)
- Pickle

## Notes

- Data cleaning and formatting were critical for network integrity.
- Genre tagging and network construction were memory-intensive and optimized using hashing and lookup tables.
- The study highlights the tradeoffs between algorithmic influence scoring and actual popularity or fame.

## License

This project is released for academic and research purposes. Please credit the source if used in publications or derivative works. No commercial use of IMDb data is intended. 
