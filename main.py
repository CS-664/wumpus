'''
Import here
'''

def InitialBoard(txtName):
    fileObject = open(txtName, "r")
    data = fileObject.read()
    print(data)

def main():
    InitialBoard('BoardInfrom.txt')

if __name__ == "__main__":
    main()