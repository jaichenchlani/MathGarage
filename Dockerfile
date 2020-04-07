FROM python:2.7
MAINTAINER Jai Chenchlani "jaichenchlani@gmail.com"
COPY . /main
WORKDIR /main
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]