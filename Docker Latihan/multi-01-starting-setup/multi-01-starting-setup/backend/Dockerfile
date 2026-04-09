from node:24-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 80
CMD ["node","app.js"]

ARG MONGO_USER
ARG MONGO_PASS
ENV MONGO_USER=$MONGO_USER
ENV MONGO_PASS=$MONGO_PASS