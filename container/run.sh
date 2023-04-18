#!/usr/bin/env bash
redis-commander \
  --redis-host ${REDIS_HOST} \
  --redis-port ${REDIS_PORT} \
  --redis-password ${REDIS_PASSWORD} \
  --redis-tls \
  --http-auth-username "${UI_USER}" \
  --http-auth-password "${UI_PASSWORD}"
