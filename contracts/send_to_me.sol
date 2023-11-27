// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract sendToMe {
    string private flag;

    constructor(string memory _flag) {
        flag = _flag;
    }

    function getFlag() public view returns(string memory) {
        require(address(this).balance > 1, "Contract balance must be over 1 wei");
        return(flag);
    }
}
