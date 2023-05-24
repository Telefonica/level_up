// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

contract Safeguard{

    string flag = "firstuse";
    string message;
    address public owner;

    //constructor
    function safeguard(string memory _flag, string memory _message) public payable{
        message = _message;
        require(keccak256(abi.encodePacked(message)) == keccak256(abi.encodePacked("secret")),"Mensaje incorrecto");
        owner = msg.sender;
        if (keccak256(abi.encodePacked(flag)) == keccak256(abi.encodePacked("firstuse")))
        {
            flag = _flag;
            message = "random";
        }
    }

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller no es el owner"
        );
        _;
    }

    function getFlag() public view onlyOwner returns(string memory){
        return flag;
    }

}



