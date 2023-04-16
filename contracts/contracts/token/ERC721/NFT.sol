pragma solidity ^0.8.0;

import "./ERC721.sol";
import "../../access/Ownable.sol";

contract MyNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    mapping(uint256 => string) private _tokenURIs;
    mapping(uint256 => address) private _originalOwners;
    mapping(address => uint256[]) private _ownedTokens;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    function mint(address to, string memory tokenURI) public onlyOwner returns (uint256) {
        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;
        _mint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        _originalOwners[tokenId] = to;
        _ownedTokens[to].push(tokenId);
        return tokenId;
    }

    function _setTokenURI(uint256 tokenId, string memory tokenURI) internal {
        require(_exists(tokenId), "ERC721Metadata: URI set of nonexistent token");
        _tokenURIs[tokenId] = tokenURI;
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        return _tokenURIs[tokenId];
    }

    function originalOwnerOf(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId), "ERC721: owner query for nonexistent token");
        return _originalOwners[tokenId];
    }

    function transferOwnership(address newOwner) public override onlyOwner {
        super.transferOwnership(newOwner);
    }

    function tokensOfOwner(address owner) public view returns (uint256[] memory) {
        return _ownedTokens[owner];
    }
}
