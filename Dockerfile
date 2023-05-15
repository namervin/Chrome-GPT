# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Clone the Chrome-GPT repository
RUN git clone https://github.com/richardyc/Chrome-GPT.git && ls -l Chrome-GPT

# Set the environment variable for the Chrome binary
ENV CHROME_BIN=/usr/bin/google-chrome

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Set the command to start Chrome-GPT
CMD ["python", "Chrome-GPT/demo.py"]
