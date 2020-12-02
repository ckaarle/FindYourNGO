FROM node:10
RUN npm install -g @angular/cli
COPY package.json ./
RUN npm install
WORKDIR ./app
#ENTRYPOINT ng serve
ENTRYPOINT tail -f /dev/null