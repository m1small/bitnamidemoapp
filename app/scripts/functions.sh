#!/bin/sh

uniqueBuildTag() {
  echo "${CI_PROJECT_ID}:${CI_PIPELINE_ID}:${CI_RUNNER_ID}" | sha256sum - | sed 's,\s.*$,,'
}

imageTag() {
  echo "${CI_COMMIT_SHA:-$(git rev-parse HEAD)}"
}
