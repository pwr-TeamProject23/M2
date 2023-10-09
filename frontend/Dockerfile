###### DEV HOT RELOAD SERVER ########
FROM node:18-alpine

# Add a work directory
WORKDIR /app

# Setup entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install dependencies
COPY package.json /app/
RUN yarn

# Copy app files
COPY . /app/

# Set startup
EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
CMD ["yarn", "dev"]