import os
import time

#This script will run the random search and NAGA2 algorithm for the vehicle problem 3 times,
# then it will save the results in the corresponding folder and build convergence plots and quality/diversity boxplots

start = time.time()
os.system("python optimize.py --problem vehicle --algorithm random --runs 2 --save_results True")
os.system("python optimize.py --problem vehicle --algorithm nsga2 --runs 2 --save_results True")
os.system("python compare.py --stats_path stats_random stats_nsga2 --stats_names random nsga2 ")
#os.system("python compare.py --stats_path stats_nsga2 --stats_names nsga2")
duration = time.time() - start
print("Running time", duration)