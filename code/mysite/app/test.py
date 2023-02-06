import os

def createNode(password):
    os.chdir("gethpoa")
    i = 1
    dir = "node"
    check = dir+str(i)
    while os.path.exists(check):
        i+=1
        check = dir+str(i)
    os.mkdir(check)
    os.chdir(check)
    #Creates textfile containing password to the node
    with open("password.txt", 'w') as f:
        f.write(password)
    #Running geth on a new node
    #os.system("geth --datadir ./data account new --password password.txt")
    output = os.popen("geth --datadir ./data account new --password password.txt").read()
    arr = output.split("\n")
    keyindex = arr[3].split(" ")
    #Store the public key somewhere...
    public_key = keyindex[len(keyindex)-1]
    #Creates genesis file on the node
    os.system("geth --datadir ./data init ../blockpoa.json")
    os.chdir("../")
    os.chdir("bnode")
    #Starts the bootnode within bnode folder
    os.system('bootnode -nodekey "./boot.key" -verbosity 7 -addr "127.0.0.1:30301"')
    #Need to use applescript to create new terminal and run command
    
    os.chdir("../")

def create_node():
    res = input("Enter password")
    createNode(res)




#createNode()
create_node()