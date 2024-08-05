# Python runtime as a parent image
FROM python:3.11

WORKDIR /app

# copy django files to created dir;
COPY . /app

# install needed packages
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

# make port 8000 available to the world outside this container
EXPOSE 8000

# on container launch
ENTRYPOINT ["/app/entrypoint.sh"]
