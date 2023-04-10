pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Loan {
    address public borrower;
    address public lender;
    address public owner;
    uint public amount;
    uint public rate;
    uint public duration;
    uint public dueDate;
    bool public isRepaid;
    uint public collateralAmount;
    address public collateralHolder;
    string public collateralUrl;
    uint public price;

    constructor(
        uint _amount,
        uint _rate,
        uint _duration,
        uint _collateralAmount,
        address _collateralHolder,
        string memory _collateralUrl,
        uint _price
    ) {
        borrower = _collateralHolder;
        lender = msg.sender;
        owner = msg.sender;
        amount = _amount;
        rate = _rate;
        duration = _duration;
        collateralAmount = _collateralAmount;
        collateralHolder = _collateralHolder;
        collateralUrl = _collateralUrl;
        price = _price;
        dueDate = block.timestamp + duration;
        isRepaid = false;
    }

    function makeRepayment() external payable {
        //require(msg.value == amount + amount * rate / 100, "Incorrect repayment amount");
        require(msg.sender == borrower, "Only borrower can make repayment");
        // require(block.timestamp <= dueDate, "Loan is already overdue");
        if (msg.value >= amount + amount * rate / 100){
            isRepaid = true;
        } 
        payable(collateralHolder).transfer(collateralAmount);
    }

    function changeLender(address _newLender) external {
        // require(msg.sender == lender || lender == address(0), "Only current lender can change the lender");
        lender = _newLender;
        owner = _newLender;
    }

    function changeOwner(address _newOwner) external {
        owner = _newOwner;
    }

    function getLoanDetails() external view returns (
        address _borrower,
        address _lender,
        address _owner,
        uint _amount,
        uint _rate,
        uint _duration,
        uint _dueDate,
        bool _isRepaid,
        uint _collateralAmount,
        address _collateralHolder,
        string memory _collateralUrl,
        uint _price
    ) {
        return (
            borrower,
            lender,
            owner,
            amount,
            rate,
            duration,
            dueDate,
            isRepaid,
            collateralAmount,
            collateralHolder,
            collateralUrl,
            price
        );
    }
    
    function repayLoan() external payable {
        require(!isRepaid, "Loan is already repaid");
        if (block.timestamp > dueDate) {
            payable(owner).transfer(address(this).balance + collateralAmount);
        } else {
            require(msg.value == amount + amount * rate / 100, "Incorrect repayment amount");
            isRepaid = true;
            payable(collateralHolder).transfer(collateralAmount);
        }
    }

    function mint(address _to, bytes memory _nftData) public returns (uint256) {
        _safeMint(_to, 0);
    }
}
