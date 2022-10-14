import argparse
import logging
import os

import yaml
from jinja2 import Environment, FileSystemLoader

CONFIG_DIR = "dag_configs/"
OUTPUT_DIR = "outputs/"

logger = logging.getLogger(__name__)


def fetch_args():
    """Process command line argument options

    Returns
    -------
    arg : namespace values
    """
    p = argparse.ArgumentParser()
    p.add_argument(
        "--job_type",
        help="Type of job to execute.",
        nargs="+",
        type=str,
        required=False,
    )
    p.add_argument(
        "--job_name",
        help="Name of job to execute.",
        nargs="+",
        type=str,
        required=False,
    )
    return p.parse_args()


def fetch_dags(job_types=None, job_names=None):
    """Return the configurations needed for the jobs to compose.
    Consider the passed in filters or return everything if both are None.

    Parameters
    ----------
    job_types : str
        types of jobs to filter down to use for processing
    job_names : str
        names of jobs to filter down to use for processing

    Returns
    -------
    file_location, template, config_name : Tuple[str]
        Location of the configuration
        Template to use for composition
        Name of the configuration
    """

    def filter_condition(item, filter_list):
        ret_val = False
        if filter_list and item not in filter_list:
            ret_val = True
        return ret_val

    # consider all files in the folder (and subfolders) for processing
    for path, folder, configs in os.walk(CONFIG_DIR):
        _, template = os.path.split(path)

        # filter by template name for the type of job to compose
        if filter_condition(template, job_types):
            continue

        for config in configs:
            config_name, _ = os.path.splitext(config)

            # filter by config_name value for the names of jobs to compose
            if filter_condition(config_name, job_names):
                continue

            file_location = os.path.join(path, config)
            yield file_location, template, config_name


def generate_dags():
    def generate_dag(file_location, template, config_name):
        export_filename = os.path.join(OUTPUT_DIR, f"load_{config_name}.py")
        template = env.get_template(f"{template}.template")

        with open(file_location, "r") as configuration_file:
            configuration = yaml.load(configuration_file, Loader=yaml.SafeLoader)

        output = template.render(
            dag_name=config_name,
            version_number=configuration.get("version"),
            description=configuration.get("description"),
            schedule=configuration.get("schedule"),
            max_runs=configuration.get("max_runs"),
            tags=configuration.get("tags"),
            catchup=configuration.get("catchup"),
            endpoint=configuration.get("endpoint"),
        )

        with open(export_filename, "w") as export_file:
            export_file.write(output)
            export_file.write("\n")

        logger.info(f"DAG file {export_filename} created")

    env = Environment(loader=FileSystemLoader("templates"))
    dags_to_generate = fetch_dags(args.job_type, args.job_name)

    for file_location, template, config_name in dags_to_generate:
        generate_dag(file_location, template, config_name)


if __name__ == "__main__":
    # Get the passed in arguments
    args = fetch_args()
    generate_dags()
