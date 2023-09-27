pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TokenA is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }

    function burn(address _from, uint256 amount) public {
        require(balanceOf(_from) >= amount, "La cantidad debe ser mayor a 0");
        _burn(_from, amount);
    }

}

contract TokenB is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }

    function burn(address _from, uint256 amount) public {
        require(balanceOf(_from) >= amount, "La cantidad debe ser mayor a 0");
        _burn(_from, amount);
    }

}