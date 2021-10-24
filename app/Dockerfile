FROM alpine:3.13
USER root
WORKDIR /var/www/
ADD . /var/www/
ADD requirements.txt /var/www/
RUN apk add --update py3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip install gunicorn

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]