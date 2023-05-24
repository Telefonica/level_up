// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.4;

contract Lottery{

    mapping(address => uint) public players;
    mapping(address => uint) private players_opportunity;
    string flag;
    uint number;
    address public owner;
    
    constructor(string memory _flag, uint _number) payable {
        flag = _flag;
        number = _number;
        owner = msg.sender;
    }

    //alta lottery
    function pagarBoleto() public payable {
        require(msg.value >= 1000000 wei,"Debes pagar. 1000000 wei => 1 oportunidad. 2000000 wei => 2 oportunidades. +2000000 wei 4 oportunidades");
        players[msg.sender] += msg.value;
        if (msg.value < 2000000 wei){
            players_opportunity[msg.sender] += 1;
        }
        else if (msg.value == 2000000 wei){
            players_opportunity[msg.sender] += 2;
        }
        else{
            players_opportunity[msg.sender] += 4;
        }
    }

    //acertar numero lottery
    function ganarLottery(uint _number) public payable returns (string memory){
        require(players_opportunity[msg.sender] > 0,"Debes comprar boleto. No tienes oportunidades");
        if(_number == number)
        {
            //ganas la lottery
            (bool sent, ) = msg.sender.call{value: address(this).balance}("");
            require(sent, "Fallo al enviar cantidad");
            return ("Has ganado la lottery. ETH para rebosar!");
        }
        else{
            players_opportunity[msg.sender] -= 1;
            return ("Has fallado. Has perdido un intento");
        }
    }

    function intentos() public view returns(uint){
        return players_opportunity[msg.sender];
    }

    function balanceTotal() public view returns(uint){
        return address(this).balance;
    }

    function anularBoleto() public {
        require(players[msg.sender] > 0,"No tienes fondos");
        (bool sent, ) = msg.sender.call{value: players[msg.sender]}("");
        require(sent, "Fallo al enviar cantidad");
        players_opportunity[msg.sender] = 0;
        players[msg.sender] = 0;
    }

    function getFlag() public view returns(string memory){
        require(address(this).balance == 0,"Si hay fondos no puedes conseguir la flag");
        return flag;
    }
    

}