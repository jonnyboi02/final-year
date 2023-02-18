import subprocess
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import User, NFT
from django.views.decorators.csrf import csrf_exempt
import io, json
from django.contrib.auth import authenticate, login
import os
import http.client
import requests
# from jsonrpcclient.clients.http_client import HTTPClient

#from web3 import Web3
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# class GethView(views.APIView):
#     def post(self, request):
#         data = json.dumps({
#             "jsonrpc": "2.0",
#             "method": "eth_getBalance",
#             "params": [request.data.get('address'), "latest"],
#             "id": 1
#         }).encode()
#         headers = {'Content-Type': 'application/json'}
#         conn = http.client.HTTPConnection('localhost', 8547)
#         conn.request("POST", "/", body=data, headers=headers)
#         response = conn.getresponse()
#         return Response(json.loads(response.read().decode()))

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
    user.save()
    return HttpResponse(status  = 200)
    #return HttpResponse("Hi")

def login(request):
    json_data = request.body
    body = json.loads(json_data)
    #query_seller = body['seller']
    username = body['username']
    password = body['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        #return redirect
    else:
        pass

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
    return JsonResponse({'transaction_hash': transaction_hash})


# def create_account(request):
#     # Get the password from the request
#     password = request.POST.get('password')

#     # Create a JSON-RPC request to create a new account with the provided password
#     data = json.dumps({
#         "jsonrpc": "2.0",
#         "method": "personal_newAccount",
#         "params": [password],
#         "id": 1
#     }).encode()

#     # Set headers and connect to the Geth node
#     headers = {'Content-Type': 'application/json'}
#     conn = http.client.HTTPConnection('localhost', 8547)

#     # Send the JSON-RPC request to the Geth node
#     conn.request("POST", "/", body=data, headers=headers)
#     response = conn.getresponse()

#     # Return the new account address as a JSON response
#     return JsonResponse({'address': json.loads(response.read().decode())})


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
        password = request.POST.get('password')
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
        response_data = {'address': account}
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