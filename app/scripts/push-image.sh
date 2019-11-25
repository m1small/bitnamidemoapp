#!/bin/sh

set -eu

. "$(dirname "${0}")/functions.sh"

pushImage() {
  local dir="${1}"
  local tag="$(imageTag)"
  local image="$(echo "${dir}" | sed 's,_,-,g')"

  docker push "${DOCKER_REGISTRY}/${DOCKER_REPOSITORY_PREFIX}${image}:${tag}"
}


if [ "$#" = "0" ] ; then
  dirs="cart catalogsvc front_end order payment user"
else
  dirs="$@"
fi

for dir in "${dirs}" ; do
  pushImage "${dir}"
done

