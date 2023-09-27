// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";


interface Itoken {
    function mint(address to, uint256 amount) external;

    function burn(address _from, uint256 amount) external;

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint);

    function approve(address spender, uint amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint amount);
}

contract DEX_CTF {
    Itoken public tokenA;
    Itoken public tokenB;
    string private flag;
    uint256 public proportion;
    bool public swap;

    constructor(address _tokenA, address _tokenB, string memory _flag, uint256 amountA, uint256 amountB) {
        tokenA = Itoken(_tokenA);
        tokenB = Itoken(_tokenB);
        flag = _flag;
        tokenA.mint(address(this), amountA);
        tokenB.mint(address(this), amountB);
        proportion = (tokenB.balanceOf(address(this)) / tokenA.balanceOf(address(this)));
        swap = false;
    }
        
    function swapAforB(uint256 quantity) public {
        require(tokenA.balanceOf(msg.sender) >= quantity, "Saldo insuficiente de tokenA");
        require((tokenB.balanceOf(address(this)) >= (quantity * proportion)), "Liquidez insuficiente para el intercambio");
        require(tokenA.transferFrom(msg.sender, address(this), quantity), "Fallo en la transferencia de msg.sender al contrato");
        uint256 receivedQuantity = (quantity * proportion);
        require(tokenB.transfer(msg.sender, receivedQuantity), "Fallo en la transferencia desde el contrato al msg.sender");
        swap = true;
    }
    
    function swapBforA(uint256 quantity) public {
        require(quantity > proportion, "Intercambio no justo");
        require(tokenB.balanceOf(msg.sender) >= quantity, "Saldo insuficiente de tokenB");
        require((tokenA.balanceOf(address(this)) >= (quantity / proportion)), "Liquidez insuficiente para el intercambio");
        require(tokenB.transferFrom(msg.sender, address(this), quantity), "Fallo en la transferencia de msg.sender al contrato");
        uint256 receivedQuantity = quantity / proportion;
        require(tokenA.transfer(msg.sender, receivedQuantity), "Fallo en la transferencia desde el contrato al msg.sender");
        swap = true;
    }
    
    function mintA(uint256 amount) public {
        tokenA.mint(msg.sender, amount);
    }

    function mintB(uint256 amount) public {
        tokenB.mint(msg.sender, amount);
    }

    function burningA(uint256 _amount) public {
        require(tokenA.balanceOf(msg.sender) >= _amount, "No tienes esa cantidad");
        tokenA.burn(msg.sender, _amount);
    }

    function burningB(uint256 _amount) public {
        require(tokenB.balanceOf(msg.sender) >= _amount, "No tienes esa cantidad");
        tokenB.burn(msg.sender, _amount);
    }

    function allowanceA() public view returns (uint) {
        uint allowedTo = tokenA.allowance(msg.sender, address(this));
        return allowedTo;
    }

    function allowanceB() public view returns (uint) {
        uint allowedTo = tokenB.allowance(msg.sender, address(this));
        return allowedTo;
    }

    function balanceA() public view returns (uint256) {
        return tokenA.balanceOf(msg.sender);
    }

    function balanceB() public view returns (uint256) {
        return tokenB.balanceOf(msg.sender);
    }

    function getFlag() public view returns (string memory) {
        require(swap == true, "No has realizado ningun intercambio");
        require(tokenB.balanceOf(msg.sender) > 0 && tokenA.balanceOf(msg.sender) > 0, "Ambos saldos de tokens deben ser mayores que 0");
        require(tokenB.balanceOf(msg.sender) == tokenA.balanceOf(msg.sender), "Los saldos de tokens deben ser iguales");
        return flag;
    }
}
