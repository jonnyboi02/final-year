pragma solidity ^0.8.0;

contract Loan {
    event Received(address, uint256);
    event Transfer(address, uint256);

    address public borrower;
    //address public lender;
    address payable public  owner;
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
    bool public isLate;

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
        //lender = msg.sender;
        owner = payable(msg.sender);
        amount = _amount;
        rate = _rate;
        // duration = _duration;
        collateralAmount = _collateralAmount;
        collateralHolder = _collateralHolder;
        collateralUrl = _collateralUrl;
        price = _price;
        dueDate = block.timestamp + duration;
        isRepaid = false;
        // amountReceived = 0;
        // isLate = false;
    }
    
    //fallout function to receive ethers to the smart contract
    receive() external payable{
        require(!isRepaid, "Loan is already repaid");
        require(msg.sender == borrower, "Only borrower can make repayment");
        amountReceived+=msg.value;
        emit Received(msg.sender, msg.value);
    }

    //call repay then call transfer
    function repay() external payable{
        if (block.timestamp <= dueDate){
            isLate = true;
            
        }
        else{
            require(!isRepaid, "Loan is already repaid");
            require(msg.sender == borrower, "Only borrower can make repayment");
            amountReceived+=msg.value;
            emit Received(msg.sender, msg.value);
        }

    }
    //transfer the funds in the smart contract back to the bank or whoever owns the contract
    function transfer() private{
        require(address(this).balance >= (amount * 1 ether * rate)+amount*1 ether, "Balance not sufficient");
        owner.transfer(address(this).balance);
        isRepaid = true;
        emit Transfer(msg.sender, msg.value);
    }

    // function makeRepayment() external payable {
    //     //require(msg.value == amount + amount * rate / 100, "Incorrect repayment amount");
    //     require(msg.sender == borrower, "Only borrower can make repayment");
    //     // require(block.timestamp <= dueDate, "Loan is already overdue");

    //     if (msg.value >= amount + amount * rate / 100){
    //         isRepaid = true;
    //     } 
    //     payable(collateralHolder).transfer(collateralAmount);
    
    //If the lender needs to be replaced
    // function changeLender(address _newLender) external {
    //     lender = _newLender;
    // }

    //used to change the owner, used for when a user want to buy a contract
    function changeOwner(address _newOwner) external {
        owner = payable(_newOwner);
    }

    function getLoanDetails() external view returns (
        address _borrower,
        //address _lender,
        address _owner,
        uint _amount,
        uint _rate,
        // uint _duration,
        uint _dueDate,
        bool _isRepaid,
        uint _collateralAmount,
        address _collateralHolder,
        string memory _collateralUrl,
        uint _price,
        uint _amountReceived,
        bool _isLate
    ) {
        return (
            borrower,
            //lender,
            owner,
            amount,
            rate,
            // duration,
            dueDate,
            isRepaid,
            collateralAmount,
            collateralHolder,
            collateralUrl,
            price,
            amountReceived,
            isLate
        );
    }
    
    // function repayLoan() external payable {
    //     require(!isRepaid, "Loan is already repaid");
    //     if (block.timestamp > dueDate) {
    //         payable(owner).transfer(address(this).balance + collateralAmount);
    //     } else {
    //         require(msg.value == amount + amount * rate / 100, "Incorrect repayment amount");
    //         isRepaid = true;
    //         payable(collateralHolder).transfer(collateralAmount);
    //     }
    // }
}
