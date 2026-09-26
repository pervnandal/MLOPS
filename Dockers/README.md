### Running and pulling docker images

```
docker run -d -p 80:80 image_name
-d --> running image in detached mode
-p --> assing port to local machine with docker container

docker pull image_name
docker images --> to check the images
docker ps --> to check the container
```

### Building a docker image

```
docker build -t image_name:image_tag .
```

### Rename docker image

docker tag image_name new_image_name

### Delete docker image

docker image rm -f image_name

### Docker hub upload

docker push image_name
