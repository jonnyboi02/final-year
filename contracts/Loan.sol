pragma solidity ^0.8.0;

//geth --http.api "personal,eth,net,web3" --miner.etherbase 0x90331b6e55da29a705c28c5dbe6d5b47e23c7aae --networkid 16969 --datadir "./data" --bootnodes enode://e297a68f525b4f12c63a783b69e9a15fb00db71070f037c14af1298f3464c2dce1659531b73416c57fab0138f45051bd01b452f3b9cdfeda7ebd157ae375cf1f@127.0.0.1:0?discport=30301 --port 30303 --ipcdisable --syncmode full --http --allow-insecure-unlock --http.corsdomain "*" --http.port 8547 --unlock 0x90331B6e55DA29A705C28C5DbE6d5B47E23C7aae --password password.txt --mine console  --unlock 0

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
       // address _borrower,
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
            //borrower,
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
