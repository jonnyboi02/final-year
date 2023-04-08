import subprocess
import uuid
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse

from .forms import ContractForm
from .models import User, Contract
from django.views.decorators.csrf import csrf_exempt
import io, json
from django.contrib.auth import authenticate, login
import os
import http.client
import requests
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import uuid

import re
#from web3 import Web3
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def upload_file(request):
#     if request.method == 'POST' and request.FILES['file']:
#         # generate a unique filename for the uploaded file
#         filename = str(uuid.uuid4())
#         # get the file object from the request
#         file = request.FILES['file']
#         # save the file to the media directory
#         path = os.path.join(settings.MEDIA_ROOT, filename)
#         with open(path, 'wb') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#         # generate a URL for the uploaded file
#         url = request.build_absolute_uri(settings.MEDIA_URL + filename)
#         return HttpResponse(url)
#     else:
#         return render(request, 'upload.html')
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        # get the file object from the request
        file = request.FILES['file']
        filename, ext = os.path.splitext(file.name)
        ext = ext.lower()

        # set the media directory
        media_dir = os.path.join(settings.BASE_DIR, 'media')
        # create the media directory if it doesn't exist
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # save the file to the media directory
        path = os.path.join(media_dir, filename + ext)
        with open(path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # generate a URL for the uploaded file
        url = request.build_absolute_uri('/') + f'media/{filename}{ext}'

        # return the URL as JSON
        return JsonResponse({'url': url})
    else:
        return render(request, 'upload.html')


# def upload_collateral(request):
#     if request.method == 'POST':
#         form = NFTForm(request.POST, request.FILES)
#         if form.is_valid():
#             nft = form.save(commit=False)
#             nft.user = request.user
#             nft.save()
#             return HttpResponseRedirect('/success/')
#     else:
#         form = NFTForm()
#     return render(request, 'upload.html', {'form': form})


@csrf_exempt
def register(request):
    json_data = request.body
    body = json.loads(json_data)
    #query_seller = body['seller']
    username = body['username']
    password = body['password']
    for user in User.objects.filter(username = username):
        if user.username == username:
            return HttpResponseBadRequest("Invalid form data.")
    user = User.objects.create_user(username)
    user.set_password(password)
    url = 'http://localhost:8547'
    headers = {'Content-Type': 'application/json'}
    data = {
            "jsonrpc": "2.0",
            "method": "personal_newAccount",
            "params": [password],
            "id": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    account = response.json().get('result')
    user.set_public_key(account)
    user.save()

    #return JsonResponse({'address': username})



    return HttpResponse(status  = 200)
    #return HttpResponse("Hi")


# def get_all_contracts(request):
#     # connect to a Geth node
#     web3 = Web3(Web3.HTTPProvider('http://localhost:8547'))
#     # get the latest block number
#     block_number = web3.eth.block_number
#     contracts = []
#     # loop through the block and get the transaction receipts for each transaction
#     for i in range(1, block_number+1):
#         block = web3.eth.get_block(i)
#         for transaction in block['transactions']:
#             receipt = web3.eth.get_transaction_receipt(transaction)
#             # check if the transaction is a contract creation
#             if receipt.contract_address:
#                 # add the contract address to the list of contracts
#                 contracts.append(receipt.contract_address)
#     # return the list of contracts as a JSON response
#     return JsonResponse({'contracts': contracts})

@csrf_exempt
def login_view2(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        json_data = request.body
        body = json.loads(json_data)
            #query_seller = body['seller']
        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

#Get the crypto key from the user object
def getAddress(request):
    pattern = r'^0x[a-fA-F0-9]{40}$'
    json_data = request.body
    body = json.loads(json_data)
    username = body['username']
    if re.match(pattern, username):
        return JsonResponse({'key' : username})
    user = User.objects.get(username=username)
    if user is not None:
        return JsonResponse({'key' : user.public_key})
    else:
        return JsonResponse({'error': 'Error occured'}, status=400)


#contract addresss
def contractAPI(request):
    if request.method == 'PUT':
        json_data = request.body
        body = json.loads(json_data)
        contract_address = body['address']
        contract = Contract.objects.create(contract_address = contract_address)
        contract.save()
        return JsonResponse({'contract_address' : contract_address})
    elif request.method == 'GET':
        addresses = [address.contract_address for address in Contract.objects.all()]
        return JsonResponse(addresses, safe=False)

        


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'User account is disabled.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid login credentials.'})
        else:
            return JsonResponse({'success': False, 'message': 'Username and password are required.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# def login_view(request):
#     error = None
#     if request.method == 'POST':
#         user = User.objects.get(username=request.data['username'])
#         if user.check_password(request.data['password']) is True:
#             token, x = Token.objects.get_or_create(user=user)
#             return JsonResponse({'status': 'OK', 'access_key': 'hi'}, status=200)
#         else:
#             return JsonResponse({'status': 'ERROR', 'access_key': ''}, status=400)
#     return JsonResponse({'status': 'ERROR', 'access_key': ''}, status=400)
    
def user_details(request):
    if request.method == "POST":
        try:
            json_data = request.body
            body = json.loads(json_data)
            #query_seller = body['seller']
            username = body['username']
            #username = request.POST['username']
            user = User.objects.get(username=username)
            response = {
                #"username": user.get_username(),
                 "public_key": user.get_public_key(),
                # "key_store": str(user.key_store),
            }
            return JsonResponse(response, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def upload_NFT(request):
    if request.method == 'POST':
        file = request.FILES['file']
        body = json.loads(request.body)
        username = body['username']
        #Gets the object user to link to the NFT
        try:
            user_object = User.objects.get(username = username)
            upload = NFT.objects.create(collateral = file, user=user_object)
            upload.save()
            return HttpResponse("NFT uploaded")
        except:
            return HttpResponse("Error processing NFT")
        
def get_public_key(request):
    body = json.loads(request.body)
    username = body['username']

    user = get_object_or_404(User, username=username)
    public_key = user.public_key
    return JsonResponse({'key': public_key})

def account_info(request):
    json_data = request.body
    body = json.loads(json_data)
    #query_seller = body['seller']
    username = body['username']
    #password = body['password']
    user = User.objects.get(username=username)
    return JsonResponse({'address': user.public_key,'username': user.username})


def send_transaction(request):
    sender_address = request.POST.get('sender_address')
    sender_password = request.POST.get('sender_password')
    recipient_address = request.POST.get('recipient_address')
    value = request.POST.get('value')
    # gas = request.POST.get('gas')
    # gas_price = request.POST.get('gas_price')

    if sender_address.startswith("0x") == False:
        sender_address = "0x" + sender_address

    if recipient_address.startswith('0x') == False:
        recipient_addres = '0x' + recipient_addres

    if value.startswith('0x') == False:
        value = '0x' + value

    url = 'http://localhost:8547'
    headers = {'Content-Type': 'application/json'}

    #Unlock the sender's account
    data = {
        "jsonrpc": "2.0",
        "method": "personal_unlockAccount",
        "params": [sender_address, sender_password, None],
        "id": 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to unlock sender account'})
    

    # Send the transaction
    data = {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [{
            "from": sender_address,
            "to": recipient_address,
            "value": value,
            #"gas": gas,
            #"gasPrice": gas_price
        }],
        "id": 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to send transaction'})
    
    # Return the transaction hash
    transaction_hash = response.json().get('result')
    return JsonResponse({'transaction': transaction_hash})

def get_balance(request, account):
    pattern = r'^0x[a-fA-F0-9]{40}$'
    #In the case that we are given the ethereum address
    if (re.match(pattern, account)):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [account, "latest"],
            "id": 1
        }
        # Send a POST request to the local Geth blockchain JSON-RPC endpoint
        response = requests.post("http://localhost:8547", data=json.dumps(payload), headers={"Content-Type": "application/json"})
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON and extract the balance in Wei
            balance_wei = int(json.loads(response.content)['result'], 16)

            # Convert the balance from Wei to Ether
            balance_eth = balance_wei / 10**18

            # Return a JSON response with the balance in Ether
            return JsonResponse({'balance': str(balance_eth)})
        else:
            # Return an error JSON response
            return JsonResponse({'error': 'Failed to retrieve balance'})
    #In the case that we get given a username
    else:
        for user in User.objects.filter(username = account):
            # if user.username==account:
                address = user.get_public_key()
                payload = {
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [address, "latest"],
                "id": 1
                }
                response = requests.post("http://localhost:8547", data=json.dumps(payload), headers={"Content-Type": "application/json"})
                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the response JSON and extract the balance in Wei
                    #return JsonResponse({'balance': user.public_key})
                    balance_wei = int(json.loads(response.content)['result'], 16)

                    #return JsonResponse({'balance': user.password})

                    # Convert the balance from Wei to Ether
                    balance_eth = balance_wei / 10**18

                    # Return a JSON response with the balance in Ether
                    return JsonResponse({'balance': str(balance_eth)})
                else:
                    # Return an error JSON response
                    return JsonResponse({'error': 'Failed to retrieve balance'})

               
        # # Send a POST request to the local Geth blockchain JSON-RPC endpoint
        #         response = requests.post("http://localhost:8547", data=json.dumps(payload), headers={"Content-Type": "application/json"})
        # # Check if the request was successful
        #         if response.status_code == 200:
        #     # Parse the response JSON and extract the balance in Wei
        #             balance_wei = int(json.loads(response.content)['result'], 16)

        #     # Convert the balance from Wei to Ether
        #             balance_eth = balance_wei / 10**18

        #     # Return a JSON response with the balance in Ether
        #             return JsonResponse({'balance': str(balance_eth)})
        #     else:
        #         return JsonResponse({'error': 'Failed to retrieve balance'})


    return JsonResponse({'error': 'Failed to retrieve balance'})



def create_account(request):
    if request.method == 'GET':
            # Set the endpoint for the JSON-RPC API
        rpc_endpoint = 'http://localhost:8547'

        # Create a JSON-RPC request to retrieve the list of accounts
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_accounts",
            "params": [],
            "id": 1
        }

        # Send the JSON-RPC request to the Geth node
        response = requests.post(rpc_endpoint, json=payload)

        # Parse the response and extract the list of accounts
        response_data = json.loads(response.content)
        accounts = response_data['result']

        # Serialize the list of accounts to JSON and return it in the response
        response_data = {'accounts': accounts}
        return JsonResponse(response_data)
    else:
        # password = request.POST.get('password')
        # username = request.POST.get('username')
        json_data = request.body
        body = json.loads(json_data)
        #query_seller = body['seller']
        username = body['username']
        password = body['password']

        url = 'http://localhost:8547'
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "personal_newAccount",
            "params": [password],
            "id": 1
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        account = response.json().get('result')
        #public_key = ""
        for user in User.objects.filter(username=username):
            if user.username == username:
                user.set_public_key(account)
                #break
                
                #user = User.objects.get(username=username)
        
            
                response_data = {'address': account, 'username': user.get_public_key()}
                return JsonResponse(response_data)

#View that gets all the accounts on a geth node
def get_accounts(request):
    # Set the endpoint for the JSON-RPC API
    rpc_endpoint = 'http://localhost:8547'

    # Create a JSON-RPC request to retrieve the list of accounts
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_accounts",
        "params": [],
        "id": 1
    }

    # Send the JSON-RPC request to the Geth node
    response = requests.post(rpc_endpoint, json=payload)

    # Parse the response and extract the list of accounts
    response_data = json.loads(response.content)
    accounts = response_data['result']

    # Serialize the list of accounts to JSON and return it in the response
    response_data = {'accounts': accounts}
    return JsonResponse(response_data)


def deploy_contract(request):
    # Solidity source code
    install_solc()
    set_solc_version('0.8.0')
    #install_solc("0.6.0")
    source = '''
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

            constructor(
                uint _amount,
                uint _rate,
                uint _duration,
                uint _collateralAmount,
                address _collateralHolder
            ) {
                borrower = msg.sender;
                lender = address(0);
                owner = msg.sender;
                amount = _amount;
                rate = _rate;
                duration = _duration;
                collateralAmount = _collateralAmount;
                collateralHolder = _collateralHolder;
                dueDate = block.timestamp + duration;
                isRepaid = false;
            }

            function makeRepayment() external payable {
                require(msg.value == amount + amount * rate / 100, "Incorrect repayment amount");
                require(msg.sender == borrower, "Only borrower can make repayment");
                require(block.timestamp <= dueDate, "Loan is already overdue");
                isRepaid = true;
                payable(collateralHolder).transfer(collateralAmount);
            }

            function changeLender(address _newLender) external {
                require(msg.sender == lender || lender == address(0), "Only current lender can change the lender");
                lender = _newLender;
                owner = _newLender;
            }

            function changeOwner(address _newOwner) external {
                require(msg.sender == owner, "Only current owner can change the owner");
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
                address _collateralHolder
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
                    collateralHolder
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
        }
            '''

    # Compile the source code
    compiled_sol = compile_source(source)

    # Get the contract interface and bytecode
    contract_interface = compiled_sol['<stdin>:Loan']
    bytecode = contract_interface['bin']

    # Set up the web3 provider and account
    w3 = Web3(Web3.HTTPProvider('http://localhost:8547'))
    w3.eth.default_account = w3.eth.accounts[0]

    # Deploy the contract
    tx_hash = w3.eth.contract(abi=contract_interface['abi'], bytecode=bytecode).constructor(
        100, 10, 30, 200, w3.eth.accounts[1]
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Save the contract address
    contract_address = tx_receipt.contractAddress

    return HttpResponse(f'Contract deployed at address: {contract_address}')