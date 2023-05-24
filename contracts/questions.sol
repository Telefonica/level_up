// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.4;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Interact is Ownable{

    string flag;
    
    constructor(string memory _flag) payable {
        flag = _flag;
    }

    function entrypoint() public view returns(string memory){
        return "misterio()";
    }

    function misterio() public pure returns(string memory){
        return "Cuanto es 2+2 Ponlo junto a misterio";
    }

    function misterio4() public pure returns(string memory){
        return "Ahora al resultado anterior resta 1 y ponlo junto a misterio";
    }

    function misterio3() public pure returns(string memory){
        return "soy la primera parte del misterio: 32";
    }

    function entrypoint2() public pure returns(string memory){
        return "cual es el hash de hola en MD5?";
    }

    function checkHash(string memory n) public pure returns(uint){
        require(keccak256(abi.encodePacked(n)) == keccak256(abi.encodePacked("4d186321c1a7f0f354b297e8914ab240")),"No es el hash adecuado");
        return 659;
    }

    function finalChoice(uint a, uint b) public view returns(string memory){
        require(a==32 && b==659,"Los numeros son incorrectos. No hay flag");
        return flag;
    }

}
