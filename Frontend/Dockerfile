FROM node:14
RUN npm install -g @angular/cli
WORKDIR /home/node/app/src
ENTRYPOINT npm install && ng serve --host 0.0.0.0 --live-reload --poll