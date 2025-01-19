# Use the full Node.js image instead of Alpine
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Next.js will run on
EXPOSE 3000

# Run the development server
CMD ["npm", "run", "dev"]