# FROM node:20-alpine3.17 as build
# RUN mkdir /app
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# gitlab-ci job에서 쓸 수 있게 Dockerfile 변경

FROM nginx:stable-alpine
COPY front-web/builds/ /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
