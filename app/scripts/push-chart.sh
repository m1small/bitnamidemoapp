#!/bin/sh

set -eu

. "$(dirname "${0}")/functions.sh"

pushChart() {
  echo "PUSH CHART..."
  local filename="kubernees/helm/acmefitness-$(imageTag).tgz"

  curl --data-binary "@${filename}" ${CHARTMUSEUM_REGISTRY}
}

pushChart
