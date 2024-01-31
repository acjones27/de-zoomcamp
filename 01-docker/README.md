# NOTES

# Intro to docker

Main benefits:

- Isolation. We can install things on containers running on our local computer that don’t conflict with our actual local installations
- Reproducibility. We can use the image on our local computer, on a VM, on someone else’s computer and we will get exactly the same environment and results
- Integration tests via CI/CD (tbd how docker is used for this) - e.g. github actions, jenkins
- Running on the cloud e.g. Kubernetes
- Spark
- Serverless - Processing data

## Commands

### Check that docker works

```bash
docker run hello-world
```

### Run an image and do something

`docker run` means to run the image

`-it` means to run in interactive mode

`ubuntu` is the name of the image we want to run

`bash` is the command we want to run

```bash
docker run -it ubuntu bash
```

everything after the image name is a parameter

If we do something stupid, we can just `exit` and create another container by running the same command

## Image with a tag

```bash
docker run -it python:3.9
```

We enter directly into a python interpreter

What if we want to enter a bash terminal on this image so that we can e.g. install pandas?

### Overriding entrypoint

```bash
docker run -it --entrypoint=bash python:3.9

$ pip install pandas
$ python 
>>> import pandas as pd
```

But this only works once because it’s an isolated environment. So we should do this in a Dockerfile to define a new image where we can install the packages we need

### Dockerfile

```docker
FROM python:3.9

RUN pip install pandas

ENTRYPOINT [ "bash" ]
```

If we have this in our current directory, then when we build the image we just specify `.` as the path, otherwise we need to point the build to the path to find the Dockerfile

We also have to specify a tag `-t` which consists of `imagename:tag`

```bash
docker build -t test:pandas .
```

Now we can use it

```bash
docker run -it test:pandas

$ python
>>> import pandas as pd
```

### Copying files

Let’s create a local file `[pipeline.py](http://pipeline.py)` with some code and run it on the docker image

For that we need to copy it so we add the following commands to our docker file (after `RUN`)

```docker
WORKDIR /app
COPY pipeline.py pipeline_on_machine.py
```

`WORKDIR` will create a folder called `app` and cd into this directory

`COPY` will copy the file `pipeline.py` from our local to the container and call it `pipeline_on_machine.py` (it could have had the same name but i wanted to clarify which is which)

Now we can rebuild

```docker
FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "bash" ]
```

```bash
docker build -t test:pandas . # will overwrite the image
docker run -it test:pandas

$ pwd
/app

$ ls
pipeline.py

$ python pipeline.py
```

### Running code

We don’t actually want to go into the container and run it manually, we want the dockerfile to do it, so we need to change the entrypoint

```docker
ENTRYPOINT [ "python", "pipeline.py" ]
```

We could just run it as a command like `RUN python [pipeline.py](http://pipeline.py)` and then we could keep bash as our entrypoint for the interactive mode, but then we wouldn’t see the output and we couldn’t parameterize it and pass args from the CLI (see below)

### Arguments

If we want to pass arguments to the command, we can do it like so

`pipeline.py`

```python
import sys
import pandas as pd

print(sys.argv)

day = sys.argv[1]  # First argument
# Do some stuff

print(f"Job finished successfully for day = {day}!")
```

```bash
docker build -t test:pandas .
docker run test:pandas 2021-01-15

['pipeline.py', '2021-01-15']
Job finished successfully for day = 2021-01-15!
```

Note: We don’t need the -it here since it will run the script and then exit the image anyway

## Setting up postgres image


```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_db:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

- Environment variables are set using the `-e` option, one for each variable
- Volumes are used to map a local folder on the host machine to a folder on the container. We need to store files for the postgres DB and we also want to persist the data we create
    - Create the local folder `ny_taxi_postgres_db`
    - Map it to a path on the container using the `-v` option (we need the full path or use `$(pwd)` to add the current directory)
- The port is needed to send requests to our DB on the container. We map a port locally to a port on the container (local_port:container_port)

Now if we run this command in the terminal (we have to be in the `01-docker` directory) we see a lot of new folders and files in the `ny_taxi_postgres_db` folder

### Accesing the postgres DB

Install the pgcli package on your host machine

```bash
python -m venv .venv
source .venv/bin/activate
pip install pgcli
```

Check the options with `pgcli --help`. Use the config above in the docker run command to fill in the port, username, database and, when prompted, the password

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Try it out:
- `\dt` list tables
- `SELECT 1;`

## Downloading taxi data

We're using the data from [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), just one month from 1 year on Yellow cabs. Since they changed the format to parquet recently, the zoomcamp recommended taking their csv from their github so it's easier to follow along with the steps. There's information on the schema etc on the above page if you scroll down

Download the data

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

gunzip yellow_tripdata_2021-01.csv.gz
```

Have a look at it (you can exit `less` with `q`)
```bash
less yellow_tripdata_2021-01.csv
```

Or save a sample and open it in Excel
```bash
head -n 100 yellow_tripdata_2021-01.csv > yellow_tripdata_2021-01_head.csv
```

Check how many lines the data has (1369766 rows)

```bash
wc -l yellow_tripdata_2021-01.csv
```

## Upload data to postgres

See the notebook `upload_taxi_data_to_postgres.ipynb`

You might need to `pip install pandas` (I created a `requirements.txt` with the packages I had to install)

