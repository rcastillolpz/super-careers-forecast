## super-careers-forecast

This is a python/flask API which retrieves information about London forecast.

The API is fed by [OpenWeatherMap](www.openweathermap.org) API.

## API Files:
- `forecaster.py`: the Python/flask API
- `cfg.py`: Configuration file which is read by forecaster.py

## DOCKER Files:
- `Dockerfile`
- `requirements.txt`: This is read by Dockerfile
- `docker-compose.yml`

## Requirements:
You will need to have docker installed on your computer.

## How to run and set the application ?
* Download the repository.
* Go to the downloaded folder where the Docker files are located and build a docker image:
```
docker build -t super-careers-forecast:latest .
```
* Run the image in a container using port 5000:
```
docker run -p 5000:5000 super-careers-forecast
```
* Now, the app is running. You can call the API on:
```
http://<docker ip>:5000/weather/london/yyyymmdd/hhmm/
```
* Optional. If you prefer, you can run the app with **docker-composer**, so you will not have to use docker ip. If previous container is running, you should stop it before execute **docker-composer**:
```
docker stop <container id>
```
* Now, we can exeute **docker-composer**:
```
docker-composer up
```
* You could chase the API on:
```
http://localhost:5000/weather/london/yyyymmdd/hhmm/
```
