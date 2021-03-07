FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY dist /app
COPY static_files /django/static
COPY nginx.conf /etc/nginx/conf.d