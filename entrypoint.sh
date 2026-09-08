#!/usr/bin/env sh

set -eu

exec streamlit run src/cascade_configuration_service/app.py \
  --server.address=0.0.0.0 \
  --server.port="${PORT:-8000}" \
  --server.headless=true
