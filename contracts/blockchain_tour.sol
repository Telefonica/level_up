// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract blockchain_tour{

    string flag;
    uint public blocknumber;
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    function set_flag(string memory _flag) public {
        require(owner == msg.sender,"No eres el propietario del contrato");
        flag = _flag;
        blocknumber = block.number;
    }

}