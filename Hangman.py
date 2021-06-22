import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words) #choice chooses a random word from a list
    while '-' in word or ' ' in words:
        word = random.choice(words)

    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word) #letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set() #what the user has guessed

    lives = 6

    #getting user input
    while len(word_letters) > 0:
        #letters used
        #' '.join(['a', 'b', 'cd']) --> 'a b cd '. The .join() converts words in a list into a string that is seperated by whatever is put before the .join. E.g: " ".join() 
        print('You have', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))
        
        #what current word is (ie W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))
    
        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters: #if a letter in alphabet that hasn't been used yet. I think that's what the minus sign means.
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                # print("Yay, you guessed the word," word)
            else:
                lives = lives - 1 #takes away a life if wrong
                print('Letter is not in word.')

        elif user_letter in used_letters:
            print('You have already used that character. Please try again.')

        else: 
            print('Invalid character. Please try again.')
#gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print('You died, sorry. The word was', word)
        return None
    else:
        print("Yay, you guessed the word", word, "!!")

hangman()

# user_input = input("Type something: ")
# print(user_input)

#Definitely fix that error of lives exceeding to -5
'''
Challenge!!!!
    try making it a gui??
'''