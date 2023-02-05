import os

print(os.getlogin())

print(os.getcwd())


def createNode():
    os.chdir("../")
    #os.mkdir("../")
    print(os.getcwd())

createNode()