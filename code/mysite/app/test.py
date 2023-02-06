import os
def createNode(password):
    #os.chdir("../")
    #os.mkdir("../")
    #print(os.getcwd(), "!")
    os.chdir("gethpoa")
    i = 1
    dir = "node"
    check = dir+str(i)
    while os.path.exists(check):
        i+=1
        check = dir+str(i)
    print(check)
    os.mkdir(check)
    os.chdir(check)
    #Creates textfile containing password to the node
    with open("password.txt", 'w') as f:
        f.write(password)

    #Running geth on a new node
    os.system("geth --datadir ./data account new --password password.txt")
    #Creates genesis file on the node
    os.system("geth --datadir ./data init ../blockpoa.json")
    #os.system("dir")
    os.chdir("../../")
    os.getcwd()
def create_node():
    res = input("Enter password")
    createNode(res)
#    return res

#createNode()
create_node()