//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "./numbers.sol";

contract Guess{

    string flag;
    uint256 number_flag;
    address public owner;
    numbers public n;

    constructor(string memory _flag, numbers _n, uint256 _number){
        n = numbers(_n);
        owner = msg.sender;
        flag = _flag;
        number_flag = _number;
    }

    function getFlag() public view returns(string memory){
        require(owner == msg.sender,"No eres el propietario del contrato");
        return flag;
    }

    function execution_function(bytes memory _data) public {
        (bool success, bytes memory returnedData) = address(n).delegatecall(_data);
        require(success,"No correcto");
    }        

}



