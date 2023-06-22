// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/// @custom:security-contact ideaslocas@telefonica.com
contract NFT_Level_Up is ERC1155, Ownable {
    uint256 public constant newbie = 1; //0 points
    uint256 public constant rookie = 2; //500 points
    uint256 public constant hero = 3; //1000 points
    uint256 public constant superhero = 4; //1500 points
    uint256 public constant master = 5; //2500 points

    constructor() ERC1155("http://127.0.0.1:5000/{id}.json") 
    {
        
    }

    function setURI(string memory newuri) public onlyOwner 
    {
        _setURI(newuri);
    }

    function mint(address account, uint256 id, uint256 amount, bytes memory data) public onlyOwner
    {
        require(this.balanceOf(account,id) == 0,"you have already minted this NFT");
        _mint(account, id, amount, data);
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) public onlyOwner
    {
        _mintBatch(to, ids, amounts, data);
    }

    function uri(uint256 tokenId) override public pure returns(string memory)
    {
        return (string(abi.encodePacked("http://127.0.0.1:5000/000000000000000000000000000000000000000000000000000000000000000",Strings.toString(tokenId),".json")));
    }
}


