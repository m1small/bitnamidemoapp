#!/bin/sh

set -eu

. "$(dirname "${0}")/functions.sh"

prepareValuesYaml() {
  sed -i \
    "s!^.*#PLACEHOLDER:image:registry!  registry: \"${DOCKER_REGISTRY}\"!;s!^.*#PLACEHOLDER:image:repositoryPrefix!  repositoryPrefix: \"${DOCKER_REPOSITORY_PREFIX}\"!;s!^.*#PLACEHOLDER:image:tag!  tag: \"$(imageTag)\"!" \
    "kubernetes/helm/acmefitness/values.yaml"
}

buildChart() {
  tar -czf "kubernetes/helm/acmefitness-$(imageTag).tgz" \
    -C "kubernetes/helm" acmefitness

  ls -la "kubernetes/helm/acmefitness-$(imageTag).tgz"
}

prepareValuesYaml
buildChart
