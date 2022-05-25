# FastStatisticsAPI
## Run app
#### 1. Create and fill .env file according to .env.example
### 2. Build container
```shell
docker build -t fast_statistics_api .
```
### 3. Run container
```shell
docker run -dp 8080:8080 --name fast_statistics_api fast_statistics_api
```
## SwaggerUI located at (http://localhost:8080/docs)








