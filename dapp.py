import os
import json

from flask import Flask, request, render_template, redirect, url_for
from web3 import Web3

from functions import Functions


DAPP = Flask(__name__)

# Blockchain settings
network = os.environ.get("NETWORK")
network_name = os.environ.get("NETWORK_NAME")
chainid = int(os.environ.get("CHAIN_ID"))
address_owner = os.environ.get("ADDRESS_OWNER")
private_key = os.environ.get("PRIVATE_KEY")
w3 = Web3(Web3.HTTPProvider(network))

# Game settings
LEVEL_BASE = os.environ.get("LEVEL_BASE")

# Files paths
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
challenges = os.path.join(SITE_ROOT, "challenges.json")
challenges_json = json.load(open(challenges))

def init_config():
    if not Functions.get_instance().exist_contracts_file():
        # se crea el diccionario para contract-address.json
        print("contract-address.json no detectado")
        contract_addresses = {network_name: {}}

        # Desplegamos el contrato base y obtenemos dirección
        addr = deploy_base()

        if not addr is None:
            contract_addresses[network_name][LEVEL_BASE] = addr
            contract_list_not1000 = Functions.get_instance().get_contract_list_without1000()
            for contract in contract_list_not1000:
                contract_addresses[network_name][contract] = []

            Functions.get_instance().set_contract_address_file(contract_addresses)
    else:
        contract_addresses = Functions.get_instance().get_contract_address_file()

    return contract_addresses

