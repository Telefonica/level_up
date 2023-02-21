//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract functions{

    string snippet_flag;
    address public owner;
    int8 public power;
    int8 stamina;

    constructor(int8 _stamina){
        snippet_flag = "flag_in_the_world";
        power = 0;
        stamina = _stamina;
    }

    function blocks() public view returns(uint){
        return block.number;
    }

    function getPower() public view returns(int8){
        return power;
    }

    function addPower() public{
        power += 5;
    }

    function addStamina() public{
        stamina += 1;
    }

    function delStamina() public{
        stamina -=1 ;
    }

    function addStaminaToPower() public{
        power += stamina;
    }

    function getFlag() private view returns(string memory){
        require(owner == msg.sender,"No eres propietario");
        return getFlag();
    }

    function setOwner() public{
        owner = msg.sender;
    }

    function setSnippetFlag() public{
        require(owner == msg.sender,"No eres propietario");
        snippet_flag = getFlag();
    }
    

}

