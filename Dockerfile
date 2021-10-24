FROM alpine:3.13
WORKDIR /usr/src/app
COPY . /usr/src/app
ADD requirements.txt /usr/src/app
#RUN set -xe apt-get install python3-pip
RUN echo
RUN apk add --update py3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
RUN echo ${PYTHONPATH}
ENTRYPOINT ["python3"]
CMD ["run.py"]
