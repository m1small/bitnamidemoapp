#!/bin/sh

set -eu

if [ "${CHARTMUSEUM_KUBEAPPS_REPO:-}" != "" ] ; then
  echo "Patching kubeapps ${CHARTMUSEUM_KUBEAPPS_REPO} repository..."
  kubectl patch apprepos -n kubeapps "${CHARTMUSEUM_KUBEAPPS_REPO}" -p "[{\"op\": \"replace\", \"path\": \"/spec/resyncRequests\", \"value\": \"$(date +%s)\"}]" --type=json
fi
