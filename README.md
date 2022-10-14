# datafest-airflow-workshop
Code used for Datafest Africa workshop on Airflow

## Requirements

To set up this project, you'll need to have the following installed on your Machine:

1. Python (>= 3.7 | can be installed [here](https://www.python.org/downloads/))
2. Docker (can be installed [here](https://docs.docker.com/engine/install/))
3. Docker Compose (>= v1.29.1 | can be installed [here](https://docs.docker.com/compose/install/))
4. Git

## Setup

1. Clone the repository
2. Create a virtual environment. See [here](https://realpython.com/python-virtual-environments-a-primer/)
3. Install requirements
```shell
pip install -r requirements.txt
```
4. Create .env file and update as follows:
```shell
ENV=dev
AIRFLOW__CORE__FERNET_KEY=
AIRFLOW_UID=
```
To get fernet key, see [here](https://composed.blog/airflow/fernet-key)
To get AIRFLOW_UID, for MacOS/Linux users, run the following in your terminal and use the value
```shell
AIRFLOW_UID=$(id -u)
echo $AIRFLOW_UID
```
4. Run setup script:
```shell
chmod a+x ./bin/run-airflow.sh
./bin/run-airflow.sh
```
