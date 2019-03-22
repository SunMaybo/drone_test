FROM python:latest
RUN mkdir -p /db/tencent
RUN chmod -R 777 /db/tencent
ADD apiutil.py /apiutil.py
ADD requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
expose 5000
CMD ["python3","apiutil.py"]