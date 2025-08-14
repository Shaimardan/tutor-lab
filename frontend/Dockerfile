FROM node:latest AS builder

COPY ./package.json /frontend/package.json

WORKDIR /frontend

RUN npm i

COPY ./ /frontend

RUN npm run build
