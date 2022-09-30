from datetime import datetime
import json
import config as cf
import os


def save_tc_results(tc_stats, tcs):
    """
    It takes two arguments, tc_stats and tcs, and saves them as JSON files in the directories specified
    in the config file

    Args:
      tc_stats: a dictionary of the test cases statistics
      tcs: a list of test cases
    """

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")

    if not os.path.exists(cf.files["stats_path"]):
        os.makedirs(cf.files["stats_path"])
    if not os.path.exists(cf.files["tcs_path"]):
        os.makedirs(cf.files["tcs_path"])

    with open(
        os.path.join(cf.files["stats_path"], dt_string + "-stats.json"), "w"
    ) as f:
        json.dump(tc_stats, f, indent=4)
        print(
            "Stats saved as %s"
            % os.path.join(cf.files["stats_path"], dt_string + "-stats.json")
        )

    with open(os.path.join(cf.files["tcs_path"], dt_string + "-tcs.json"), "w") as f:
        json.dump(tcs, f, indent=4)
        print(
            "Test cases saved as %s"
            % os.path.join(cf.files["tcs_path"], dt_string + "-tcs.json")
        )
