// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Interact is Ownable{

    string flag;
    
    constructor(string memory _flag) payable {
        flag = _flag;
    }

    function getFlag() public view returns(string memory){
        return flag;
    }

}


