# Base image for both Node and Python
FROM node:18-slim AS base

# Install Python and dependencies for AI Core
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Backend API (Node.js) ---
COPY package*.json ./
RUN npm install

# --- AI Core (Python) ---
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Environment setup
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

# Start script
CMD ["npm", "start"]
