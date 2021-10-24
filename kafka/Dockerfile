#FROM confluentinc/cp-kafka-connect:5.1.0
#
#ENV COMPONENT=kafka-connect
#
#RUN confluent-hub install --no-prompt confluentinc/kafka-connect-mqtt:1.5.0 \
#    && curl -L -k --http1.1 https://cnfl.io/cli | sh -s -- -b /usr/local/bin

FROM confluentinc/cp-kafka-connect-base:5.5.0
ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"
COPY ./confluent-4.1.0 /etc/confluent-4.1.0

RUN echo 'export CONFLUENT_HOME="/etc/confluent-4.1.0"' >> /root/.bashrc
RUN echo 'export PATH="$PATH:$CONFLUENT_HOME/bin"' >>  /root/.bashrc
WORKDIR /etc/confluent-4.1.0/bin/

ENV CONFLUENT_HOME="/etc/confluent"
ENV PATH="${PATH}:$CONFLUENT_HOME/bin"


RUN confluent-hub install confluentinc/kafka-connect-mqtt:latest \
    && curl -L -k --http1.1 https://cnfl.io/cli | sh -s -- -b /usr/local/bin

#RUN echo "===> Installing GCS Sink Connector ..."
#RUN confluent-hub install confluentinc/kafka-connect-gcs:latest --no-prompt