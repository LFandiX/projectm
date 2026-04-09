# Import library
import random 
# Input Jumlah data
while True:
    maximum_data = 5 
    number_of_word = int(input(f"Enter number of word (maximum data: {maximum_data}): "))
    if number_of_word > maximum_data:
        print("Your had exceed the limit, Choose another number less than 5!")
    else: 
        break 

# Input data satu per satu
def get_word(number_of_words):
    word_list = []
    for data_number in range(number_of_words):
        data = input(f"Input word {data_number + 1}: ").lower()
        while data in word_list or data.isalpha() == False:
            print ("Please input diffrent word!")
            data = input(f"Input word {data_number + 1}: ").lower()
        word_list.append(data)
    return word_list
# word_list = get_word(number_of_word)
word_list = ['Cendrawasih','angrek']

#Visual Hangman
def hangman_visual(attempt):
    if attempt == 6:
                            print ('''
    ___
    |
    ''' )
    else:
        if attempt == 5:
            print ('''
    ___
    |
    O
    ''')
        else:
            if attempt == 4:
                print ('''
    ___
    |
    O
    |
    |
    ''')
            else:
                if attempt == 3:
                    print ('''
    ___
    |
    O
   /|
    |
    ''')
                else:
                    if attempt == 2:
                        print ('''
    ___
    |
    O
   /|\\
    | 
    ''')
                    else:
                        if attempt == 1:
                            print ('''
    ___
    |
    O
   /|\\
    |
   / 
    ''')

# Memastikan bahwa kata masih ada untuk dimainkan
total_word = len(word_list)
while total_word > 0:
    word_selected = word_list[random.randint(0,total_word-1)]

# Hangman
    word_selected = word_selected.lower()
    true_guesses = set()
    false_guesses = set()
    attempt = 7

    while attempt > 0:
        gueseed_word = ""
        for character in word_selected:
            if character in true_guesses:
                gueseed_word += character
            else: 
                gueseed_word += "_"
        print ("Guessed Word:" + gueseed_word)

        player_guessed = input ("Input a Char: ").lower()
        player_guessed = player_guessed[0]

        if player_guessed.isalpha():
            if player_guessed in true_guesses or player_guessed in false_guesses:
                print ("You had gueess this Letter!")
            else: 
                if player_guessed in word_selected:
                    true_guesses.add(player_guessed)
                    if set(true_guesses) == set(word_selected):
                        print ("Congratulations! You Win, Word:" + word_selected)
                        word_list.remove(word_selected)
                        total_word-=1
                        break
                    
                else:
                    attempt -= 1
                    false_guesses.add(player_guessed)
                    hangman_visual(attempt)
        else:
            print ("Please input a Alphabet!")
    if attempt == 0:
        print ('''
    ___
    |
    O
   /|\\
    |
   / \\
''')
        print ("GameOver, word is", word_selected)
        word_list.remove(word_selected)
        total_word -= 1





