#!/bin/sh

set -eu

if [ "${DEMO_ENVIRONMENT:-none}" = "aws" ] ; then
  if which git >/dev/null 2>/dev/null ; then
    aws ecr get-login --region us-east-1 | sed 's, -e none , ,'  | sh
  else
    docker run --rm mesosphere/aws-cli ecr get-login --region us-east-1 | sed 's, -e none , ,'  | sh
  fi
fi

if [ "${DOCKER_REGISTRY_USERNAME:-}" != "" ] && [ "${DOCKER_REGISTRY_PASSWORD:-}" != "" ] ; then
  docker login -u "${DOCKER_REGISTRY_USERNAME}" -p "${DOCKER_REGISTRY_PASSWORD}" "${DOCKER_REGISTRY}"
fi
