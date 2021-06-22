import random

def play():
    user = input("What's your choice? 'r' for rock, 'p' for paper, 's' for scissors: ")
    computer = random.choice(['r','s','p'])
    display = computer

    if user == computer:
        print("It's a tie!")
        print(f"Computer choose {display}")

    if win(computer, user): 
        print("You lost!")
        print(f"Computer choose {display}")
        
    if win(user, computer): #how does the precedence matter? cos putting computer before user means the former has won
        print("You Won!")
        print(f"Computer choose {display}")

def win(player, computer):
    if(player == "r" and computer == "s" or player == "s" and computer == "p" or player == "p" and computer == "r"):
        return True

play()