def deploy_base():
    bytecode = Functions.get_instance().get_bytecode_level(LEVEL_BASE)
    abi = Functions.get_instance().get_abi_level(LEVEL_BASE)

    if bytecode and abi:
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        # Tomamos Nonce
        nonce = w3.eth.getTransactionCount(address_owner)

        # Construimos transacción y comprobamos parámetros del constructor
        params_constructor = Functions.get_instance(
        ).get_constructor_params_level(LEVEL_BASE)

        if int(params_constructor) == 0:
            transaction = contract.constructor().buildTransaction(
                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

            # firmar transacción
            sign_transaction = w3.eth.account.sign_transaction(
                transaction, private_key=private_key)

            # recibo (se espera por ello)
            receipt = w3.eth.wait_for_transaction_receipt(
                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

            # Mostrar el contract address del contrato
            contract_address = receipt.contractAddress
            print("Contract address deployed: {}".format(contract_address))

            return contract_address


def playerScore(user_address):
    instances_list = []
    player_score = 0
    levels = Functions.get_instance().get_contract_list_without1000()

    for level in levels:
        if level in contract_addresses[network_name].keys():
            l = contract_addresses[network_name][level]
            for element in l:
                if element['user_address'] == user_address:
                    instances_list.append(element['contract_address'])
                    instance = element['contract_address']
                    result = base.functions.playerStatus(
                        user_address, instance).call()

                    # result es un array de 3 posiciones: [level,contract_address,flagOK]
                    if result[2]:
                        score = Functions.get_instance().give_me_score(level)
                        print("score: {} user_address: {} en level {}".format(
                            score, user_address, level))
                        player_score += score
                    else:
                        print("user_address: {} no tiene flag en level {}".format(
                            user_address, level))

    print(instances_list)
    return str(player_score)

def playerStats(user_address):
    stats = {}
    levels = Functions.get_instance().get_contract_list_without1000()

    for level in levels:
        if level in contract_addresses[network_name].keys():
            l = contract_addresses[network_name][level]
            for element in l:
                if element['user_address'] == user_address:
                    stats[level] = {}
                    result = base.functions.playerStatus(user_address, element['contract_address']).call()
                    stats[level]['name'] = challenges_json[level]['name']
                    stats[level]['instance'] = element['contract_address']
                    stats[level]['flag'] = result[2]
                    if stats[level]['flag']:
                        stats[level]['score'] = challenges_json[level]['score']
                        stats[level]['flag_value'] = result[1]
                    else:
                        stats[level]['score'] = 0
                        stats[level]['flag_value'] = None
                    #instances_list.append(element['contract_address'])

    return stats

def scoreboard():
    levels = Functions.get_instance().get_contract_list_without1000()
    scores = {}
    for level in levels:
        if level in contract_addresses[network_name].keys():
            l = contract_addresses[network_name][level]
            for element in l:
                user_address = element['user_address']
            
                #si un user_address no está en keys de score
                if not user_address in scores.keys():
                    scores[user_address] = 0

                instance = element['contract_address']
                try:
                    result = base.functions.playerStatus(user_address,instance).call()
                    #result es un array de 3 posiciones: [level,contract_address,flagOK]
                    if result[2]:
                        score = Functions.get_instance().give_me_score(level)
                        scores[user_address] += score
                except Exception as e:
                    scores = {"error": "HTTPConnectionPool"}
                    return scores

    scores_sorted = dict(sorted(scores.items(),key=lambda item: item[1], reverse=True))
    return scores_sorted


# TODO: Añadir las funciones anteriores a la clase Functions
contract_addresses = init_config()
base_address = contract_addresses[network_name][LEVEL_BASE]
abi_base = Functions.get_instance().get_abi_level(LEVEL_BASE)
base = w3.eth.contract(abi=abi_base, address=base_address)

@DAPP.route("/", methods=['GET'])
def go():
    # return render_template("index.html", base_address=None, abi_base=None, challenges=challenges_json)
    return render_template("index.html", base_address=base_address, abi_base=abi_base, challenges=challenges_json)

@DAPP.route("/faqs", methods=['GET'])
def faqs():
    return render_template("faqs.html")

@DAPP.route("/score", methods=['GET'])
def score():
    score = scoreboard()
    return render_template("score.html", score=score)

@DAPP.route("/player", methods=["GET"])
def player():
    if request.method == 'GET':
        if request.args.get('user_address'):
            player_dict = {}
            user_address = request.args.get('user_address')
            player_dict['user_address'] = user_address
            exists_player = base.functions.existPlayer(user_address).call()
            player_dict['exists_player'] = exists_player
            player_dict['score'] = playerScore(user_address)
            player_dict['level'] = playerStats(user_address)

            # return player_dict
            return render_template("player.html",player=player_dict)

    return render_template("player.html",player=None)

@DAPP.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@DAPP.route("/interact", methods=['GET'])
def interact():
    # return render_template("interact.html", base_address=None, abi_base=None, network=None)
    return render_template("interact.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/questions", methods=['GET'])
def questions():
    return render_template("questions.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/ownership", methods=['GET'])
def ownership():
    return render_template("ownership.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/safeguarding", methods=['GET'])
def safeguarding():
    return render_template("safeguarding.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/origin", methods=['GET'])
def origin():
    return render_template("origin.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/relottery", methods=['GET'])
def relottery():
    return render_template("relottery.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/overworld", methods=['GET'])
def overworld():
    return render_template("overworld.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/snippet_delegated", methods=['GET'])
def snippet_delegated():
    return render_template("snippet_delegated.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/blockchain_tour", methods=['GET'])
def blockchain_tour():
    return render_template("blockchain_tour.html", base_address=base_address, abi_base=abi_base, network=network)

@DAPP.route("/rich_club", methods=['GET'])
def rich_club():
    return render_template("rich_club.html", base_address=base_address, abi_base=abi_base, network=network)

# ===================

# Lógica deploys contracts
@DAPP.route("/deploy_interact", methods=['POST'])
def deploy_interact():
    user_address = None
    level = None

    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        transaction = contract.constructor(param).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("interact.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)
                    
                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("interact.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_questions", methods=['POST'])
def deploy_questions():
    user_address = None
    level = None

    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        transaction = contract.constructor(param).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress

                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("questions.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("questions.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_ownership", methods=['POST'])
def deploy_ownership():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        param2 = Functions.get_instance().give_me_params(level)
                        transaction = contract.constructor(param, param2).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                            
                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("ownership.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("ownership.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")
            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_safeguarding", methods=['POST'])
def deploy_safeguarding():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        param2 = Functions.get_instance().give_me_params(level)
                        transaction = contract.constructor(param, param2).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        # Metemos flag y message al contrato desplegado
                        safeguarding = w3.eth.contract(
                            abi=abi, address=contract_address)

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = safeguarding.functions.safeguard(param, param2).build_transaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                            print("update safeguarding contract: flag {} and message {}".format(
                                param, param2))

                        except Exception as e:
                            print(e)
                            return "{}".format(e)
                        
                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("safeguarding.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)
                    
                    else:

                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("safeguarding.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_origin", methods=['POST'])
def deploy_origin():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        transaction = contract.constructor(param).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "value": 1000000, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress

                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("origin.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, show_verify=True)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("origin.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, show_verify=True, error=True, msg="Ya tienes un contrato de este level desplegado")

                else:
                    return ("error con bytecode o ABI")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_relottery", methods=['POST'])
def deploy_relottery():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()

            # return "player good!"
            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        param2 = Functions.get_instance().give_me_params(level)
                        print("lottery number: {}".format(param2))

                        transaction = contract.constructor(param, param2).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "value": 1000000000, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress

                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            # Si no hay error se actualiza el fichero contract-address.json

                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("relottery.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("relottery.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")

                else:
                    return ("error con bytecode o ABI")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"

@DAPP.route("/deploy_overworld", methods=['POST'])
def deploy_overworld():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                bytecode_token = Functions.get_instance().get_bytecode_level("1001")
                abi_token = Functions.get_instance().get_abi_level("1001")
                abi = Functions.get_instance().get_abi_level(level)

                if (bytecode and abi) and (bytecode_token and abi_token):
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract_token = w3.eth.contract(
                            abi=abi_token, bytecode=bytecode_token)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        transaction = contract_token.constructor("IdeasLocas Token", "ILT").buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address_token = receipt.contractAddress
                        print("Contract address Token deployed: {}".format(
                            contract_address_token))

                        # Ahora desplegamos el contrato overworld
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        param = Functions.get_instance().give_me_value()
                        print("flag: {}".format(param))

                        transaction = contract.constructor(param, contract_address_token).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            # Cambiar Owner del contrato Token
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = contract_token.functions.changeOwner(contract_address).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "to": contract_address_token, "nonce": nonce})

                            # firmar transacción
                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            # recibo (se espera por ello)
                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                            print("New Owner: Contrato overworld!")
                            # Si no hay error se actualiza el fichero contract-address.json

                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("overworld.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_token=contract_address_token, abi_token=abi_token)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))
                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)
                        contract = w3.eth.contract(
                            abi=abi, address=contract_address)
                        contract_address_token = contract.functions.token().call()

                        return render_template("overworld.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_token=contract_address_token, abi_token=abi_token, error=True, msg="Ya tienes un contrato de este level desplegado")

                else:
                    return ("error con bytecode o ABI")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"


@DAPP.route("/deploy_snippet_delegated", methods=['POST'])
def deploy_snippet_delegated():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                bytecode_functions = Functions.get_instance().get_bytecode_level("1002")
                abi_functions = Functions.get_instance().get_abi_level("1002")
                abi = Functions.get_instance().get_abi_level(level)

                if (bytecode and abi) and (bytecode_functions and abi_functions):
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract_functions = w3.eth.contract(
                            abi=abi_functions, bytecode=bytecode_functions)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        random_stamina = Functions.get_instance().give_me_params(level)
                        transaction = contract_functions.constructor(random_stamina).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address_functions = receipt.contractAddress
                        print("Contract address Token deployed: {}".format(
                            contract_address_functions))

                        # Ahora desplegamos el contrato overworld
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        param = Functions.get_instance().give_me_value()
                        print("flag: {}".format(param))

                        transaction = contract.constructor(param, contract_address_functions, random_stamina).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            '''# Cambiar Owner del contrato Token
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = contract_functions.functions.changeOwner(contract_address).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "to": contract_address_token, "nonce": nonce})

                            # firmar transacción
                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            # recibo (se espera por ello)
                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                            print("New Owner: Contrato overworld!")
                            # Si no hay error se actualiza el fichero contract-address.json'''

                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("snippet_delegated.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_functions=contract_address_functions, abi_functions=abi_functions)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))
                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)
                        contract = w3.eth.contract(
                            abi=abi, address=contract_address)
                        contract_address_functions= contract.functions.f().call()

                        return render_template("snippet_delegated.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_functions=contract_address_functions, abi_functions=abi_functions, error=True, msg="Ya tienes un contrato de este level desplegado")

                else:
                    return ("error con bytecode o ABI")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"


@DAPP.route("/deploy_blockchain_tour", methods=['POST'])
def deploy_blockchain_tour():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                abi = Functions.get_instance().get_abi_level(level)

                if bytecode and abi:
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                        print(abi)

                        # Tomamos Nonce
                        nonce = w3.eth.getTransactionCount(address_owner)

                        # Construimos transacción y comprobamos parámetros del constructor
                        #params_constructor = Functions.get_instance().get_constructor_params_level(level)
                        param = Functions.get_instance().give_me_value()
                        transaction = contract.constructor().buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        nonce = w3.eth.getTransactionCount(address_owner)
                        transaction2 = contract.functions.set_flag(param).build_transaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "to":contract_address, "nonce": nonce})
                        sign_transaction2 = w3.eth.account.sign_transaction(
                            transaction2, private_key=private_key)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction2.rawTransaction))
                        

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                            
                            # Si no hay error se actualiza el fichero contract-address.json
                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("blockchain_tour.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))

                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)

                        return render_template("blockchain_tour.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, error=True, msg="Ya tienes un contrato de este level desplegado")
            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"




@DAPP.route("/deploy_rich_club", methods=['POST'])
def deploy_rich_club():
    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                # Creamos contrato
                bytecode = Functions.get_instance().get_bytecode_level(level)
                bytecode_token = Functions.get_instance().get_bytecode_level("1003")
                abi_token = Functions.get_instance().get_abi_level("1003")
                abi = Functions.get_instance().get_abi_level(level)

                if (bytecode and abi) and (bytecode_token and abi_token):
                    if not Functions.get_instance().user_hash_level(network_name, level, user_address):
                        contract_token = w3.eth.contract(
                            abi=abi_token, bytecode=bytecode_token)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        transaction = contract_token.constructor().buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address_token = receipt.contractAddress
                        print("Contract address Liquidity Provider deployed: {}".format(
                            contract_address_token))

                        # Ahora desplegamos el contrato rich club
                        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                        nonce = w3.eth.getTransactionCount(address_owner)
                        param = Functions.get_instance().give_me_value()
                        print("flag: {}".format(param))

                        transaction = contract.constructor(param, contract_address_token).buildTransaction(
                            {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})

                        # firmar transacción
                        sign_transaction = w3.eth.account.sign_transaction(
                            transaction, private_key=private_key)

                        # recibo (se espera por ello)
                        receipt = w3.eth.wait_for_transaction_receipt(
                            w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                        # Mostrar el contract address del contrato
                        contract_address = receipt.contractAddress
                        print("Contract address deployed: {}".format(
                            contract_address))

                        try:
                            nonce = w3.eth.getTransactionCount(address_owner)
                            transaction = base.functions.addContract(contract_address, user_address, int(level), param).buildTransaction(
                                {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                            print("param: {}".format(param))

                            sign_transaction = w3.eth.account.sign_transaction(
                                transaction, private_key=private_key)

                            receipt = w3.eth.wait_for_transaction_receipt(
                                w3.eth.send_raw_transaction(sign_transaction.rawTransaction))

                            if not level in contract_addresses[network_name].keys():
                                contract_addresses[network_name][level] = []

                            contract_addresses[network_name][level].append(
                                {'contract_address': contract_address, 'user_address': user_address})

                            Functions.get_instance().set_contract_address_file(contract_addresses)
                            print("updated contract-addresses.json")

                        except Exception as e:
                            print(e)
                            return "{}".format(e)

                        return render_template("rich_club.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_token=contract_address_token, abi_token=abi_token)

                    else:
                        print("{} ya tiene level {} desplegado".format(
                            user_address, level))
                        contract_address = Functions.get_instance().give_me_contract_address(
                            network_name, level, user_address)
                        contract = w3.eth.contract(
                            abi=abi, address=contract_address)
                        contract_address_token = contract.functions.token().call()

                        return render_template("rich_club.html", base_address=base_address, abi_base=abi_base, network=network, contract_address=contract_address, abi_address=abi, contract_address_token=contract_address_token, abi_token=abi_token, error=True, msg="Ya tienes un contrato de este level desplegado")

                else:
                    return ("error con bytecode o ABI")

            else:
                print("No existe player {}".format(user_address))
                return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

        else:
            return "No se ha enviado el user_address ni el level del reto"



@DAPP.route("/verify_origin_attack", methods=['POST'])
def verify_origin_attack():
    if request.method == 'POST':
        if request.form.get('caddress') and request.form.get('cabi'):
            cabi = request.form.get('cabi')
            caddress = request.form.get('caddress')
            nonce = w3.eth.getTransactionCount(address_owner)

            try:
                attack = w3.eth.contract(abi=cabi, address=caddress)
                transaction = attack.functions.attack().build_transaction(
                    {"chainId": chainid, "gasPrice": w3.eth.gas_price, "from": address_owner, "nonce": nonce})
                sign_transaction = w3.eth.account.sign_transaction(
                    transaction, private_key=private_key)
                receipt = w3.eth.wait_for_transaction_receipt(
                    w3.eth.send_raw_transaction(sign_transaction.rawTransaction))
                print(receipt)

                return "Transaction done! Parece que ha ido bien. ¿Has conseguido cambiar algo en el Contrato Origin?"

            except Exception as e:
                return "Error ejecutando método attack. Vuelve a intentarlo!"

        else:
            return "No han introducido Contract Addres ni ABI"

# ===============

@DAPP.route("/deploy", methods=['POST'])
def deploy():
    user_address = None
    level = None

    if request.method == 'POST':
        if request.form.get('user_address') and request.form.get('level'):
            user_address = request.form.get('user_address')
            user_address = w3.toChecksumAddress(user_address)
            level = request.form.get('level')
            print("user_address {} and level {}".format(user_address, level))

            # Chequeamos si usuario / player existe
            exist_player = base.functions.existPlayer(user_address).call()
            # return "player good!"

            if exist_player:
                if int(level) == 0:
                    return redirect(url_for('deploy_interact'), code=307)
                elif int(level) == 1:
                    return redirect(url_for('deploy_questions'), code=307)
                elif int(level) == 2:
                    return redirect(url_for('deploy_ownership'), code=307)
                elif int(level) == 3:
                    return redirect(url_for('deploy_safeguarding'), code=307)
                elif int(level) == 4:
                    return redirect(url_for('deploy_origin'), code=307)
                elif int(level) == 5:
                    return redirect(url_for('deploy_relottery'), code=307)
                elif int(level) == 6:
                    return redirect(url_for('deploy_overworld'), code=307)
                elif int(level) == 7:
                    return redirect(url_for('deploy_blockchain_tour'), code=307)
                elif int(level) == 8:
                    return redirect(url_for('deploy_snippet_delegated'), code=307)
                elif int(level) == 9:
                    return redirect(url_for('deploy_rich_club'), code=307)
            else:
                return redirect(url_for('createPlayer'))
        else:
            return "No me has pasado parametros"

@DAPP.route("/createPlayer", methods=["GET"])
def createPlayer():
    return render_template("create_player.html", base_address=base_address, network=network, abi_base=abi_base)

@DAPP.route("/deletePlayer", methods=["GET"])
def deletePlayer():
    return render_template("delete_player.html", base_address=base_address, network=network, abi_base=abi_base)

@DAPP.route("/playerOptions", methods=["GET"])
def playerOptions():
    user_address = None
    if request.method == 'GET':
        if request.args.get('user_address'):
            user_address = request.args.get('user_address')
            return render_template("player_options.html", user_address=user_address)



'''
if __name__ == '__main__':
    # configuration = Functions.get_instance().initialize_config()
    # network = configuration['network']
    # address_owner = configuration['address_owner']
    # private_key = configuration['private_key']
    # chainid = configuration['chain_id']
    # network_name = configuration['network_name']

    if not Functions.get_instance().exist_contracts_file():
        # se crea el diccionario para contract-address.json
        print("contract-address.json no detectado")
        contract_addresses = {network_name: {}}

        # Desplegamos el contrato base y obtenemos dirección
        addr = deploy_base()

        if not addr is None:
            contract_addresses[network_name][LEVEL_BASE] = addr
            contract_list_not1000 = Functions.get_instance().get_contract_list_without1000()
            for contract in contract_list_not1000:
                contract_addresses[network_name][contract] = []

            Functions.get_instance().set_contract_address_file(contract_addresses)
    else:
        contract_addresses = Functions.get_instance().get_contract_address_file()

    w3 = Web3(Web3.HTTPProvider(network))
    base_address = contract_addresses[network_name][LEVEL_BASE]
    abi_base = Functions.get_instance().get_abi_level(LEVEL_BASE)
    base = w3.eth.contract(abi=abi_base, address=base_address)

    # DAPP.run(
    #     debug=True, host=configuration['listen_host'], port=configuration['port'])
'''