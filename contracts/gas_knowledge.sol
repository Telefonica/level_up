// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GasKnowledge  {
    string private  flag;
    uint public gaspricetx;
    address public owner;

    constructor(string memory _flag)  {
        flag = _flag;
        owner = msg.sender;
        gaspricetx = 1;
        gaspricetx = tx.gasprice;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner");
        _;
    }
    
    function add(uint _num1, uint _num2) public returns (uint) {
        uint result = _num1 + _num2;
        require(result == 100, "Improve your maths!");
        require(tx.gasprice > (2 * gaspricetx), "Pay more to get your tx done faster!");
        owner = msg.sender;
        return (result);
    }

    function getFlag() public view onlyOwner returns (string memory) {
        return flag;
    }
}