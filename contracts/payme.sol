// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

contract MicroPayment {
    string flag;
    address public owner;

    constructor(string memory _flag) {
        flag = _flag;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "No eres el propietario");
        _;
    }

    function payMe() public payable {
        require(msg.value >= 0.000000000001 ether, "No has pagado lo suficiente");
        require(msg.value <= 0.000000001 ether, "Has pagado demasiado");
        owner = msg.sender;
    }

    function getFlag() public view onlyOwner returns (string memory) {
        return flag;
    }

    function giveMeMoney() public onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }
}
