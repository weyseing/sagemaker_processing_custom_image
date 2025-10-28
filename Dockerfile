FROM python:3.10-slim

# working dir
WORKDIR /app

# install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app files
COPY . /app

# entrypoint
ENTRYPOINT ["tail", "-f", "/dev/null"]