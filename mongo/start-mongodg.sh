docker network create -d bridge mongodbnet
docker run --rm -d --network mongodbnet --name mongodb \
    -p 27017:27017 \
    -v $(pwd)/mongodata:/data/db \
    -e MONGO_INITDB_ROOT_USERNAME=mongodb \
    -e MONGO_INITDB_ROOT_PASSWORD=mongodb \
    mongo