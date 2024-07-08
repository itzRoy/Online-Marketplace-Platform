FROM python:3.11-buster as web

RUN groupadd -r docker && useradd -r -g docker -G audio,video -d /home/docker docker

# Install app requirements
COPY --chown=docker:backend requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt --no-cache-dir --use-deprecated=legacy-resolver

# Switch to the backend user
USER docker
WORKDIR /home/docker/code