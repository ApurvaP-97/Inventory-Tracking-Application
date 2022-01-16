FROM python:3.7

COPY configurations.txt /opt/python/configurations.txt
RUN pip install -r /opt/python/configurations.txt \
 && rm -rf /opt/python

COPY app /opt/app

EXPOSE 8000

WORKDIR /opt/app
CMD python app.py run -h 0.0.0.0 -p 8000
