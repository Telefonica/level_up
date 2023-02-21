// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RichClub {
	string private flag;
	IERC20 private token;

	modifier onlyRichPeople() {
		require(
			token.balanceOf(msg.sender) > 10 ** 18,
			"You are not rich enough"
		);
		_;
	}

	constructor(string memory _flag, IERC20 _token) {
		flag = _flag;
		token = _token;
	}

	function getFlag() public onlyRichPeople returns (string memory) {
		return flag;
	}
}
