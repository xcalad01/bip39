# Compile newest version of bip-39 mnemonic
python compile.py


# Run Custom Trezor API in detached mode
docker build -t trezor_api .
docker run --env-file backend_trezor/env -dp 8001:8001 trezor_api


# open mnemonic in browser
open bip39-standalone.html