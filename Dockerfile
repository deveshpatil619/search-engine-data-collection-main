## This line specifies the base image that this Docker image will be built on top of. 
#In this case, it's the official Python 3.9.14 slim image based on the Debian Bullseye distribution.
FROM python:3.9.14-slim-bullseye

## This line copies the contents of the current directory (where the Dockerfile is located) into
# the /searchengine directory in the Docker image.
COPY . /searchengine

##This line sets the working directory for the image to /searchengine, meaning that all 
# subsequent commands will be executed in this directory.
WORKDIR /searchengine

##runs two commands, separated by &&. The first command upgrades pip to the latest version,
# and the second command installs the Python packages listed in requirements.txt.
RUN pip install --upgrade pip && pip install -r requirements.txt

#exposes port 8080 on the Docker container, which allows external applications to access the
# web server running inside the container.
EXPOSE 8080

## Command that should be executed when a container is started from this image. In this case,
# it runs the app.py file using the Python interpreter. This will start a web server that 
#listens on port 8080 (as specified in the EXPOSE command).

CMD ["python","app.py"]