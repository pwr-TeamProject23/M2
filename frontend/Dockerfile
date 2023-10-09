###### DEV HOT RELOAD SERVER ########
FROM node:18-alpine

# Add a work directory
WORKDIR /app

# Install dependencies
COPY package*.json /app/
RUN yarn

# Copy app files
COPY . /app/

# Set startup
EXPOSE 80
CMD ["yarn", "dev"]