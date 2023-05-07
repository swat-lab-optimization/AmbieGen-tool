import os
import time
from datetime import datetime

#This script will run the random search and NAGA2 algorithm for the vehicle problem 3 times,
# then it will save the results in the corresponding folder and build convergence plots and quality/diversity boxplots
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y") + "_"
start = time.time()
os.system("python optimize.py --problem vehicle --algorithm random --runs 3 --save_results True")
os.system("python optimize.py --problem vehicle --algorithm nsga2 --runs 3 --save_results True")
os.system("python compare.py --stats_path " + dt_string +  "stats_random " + dt_string + "stats_nsga2 --stats_names Random NSGA-II ")
duration = time.time() - start
print("Running time", duration)