//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract Numbers{

    string flag;
    uint256 number_flag;
    address public owner;

    constructor(uint256 _number_flag){
        flag = "0";
        number_flag = _number_flag;
    }

    function blocks() public view returns(uint){
        return block.number;
    }

    function guess(uint256 _number) public {
        require(number_flag == _number,"No has acertado");
        owner = msg.sender;
    }

    function getFlag() private view returns(string memory){
        require(owner == msg.sender,"No eres propietario");
        return getFlag();
    }

    function setNumberFlag() public{
        require(owner == msg.sender,"No eres propietario");
        flag = getFlag();
    }

}

