// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Base is Ownable {


    mapping (address => bool) registeredContracts;
    mapping (address => bool) registeredPlayers;
    struct levelStatus{
        uint level;
        string flag;
        bool flagOK;
    }
    mapping(address => mapping(address => levelStatus)) public playerStatus;
    // [player_address][instance_address].levelStatus

    function addContract(address _contract, address _player, uint _level, string memory _flag) public onlyOwner{
        require(!registeredContracts[_contract],"contract already registered");
        require(registeredPlayers[_player],"player not registered");
        registeredContracts[_contract] = true;

        playerStatus[_player][_contract].level = _level;
        playerStatus[_player][_contract].flag = _flag;
        playerStatus[_player][_contract].flagOK = false;

    }

    function delContract(address _contract) public onlyOwner{
        require(registeredContracts[_contract],"contract not registered");
        registeredContracts[_contract] = false;
    }

    function addPlayer() public {
        require(!registeredPlayers[msg.sender],"player already registered");
        registeredPlayers[msg.sender] = true;
    }

    function delPlayer() public{
        require(registeredPlayers[msg.sender],"player not registered");
        registeredPlayers[msg.sender] = false;        
    }

    function existPlayer(address _player) public view returns(bool){
        return registeredPlayers[_player];
    }

    function validateFlag(address _contract,string memory _flag) public payable{
        string memory _f = playerStatus[msg.sender][_contract].flag;
        require(registeredContracts[_contract],"contract not found");
        require(registeredPlayers[msg.sender],"player not found");
        require(keccak256(abi.encodePacked(_f)) == keccak256(abi.encodePacked(_flag)),"flag is not correct");
        playerStatus[msg.sender][_contract].flagOK = true;
    }

    function checkFlag(address _contract, address _player) public view returns(bool){
        return playerStatus[_player][_contract].flagOK;
    }

    /*function generateFlag() private view returns (string memory){
        uint256 f = uint256(keccak256(abi.encodePacked(block.timestamp,msg.sender)));
        return Strings.toString(f);
    }*/


}