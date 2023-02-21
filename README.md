![ [python_version](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue) ](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

# { level_up! : Web3 Security WarGames }

<p align="center">
  <img src="./static/img/blockchain.jpeg" alt="image" width="256"/>
</p>


**level_up!** is a smartcontracts challenge platform where users can register with their wallet and perform different challenges oriented to their security. In each challenge the corresponding Solidity code can be found for analysis.

**level_up!** is based on the idea that the best way to improve smart contract security is through active participation. By motivating users to work in such an easy way to find security flaws, we hope to improve good programming practices within smart contracts.

## Requirements
- Python 3.9 or 3.10
- [Ganache (CLI or GUI)](https://trufflesuite.com/ganache/)

## Ganache
The easiest way to run Ganache is to use the GUI version, as it allows you to view the necessary information very quickly and the installation is easy to perform.

It is necessary to know the configuration information and then indicate it in the file to be created with the [environment variables](#environment-variables), such as the blockchain address, the port, the chainId and an address together with its private key.

## Environment variables

For the environment variables there must be a file named `.env` in the root of the project (just like the `.flaskenv` file) with the following configuration:

```
# Files paths
FILE_BYTECODES_PATH=bytecode.json
FILE_ABI_PATH=abi.json
FILE_DATA_PATH=data.json
FILE_CONTRACT_ADDRESS=contract-address.json

# Blockchain settings
NETWORK=http://localhost:7545
NETWORK_NAME=ganache-gui
CHAIN_ID=1337
ADDRESS_OWNER=[ADDRESS_OWNER]
PRIVATE_KEY=[PRIVATE_KEY_HERE]

# Game settings
LEVEL_BASE=1000
```

The address and the private key must be specified in order to deploy the contracts.

The `.flaskenv` file contains the environment variables with the information about the flask launch.

## About the virtual environment

**levelup!** can be installed on the global Python environment, however, if you want to install on a virtual environment you can use [`pipenv`](https://pipenv-es.readthedocs.io/es/latest/) or `venv`, among others.

The following is the installation using `pipenv` as the virtual environment manager.

First, you must install `pipenv`. Then, on the root directory of the project, the dependencies are installed and the virtual environment is activated:
```
pipenv install
pipenv shell
```

**Note:** *You must ensure that you are using a supported version of Python, such as 3.9 or 3.10. This can be indicated at the time of creating the environment.*

## Execution

Finally, run **levelup!** with the `flask` command:
```
flask run
```

## Docker

For a more agile deployment, it is possible to run **levelup!** with Docker, mounting the entire environment by using the `docker-compose` command at the root of the project:
```
docker-compose up
```
If Docker is used, it is not necessary to create the `.env` file, since the environment variables are set in the `Dockerfile` file. In the `compose.yaml` are those that have to do with the blockchain configuration, such as `NETWORK`, `NETWORK_NAME`, `ADDRESS_OWNER` and `PRIVATE_KEY`.

## Contact

The goal of **level_up!** is to facilitate learning in a new disruptive world. We recommend to always use it in a test environment, as it is designed and implemented to work in a test environment. We do not recommend using it in a production or real Blockchain (where transactions cost real money and we are not responsible for such use or misuse of the platform).

This software doesn't have a QA Process. This software is a **Proof of Concept**.If you have any problems, you can contact: ideaslocas@telefonica.com