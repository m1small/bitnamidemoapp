#!/bin/sh

set -eu

. "$(dirname "${0}")/functions.sh"

buildImage() {
  local dir="${1}"
  local tag="$(imageTag)"
  local image="$(echo "${dir}" | sed 's,_,-,g')"

  docker build -t "${DOCKER_REGISTRY}/${DOCKER_REPOSITORY_PREFIX}${image}:${tag}" "${dir}"
}


if [ "$#" = "0" ] ; then
  dirs="cart catalogsvc front_end order payment user"
else
  dirs="$@"
fi

for dir in "${dirs}" ; do
  buildImage "${dir}"
done
