pragma solidity ^0.8.0;

import "./ERC721.sol";


contract LoanNFT is ERC721 {
    uint256 public tokenCounter;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        tokenCounter = 0;
    }

    function mintLoanNFT(address borrower) external returns (uint256) {
        tokenCounter++;
        _safeMint(borrower, tokenCounter);
        return tokenCounter;
    }
}