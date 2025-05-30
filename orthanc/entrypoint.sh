#!/usr/bin/env sh
set -e

CONFIG_DIR="/data/config"
CONFIG_FILE="${CONFIG_DIR}/orthanc.json"

# If there is no config yet, dump the built-in defaults into it
if [ ! -s "${CONFIG_FILE}" ]; then
  echo "⟳ No custom config—generating default from Orthanc"
  mkdir -p "${CONFIG_DIR}"
  # NOTE the equals sign: this tells Orthanc to *write* the default JSON here
  exec Orthanc --config="${CONFIG_FILE}"
fi

# Otherwise start Orthanc using your mounted JSON
exec Orthanc --config="${CONFIG_FILE}"
