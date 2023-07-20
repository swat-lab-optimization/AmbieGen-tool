
ga = {"pop_size": 100, "n_gen": 100, "mut_rate": 0.4, "cross_rate": 0.9, "test_suite_size": 10}
files = {"stats_path": "stats", "tcs_path": "tcs", "images_path": "tc_images"}

vehicle_env = {
    "map_size": 200,
    "min_len": 5,  # min road segment length
    "max_len": 30,  # max road segment length
    "min_angle": 10,  # min road segment angle of rotation in degrees
    "max_angle": 80,  # max road angle of rotation in degrees
}

robot_env = {
    "map_size": 40,
    "min_len": 8,  # min wall size
    "max_len": 15,  # max wall size
    "min_pos": 1,  # min wall position along X axis
    "max_pos": 38,  #  max wall position along X axis
}



