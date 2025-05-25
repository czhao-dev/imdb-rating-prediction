#!/bin/bash

# IMDb Graph Project - Full Pipeline Runner

echo "========================================="
echo "IMDb Graph Analysis Project - Starting..."
echo "========================================="

# Check Python version
PYTHON_VERSION=$(python -V 2>&1)
if [[ $PYTHON_VERSION != *"Python 2.7"* ]]; then
  echo "Error: Python 2.7 is required. Current version: $PYTHON_VERSION"
  exit 1
fi

# Step 1-2: Process Actor and Actress Lists
echo "🔹 Running Q1-2: Building actor/movie dictionaries..."
python Project2_Q1-2.py || { echo "Failed at Q1-2"; exit 1; }

# Step 3: PageRank on Actor Network
echo "🔹 Running Q3: PageRank calculation..."
python Project2_Q3.py || { echo "Failed at Q3"; exit 1; }

# Step 4: Movie Network Construction (Jaccard Index)
echo "🔹 Running Q4: Generating movie edgelist..."
python Project2_Q4_readfile.py || { echo "Failed at Q4 readfile"; exit 1; }
echo "🔹 Running Q4-6.R for community detection..."
Rscript Project2_Q4-6.R || { echo "Failed at Q4-6.R"; exit 1; }

# Step 5: Genre tagging per community
echo "🔹 Running Q5: Generating movie genre mappings..."
python Project2_Q5_readfile.py || { echo "Failed at Q5 readfile"; exit 1; }
echo "🔹 Updating communities in R..."
Rscript Project2_Q4-6.R || { echo "Failed again at Q4-6.R"; exit 1; }

# Step 6: Nearest Neighbor Analysis (already done in Q4-6.R)
echo "🔹 Q6 results already generated from Q4-6.R."

# Step 7: Rating Prediction - Neighborhood Averaging
echo "🔹 Running Q7: Preparing ratings..."
python Project2_Q7_readfile.py || { echo "Failed at Q7 readfile"; exit 1; }
echo "🔹 Predicting with R..."
Rscript Project2_Q7.R || { echo "Failed at Q7.R"; exit 1; }

# Step 8: Rating Prediction - Linear Regression
echo "🔹 Running Q8: Regression prediction..."
python Project2_Q8.py || { echo "Failed at Q8"; exit 1; }

# Step 9: Rating Prediction - Bipartite Graph Method
echo "🔹 Running Q9 (Bonus): Bipartite graph prediction..."
python Project2_Q9_Bonus.py || { echo "Failed at Q9 Bonus"; exit 1; }

echo "========================================="
echo "✅ All steps completed successfully!"
echo "========================================="
