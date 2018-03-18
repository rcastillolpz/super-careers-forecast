FROM python:2.7

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./ /app

EXPOSE 5000

ENTRYPOINT ["python", "./forecaster.py"]