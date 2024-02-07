## Question 1

Explore the `--help` information for `docker`, `docker build` and `docker run`


``` bash
docker run --help
```


We see that the option`--rm` has the text "Automatically remove the container when it exits"

## Question 2

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed ( use pip list ).

What is version of the package wheel?

```bash
docker run -it --entrypoint bash python:3.9
pip list | grep wheel
> wheel      0.42.0
```

## Prepare Postgres

Check the `docker_compose_env_vars` and update them as necessary

```
CSV_TAXI_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz" CSV_TAXI_FILENAME=green_tripdata_2019-09.csv 
```

Build the image with our ingestion script (NOTE: every time we change the python file, we need to rebuild the image)

```bash
docker build -t ingest_data:v0.0.1 .
```

If we get an error with e.g. "error checking context: can't stat '/home/ajones_de_zoomcamp/de-zoomcamp/01-docker/data/ny_taxi_postgres_db'", this is likely due to us not having permissions to the folder ny_taxi_postgres_db. We can get around this by adding a .dockerignore file with our data folder

```dockerignore
data
```

Run docker compose

```bash
docker-compose --env-file docker_compose_env_vars up -d
```

## Question 3

How many taxi trips were totally made on September 18th 2019? Tip: started and finished on 2019-09-18.


```sql
SELECT COUNT(*)
FROM GREEN_TAXI_DATA
WHERE CAST(LPEP_PICKUP_DATETIME AS date) = '2019-09-18'
	AND CAST(LPEP_DROPOFF_DATETIME AS date) = '2019-09-18'

> 15612
```
## Question 4

Which was the pick up day with the longest trip distance? Use the pick up time for your calculations. Tip: For every trip on a single day, we only care about the trip with the longest distance.

```sql
SELECT CAST(LPEP_PICKUP_DATETIME AS date) AS PICKUP_DATE,
	MAX(TRIP_DISTANCE) AS MAX_DISTANCE
FROM GREEN_TAXI_DATA
GROUP BY 1
ORDER BY 2 DESC

> 2019-09-26
```

## Question 5

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

```sql
SELECT "Borough",
	SUM(TOTAL_AMOUNT) AS TOTAL
FROM GREEN_TAXI_DATA T
INNER JOIN ZONES Z ON T."PULocationID" = Z."LocationID"
WHERE CAST(LPEP_PICKUP_DATETIME AS date) = '2019-09-18'
	AND Z."Borough" != 'Unknown'
GROUP BY 1
HAVING SUM(TOTAL_AMOUNT) > 50000
ORDER BY 2 DESC

> Brooklyn, Manhattan, Queens
```

## Question 6

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's tip , not trip

```sql
SELECT ZD."Zone",
	MAX(T.tip_amount) AS MAX_TIP
FROM GREEN_TAXI_DATA T
INNER JOIN ZONES ZP ON T."PULocationID" = ZP."LocationID"
INNER JOIN ZONES ZD ON T."DOLocationID" = ZD."LocationID"
WHERE CAST(DATE_TRUNC('MONTH', LPEP_PICKUP_DATETIME) AS DATE) = '2019-09-01'
AND ZP."Zone" = 'Astoria'
GROUP BY 1
ORDER BY MAX_TIP DESC

> JFK Airport
```

## Push to git

```bash
git config --global user.email "indianna27@gmail.com"
git config --global user.name "Anna Jones"
```