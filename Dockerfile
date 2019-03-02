FROM ubuntu:18.04

WORKDIR /app
#VOLUME /data

COPY . ./

# install python3
RUN apt-get update
RUN apt-get install python3 -y

# install cronjob
RUN apt-get -y install -qq --force-yes cron
ADD ./devops/crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

# cleanup
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*


CMD cron -f
