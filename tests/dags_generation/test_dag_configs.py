import os
from pathlib import Path

import yaml

BASE_PATH = Path(__file__).parents[2]
CONFIG_DIR = f"{BASE_PATH}/dags_generation/dag_configs/"


def test_config_has_correct_keys():
    expected = {
        "version",
        "description",
        "schedule",
        "max_runs",
        "tags",
        "catchup",
        "endpoint",
    }

    for path, folder, configs in os.walk(CONFIG_DIR):
        for config in configs:
            file_location = os.path.join(path, config)

            with open(file_location, "r") as configuration_file:
                actual = yaml.load(configuration_file, Loader=yaml.SafeLoader)
                assert expected.issubset([*actual])
