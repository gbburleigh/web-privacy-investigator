FROM python:latest
FROM node:latest

RUN mkdir resources
WORKDIR "/resources"
ADD ./wrapper.js .
ADD ./parse-inspection.py .
ADD ./setup.sh .

RUN git clone https://github.com/the-markup/blacklight-collector.git
RUN mv wrapper.js ./blacklight-collector/
RUN bash setup.sh
WORKDIR "/resources/blacklight-collector"

RUN npm install -g npm
RUN npm install puppeteer
RUN npm install ca-certificates
RUN npm install fonts-liberation
RUN npm install libappindicator3-1
RUN npm install libasound2
RUN npm install libatk-bridge2.0-0
RUN npm install libatk1.0-0
RUN npm install libc6
RUN npm install libcairo2
RUN npm install libcups2
RUN npm install libdbus-1-3
RUN npm install libexpat1
RUN npm install libfontconfig1
RUN npm install libgbm1
RUN npm install libgcc1
RUN npm install libglib2.0-0
RUN npm install libgtk-3-0
RUN npm install libnspr4
RUN npm install libnss3
RUN npm install libpango-1.0-0
RUN npm install libpangocairo-1.0-0
RUN npm install libstdc++6
RUN npm install libx11-6
RUN npm install libx11-xcb1
RUN npm install libxcb1
RUN npm install libxcomposite1
RUN npm install libxcursor1
RUN npm install libxdamage1
RUN npm install libxext6
RUN npm install libxfixes3
RUN npm install libxi6
RUN npm install libxrandr2
RUN npm install libxrender1
RUN npm install libxss1
RUN npm install libxtst6
RUN npm install lsb-release
RUN npm install wget
RUN npm install xdg-utils
RUN npm install --loglevel=error