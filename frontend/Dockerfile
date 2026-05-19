FROM node:22-slim AS base

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build step if needed, or just run dev
# For development, we might just want to run npm run dev
# For production, we build
# RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]
