// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

contract Origin{

    string flag;
    address payable public owner;
    address winner;

    constructor(string memory _flag) public payable {
        flag = _flag;
        owner = payable(msg.sender);
    }

    function transfer(address payable _to, uint _amount) public {
        require(tx.origin == owner, "No Owner");
        winner = msg.sender;

        (bool sent, ) = _to.call{value: _amount}("");
        require(sent, "Fallo al enviar cantidad");
    }

    receive() external payable{}

    function balanceTotal() public view returns(uint){
        return address(this).balance;
    }

    function getFlag() public view returns (string memory){
        require(address(this).balance==0,"No has conseguido el ETH");
        require(winner == msg.sender,"No eres el winner. Usa tu smartcontract");
        return flag;
    }

}