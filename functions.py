'''
© 2023 Telefónica Digital España S.L.
This file is part of Level_Up!.
Level_Up! is free software: you can redistribute it and/or modify it under the terms of the Affero GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
Level_Up! is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the Affero GNU General Public License for more details.
You should have received a copy of the Affero GNU General Public License along with Level_Up!. If not, see https://www.gnu.org/licenses/.
'''

import os
import json
from math import fabs
import random

def generate_flag():
    return str(random.getrandbits(128))


def generate_number():
    return random.randrange(10)


def generate_number_5digits():
    return random.randrange(99999)


class Functions:
    __instance = None

    def __init__(self):
        if Functions.__instance == None:
            Functions.__instance = self

            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

            self.file_bytecode = os.path.join(SITE_ROOT, str(os.environ.get("FILE_BYTECODES_PATH")))
            self.file_abi = os.path.join(SITE_ROOT, str(os.environ.get("FILE_ABI_PATH")))
            self.file_data = os.path.join(SITE_ROOT, str(os.environ.get("FILE_DATA_PATH")))
            self.file_contract_address = os.path.join(SITE_ROOT, str(os.environ.get("FILE_CONTRACT_ADDRESS")))

    @staticmethod
    def get_instance():
        if Functions.__instance == None:
            Functions()

        return Functions.__instance

    def get_contract_address_file(self):
        with open(self.file_contract_address) as addresses:
            contract_addresses = json.load(addresses)

        return contract_addresses

    def set_contract_address_file(self, addresses):
        with open(self.file_contract_address, "w") as data:
            f = json.dumps(addresses)
            data.write(f)

    def get_bytecode_level(self, level):
        with open(self.file_bytecode) as data:
            bytecode = json.load(data)

        if str(level) in bytecode.keys():
            return bytecode[str(level)]['bytecode']

        else:
            return None

    def get_abi_level(self, level):
        with open(self.file_abi) as data:
            abi = json.load(data)

        if str(level) in abi.keys():
            return abi[str(level)]['abi']

        else:
            return None

    def get_constructor_params_level(self, level):
        with open(self.file_data) as data:
            d = json.load(data)

        if str(level) in d.keys():
            return d[str(level)]['constructor']

        else:
            return None

    def give_me_params(self, level):
        if int(level) == 2:
            return generate_number()

        if int(level) == 3:
            return "secret"

        if int(level) == 5:
            return generate_number_5digits()
        
        if int(level) == 8:
            return generate_number()
        
        if int(level) == 10:
            return generate_number()

    def give_me_value(self):
        return generate_flag()

    def exist_contracts_file(self):
        if not self.file_contract_address is None:
            return os.path.exists(self.file_contract_address)

    def get_contract_list_without1000(self):
        l = []

        if not self.file_data is None:
            with open(self.file_data) as data:
                d = json.load(data)
                for key in d.keys():
                    if int(key) < 1000:
                        l.append(key)

        return l

    def give_me_template(self, level):
        with open(self.file_data) as data:
            d = json.load(data)
        template = d[level]['template']

        return template

    def user_hash_level(self, network_name, level, user_address):
        hash_level = False
        with open(self.file_contract_address) as data:
            levels = json.load(data)
            if level in levels[network_name].keys():
                l = levels[network_name][level]
                for record in l:
                    if record['user_address'] == user_address:
                        hash_level = True
                        break

        return hash_level

    def give_me_contract_address(self, network_name, level, user_address):
        address = None

        with open(self.file_contract_address) as data:
            levels = json.load(data)
            l = levels[network_name][level]
            for record in l:
                if record['user_address'] == user_address:
                    address = record['contract_address']
                    break

        return address

    def give_me_score(self, level):
        with open(self.file_data) as data:
            d = json.load(data)

        if str(level) in d.keys():
            return d[str(level)]['score']

        else:
            return None
