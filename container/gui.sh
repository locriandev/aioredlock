#!/usr/bin/env bash
usage() {
  echo "Usage: $0 <http-auth-username> <http-auth-password>"
  echo "    - http-auth-username: Redis Commander username"
  echo "    - http-auth-password: Redis Commander password"
}

if [ "$#" -ne 2 ]; then
  echo "Passed $# args, required 2"
  usage
  exit 1
fi

docker run -d \
  --restart=always \
  -p 8081:8081 \
  --network redis \
  --name gui \
  art/redis-commander \
  redis-commander \
  --redis-host server \
  --redis-password password \
  --http-auth-username $1 \
  --http-auth-password $2
