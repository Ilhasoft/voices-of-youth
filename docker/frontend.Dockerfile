###############################################################################
# Build stage
# Creation date: 12/06/2018
# Author: eltonplima
###############################################################################
FROM node:8-alpine as builder

ENV HOME /home/app

WORKDIR $HOME

RUN apk update && apk add git

COPY package.json .
COPY . .

RUN npm install && npm run build

###############################################################################
# Image creation stage
# Creation date: 06/02/2018
# Author: eltonplima
###############################################################################

FROM nginx:alpine

COPY --from=builder /home/app/frontend/dist/ /home/voy/frontend/
RUN ls -l --color /home/voy/frontend/
COPY docker/voy_frontend.conf /etc/nginx/conf.d/default.conf
