FROM node:14
RUN npm install -g @angular/cli
COPY package.json ./
RUN npm install
WORKDIR /home/node/app/src
ENTRYPOINT ng serve --host 0.0.0.0