// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later

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


