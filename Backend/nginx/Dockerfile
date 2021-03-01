FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY dist /app
COPY nginx.conf /etc/nginx/conf.d