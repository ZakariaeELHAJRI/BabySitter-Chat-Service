FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

EXPOSE 8000
#first time it's work with this command and make migrations and upgrade db
#CMD ["bash", "-c", "alembic upgrade head && wait-for-it --service db:3306 --timeout=60 && uvicorn main:app --host 0.0.0.0 --port 80 --reload"]
# after that it's work with this command
CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 --reload"]


