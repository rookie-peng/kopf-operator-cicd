FROM private-registry.rootcloud.com/devops/archery-base:1.8.1

WORKDIR /opt/archery

COPY . /opt/archery/

#archery
RUN cd /opt \
    && source /opt/venv4archery/bin/activate \
    && pip3 install -r /opt/archery/requirements.txt \
    && cp /opt/archery/src/docker/supervisord.conf /etc/ 

#port
EXPOSE 9123

#start service
ENTRYPOINT dockerize -wait tcp://archery-mysql:3306 -wait tcp://archery-redis:6379 -timeout 60s /opt/archery/src/docker/startup.sh