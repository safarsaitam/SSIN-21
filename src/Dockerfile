FROM node:12.18.4-alpine3.12

# Create App Directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install Dependencies
COPY package*.json ./

RUN apk update
RUN apk add openssl
RUN npm ci

# Copy app source code
COPY . .

# Expose server
EXPOSE 3000

CMD ["npm","run","dev"]