// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

contract Ownership{

    string flag;
    uint number;
    address public owner;
    mapping (address => uint256) public players;
    mapping (address => uint256) public inflacion;

    
    constructor(string memory _flag, uint _number) public {
        flag = _flag;
        number = _number;
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller no es el owner"
        );
        _;
    }

    function comprarPropiedad() public payable{
        require(msg.value > 1000 ether);
        owner = msg.sender;
    }

    function darAlta() public payable{
        require(msg.value > 0.0000001 ether);
        players[msg.sender] = msg.value;
    }

    function darBaja() public payable{
        require(players[msg.sender] > 0);
        (bool sent, ) = payable(msg.sender).call{value: players[msg.sender]}("");
        if (sent)
        {
            players[msg.sender] = 0;
        }
        require(sent, "Error dando de baja. No se han devuelto Ethers");
    }

    function miInflacion() public view returns(uint){
        return inflacion[msg.sender];
    }

    function miContribucion() public view returns(uint){
        return players[msg.sender];
    }

    function miPista() public pure returns (string memory){
        return "Debes acertar el numero de la propiedad. Entre 0 y 9";
    }

    function cambioPropiedad(uint _number) public payable {
        require(players[msg.sender] > 0,"No has contribuido a la propiedad");
        uint256 incremento = 100000000000000;
        if (!(_number == number)){
            inflacion[msg.sender] += incremento;
        }
        else{
            require(inflacion[msg.sender] <= msg.value,"Adivinaste el numero de la propiedad, pero no has contribuido lo suficiente");
            owner = msg.sender;
        }    
    }

    function getFlag() public view onlyOwner returns(string memory){
        return flag;
    }

}
