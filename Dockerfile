FROM python:latest
FROM node:latest

ADD ./wrapper.js .
ADD ./parse-inspection.py .
ADD ./setup.sh .

RUN git clone https://github.com/the-markup/blacklight-collector.git
RUN mv wrapper.js ./blacklight-collector/
RUN bash setup.sh
RUN npm install -g npm
WORKDIR "/blacklight-collector"
RUN npm install