// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.17;

contract forensic_ouch{

    mapping(uint => string) private options;
    mapping(uint => string) private names;
    string private flag;
    uint private number;
    address public owner;
    uint public blockNumber;

    modifier onlyOwner {
        require(msg.sender == owner, "No eres el propietario");
        _;
    }
    
    constructor(string memory _flag, uint _number, string[] memory _list, string[] memory _names) {
        flag = _flag;
        number = _number;
        owner = msg.sender;
        uint counter = _list.length;
        for (uint i=0; i < counter; i++){
            options[i] = _list[i];
            names[i] = _names[i];
        }
    }

    function jump() public onlyOwner {
        blockNumber = block.number;
    }

    function loveisintheair() public onlyOwner {
        blockNumber = block.number;
    }

    function gameover() public onlyOwner {
        blockNumber = block.number;
    }

    function ideaslocas() public onlyOwner {
        blockNumber = block.number;
    }

    function team() public onlyOwner {
        blockNumber = block.number;
    }

    function nostradamus(string memory _option, string memory _name) public {
        require(keccak256(abi.encodePacked(_option)) == keccak256(abi.encodePacked(options[number])),"Sigue haciendo de forense...");
        require(keccak256(abi.encodePacked(_name)) == keccak256(abi.encodePacked(names[number])),"Sigue haciendo de forense, te falta el nombre...");
        owner = msg.sender;
    }

    function getFlag() public view onlyOwner returns(string memory) {
        return(flag);
    }

    
}
