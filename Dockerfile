FROM python:2.7.15-stretch

ADD requirements.txt .
ADD utilities_exporter.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["./utilities_exporter.py"]
