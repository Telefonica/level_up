// SPDX-FileCopyrightText: © 2023 Telefónica Digital España S.L.

// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

interface IFlashLoanReceiver {
	function executeOperation(address token, uint256 amount) external;
}

contract LiquidityProvider is ERC20, ERC20Burnable {
	uint256 public loan;

	modifier isRepaidOnly() {
		_;
		require(loan == 0, "You must repay the loan first");
	}

	constructor() ERC20("IdeasLocas_Token", "ILT") {}

	function mint(address _to, uint256 _amount) public payable {
		require(_to != address(0), "only owner can mint");
		require(msg.value == _amount * (1 ether), "Price per token is 1 ETH");
		_mint(_to, _amount);
	}

	function flashLoan(
		address _to,
		uint256 _amount
	) public isRepaidOnly returns (bool) {
		require(_to != address(0), "only owner can mint");

		_mint(_to, _amount);

		loan = _amount;
		IFlashLoanReceiver(_to).executeOperation(address(this), _amount);

		return true;
	}

	function repayLoan(uint _amount) public {
		require(loan > 0, "You must have a loan to repay");
		require(_amount == loan, "You must repay the exact amount of the loan");
		require(
			balanceOf(msg.sender) >= _amount,
			"You must have enough tokens to repay the loan"
		);

		_burn(msg.sender, _amount);
		loan = 0;
	}
}
