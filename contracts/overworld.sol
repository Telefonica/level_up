//SPDX-License-Identifier: MIT

pragma solidity ^0.6.2;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.0.0/contracts/token/ERC20/ERC20.sol";

contract ILT_Token is ERC20{

    address public owner;

    constructor (string memory name, string memory symbol) ERC20(name, symbol) public {
        _mint(msg.sender, 100);
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller no es el owner"
        );
        _;
    }

    function mint(address _address, uint _amount) public onlyOwner{
        _mint(_address,_amount);
    }

    function burn(address _address, uint _amount) public onlyOwner{
        if (balanceOf(_address) - _amount <=0)
        {
            _burn(_address, balanceOf(_address));
        }
        else{
            _burn(_address, balanceOf(_address));
        }
        
    }

    function changeOwner(address _address) public onlyOwner{
        owner = _address;
    }

}

contract OverWorld{

    ILT_Token public token;
    mapping(address => uint8) balances;
    string flag;

    constructor(string memory _flag, ILT_Token _token) public{
        token = _token;
        flag = _flag;
    }

    function mytokens() public view returns(uint8){
        return balances[msg.sender];
    }

    function faucet(uint8 _amount) public{
        require(balances[msg.sender] + _amount != 255,"No puedes llegar a esa cantidad");
        token.mint(msg.sender, _amount);
        balances[msg.sender] += _amount;
    }

    function burning(uint8 _amount) public{
        require(balances[msg.sender]+_amount != 255,"No puedes llegar a esa cantidad");
        token.burn(msg.sender, _amount);
        balances[msg.sender] -= _amount;
    }

    function getFlag() public view returns(string memory){
        require(balances[msg.sender] == 255,"No tienes suficientes tokens");
        return flag;
    }

}