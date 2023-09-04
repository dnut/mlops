FROM python

COPY animal-classes.pkl /app/animal-classes.pkl
COPY input/class.csv /app/class.csv

COPY dist /app/dist
RUN pip install --find-links /app/dist /app/dist/animal_classifier.sklearn_app-0.0.0-py3-none-any.whl

RUN pip install gunicorn

WORKDIR /app/

ENV SKLEARN_PICKLE_PATH=/app/animal-classes.pkl
ENV CLASS_FILE_PATH=/app/class.csv

CMD gunicorn --bind 0.0.0.0:5000 animal_classifier.sklearn_app:app
