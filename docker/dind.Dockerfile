# Create a DockerFile inside wich we will run the docker compose command to run the application
FROM docker:dind

ENV APP_HOME /app
WORKDIR /app

EXPOSE 3000 3000

COPY . .

COPY docker/entrypoint-wrapper.sh .
RUN chmod +x entrypoint-wrapper.sh

ENTRYPOINT ["sh", "entrypoint-wrapper.sh"]