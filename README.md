# Run with virtualenv
# Run with docker

```shell
docker build -f "Dockerfile" -t stayinyourkot:latest "."
```

```shell
docker run -p 8080:8080 stayinyourkot:latest
```

# Deploy on Google App Engine

An app.yaml file is included with the correct gunicor command to deploy and run on gae.
