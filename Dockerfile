FROM --platform=linux/amd64 python:3.10-slim-buster

# Setup flask environment variables
ENV FLASK_APP=dapp
ENV FLASK_RUN_HOST=0.0.0.0

# Env files paths
ENV FILE_BYTECODES_PATH=bytecode.json
ENV FILE_ABI_PATH=abi.json
ENV FILE_DATA_PATH=data.json
ENV FILE_CONTRACT_ADDRESS=contract-address.json

# Env blockchain settings
ENV NETWORK=http://127.0.0.1:7545
ENV NETWORK_NAME=ganache-gui
ENV CHAIN_ID=1337
ENV ADDRESS_OWNER=ADDRESS_OWNER_HERE
ENV PRIVATE_KEY=PRIVATE_KEY_HERE

# Env game settings
ENV LEVEL_BASE=1000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run" ]