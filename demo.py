import os

os.system("python optimize.py --problem vehicle --algorithm random --runs 3 --save_results True")
os.system("python optimize.py --problem vehicle --algorithm nsga2 --runs 3 --save_results True")
os.system("python compare.py --stats_path stats_random stats_nsga2 --stats_names random nsga2 ")