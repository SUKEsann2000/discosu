FROM node:24-slim

WORKDIR /usr/src/app

COPY ./src/package*.json ./

RUN npm install --omit=dev

COPY ./src .

EXPOSE 3000

CMD ["node", "server.js"]