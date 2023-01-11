FROM node:lts as build
# RUN addgroup app && adduser -S -G app app
WORKDIR /var/www/html/app/
COPY package.json ./
RUN npm install -g --unsafe-perm=true --allow-root
RUN  npm install
RUN npm install -g serve
RUN chown -R node /var/www/html/app/
EXPOSE 8080
# RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache
FROM node:lts as stage
# RUN addgroup app && adduser -S -G app app
WORKDIR /var/www/html/app/
# ENTRYPOINT /bin/bash
USER node
CMD ["npm", "run", "dev"]


# docker-composer up # to start the compilation process
# to install npm package run
# docker-compose exec web npm i bootstrap