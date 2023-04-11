pragma solidity ^0.8.0;


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
    uint public amountReceived;

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
        amountReceived = 0;
    }

    function makeRepayment() external payable {
        require(address(this).balance >= (amount * 1 ether * rate)+amount*1 ether, "Balance not sufficient");
        payable(owner).transfer(address(this).balance);
        isRepaid = true;
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
        uint _price,
        uint _amountReceived
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
            price,
            amountReceived
        );
    }
    
    receive() external payable{
        require(!isRepaid, "Loan is already repaid");
        require(msg.sender == borrower, "Only borrower can make repayment");
        amountReceived+=msg.value;
        //emit Received(msg.sender, msg.value);
    }

}
