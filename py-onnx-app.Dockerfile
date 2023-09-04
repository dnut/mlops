FROM python

COPY animal-classes.onnx /app/animal-classes.onnx
COPY input/class.csv /app/class.csv

COPY dist /app/dist
RUN pip install --find-links /app/dist /app/dist/animal_classifier.onnx_app-0.0.0-py3-none-any.whl

RUN pip install gunicorn

WORKDIR /app/

ENV ONNX_FILE_PATH=/app/animal-classes.onnx
ENV CLASS_FILE_PATH=/app/class.csv

CMD gunicorn --bind 0.0.0.0:5000 animal_classifier.onnx_app:app
