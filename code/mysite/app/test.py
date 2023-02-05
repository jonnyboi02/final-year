import os
def createNode():
    #os.chdir("../")
    #os.mkdir("../")
    print(os.getcwd(), "!")
    os.chdir("gethpoa")
    i = 1
    dir = "node"
    check = dir+str(i)
    while os.path.exists(""):
        check = dir+str(i)
        

    print(os.getcwd(), "!")

createNode()