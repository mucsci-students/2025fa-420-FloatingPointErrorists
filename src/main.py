from enum import Enum
import faculty

class Options(Enum):
    Faculty = faculty.faculty()

def printmenu():
    print("Options:")
    print("A) Faculty\nB) Courses\nC) Rooms/Labs")
    print("Enter Q to quit (this will not save current changes)")

def main():
    print("Hello welcome to the scheduler config compiler!!!!")
    printmenu()
    chosenOption = input("Choose an option> ")
    chosenOption = chosenOption.lower()
    while not chosenOption == "q":
        printmenu()
        chosenOption = input("Choose an option> ")

main()


