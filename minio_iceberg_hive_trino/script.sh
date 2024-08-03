#!/bin/sh

git clone https://github.com/bitsondatadev/hive-metastore.git

sed -i -e 's/METASTORE_TYPE:-mysql/METASTORE_TYPE:-postgres/g' hive-metastore/scripts/entrypoint.sh

docker build -t test-hive-metastore hive-metastore/.

docker-compose up