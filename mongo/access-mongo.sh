docker run -it --rm --network mongodbnet mongo \
    mongo --host mongodb \
        -u mongodb \
        -p mongodb \
        --authenticationDatabase admin \
        mongodb