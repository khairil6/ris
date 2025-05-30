FROM node:18-alpine

WORKDIR /app

# build tools often needed by Nuxt modules
RUN apk add --no-cache python3 make g++ git \
 && npm install -g nuxi@latest

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
