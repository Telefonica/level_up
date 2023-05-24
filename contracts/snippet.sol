// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.7;

import "./functions.sol";

contract Snippet{

    string snippet_flag;
    address public owner;
    int8 public power;
    int8 stamina;
    functions public f;

    constructor(string memory _flag, functions _f, int8 _stamina){
        f = functions(_f);
        power = f.getPower();
        stamina = _stamina;
        owner = msg.sender;
        snippet_flag = _flag;
    }

    function getFlag() public view returns(string memory){
        require(owner == msg.sender,"No eres el propietario del contrato");
        require(power == 9,"No tienes suficiente fuerza! Pista: de 0 a 10");
        return snippet_flag;
    }

    function getPower() public view returns(int8){
        return power;
    }

    function getStamina() public view returns(int8){
        return stamina;
    }

    function execution_function(bytes memory _data) public {
        (bool success, bytes memory returnedData) = address(f).delegatecall(_data);
        require(success,"Delegada no correcta");
    }        

}



