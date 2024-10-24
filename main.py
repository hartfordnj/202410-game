import os
import random

def clear_screen():
    # Clears the terminal screen for a clean UI
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ui(round_number, enemy_name, bookbag, current_guess, guess_history, correct_letters, incorrect_letters, debug_answer=None):
    # Clear the screen each time before displaying the UI
    clear_screen()
    
    # Display round and enemy
    print(f"Round {round_number} - {enemy_name}")
    print("Bookbag:")
    for book, status in bookbag.items():
        print(f"[{status or 'NOPE!'}] {book}")
    if not bookbag:
        print("[empty]")
    print()

    # Display debug information if debug_answer is provided
    if debug_answer:
        print(f"DEBUG: {debug_answer}\n")

    # Current guess
    print(f"Current Guess:")
    print(' '.join(current_guess) + "\n")

    # Guess history
    for guess in guess_history:
        print(' '.join(guess))
    print()

    # Correct letters
    print("Correct: " + (', '.join(sorted(set(correct_letters))) if correct_letters else "[none]"))

    # Incorrect letters
    print("Incorrect: " + (', '.join(sorted(set(incorrect_letters))) if incorrect_letters else "[none]"))

    # Guess prompt
    player_guess = input("Guess: ")
    return player_guess

# Define a word bank for each difficulty category with 5-letter words
easy_words = ["brick", "chart", "habit", "blank", "fight", "light", "lemon", "apple", "beach", "grape", "plant", "storm", "candy", "drink", "paper", "flame", "store", "party", "chair", "taste", "bread", "shiny", "water", "smile"]
medium_words = ["stoop", "check", "leaky", "spool", "trace", "frank", "crisp", "brisk", "plumb", "sheep", "grasp", "flock", "spear", "cloak", "crave", "blink", "flint", "proud", "stark", "shrub", "brace", "flour", "plume", "whisk"]
hard_words = ["realm", "haste", "lapse", "clamp", "knack", "glyph", "prank", "shrew", "wince", "quilt", "pivot", "flair", "quash", "brine", "scorn", "twist", "crisp", "wharf", "fluke", "mourn", "slant"]
expert_words = ["azure", "plumb", "fjord", "glyph", "wrath", "quoth", "whisk", "sword", "whale", "scalp", "fluke", "mirth", "snarl", "crust", "blurt", "quack", "slink", "quilt", "wrist", "squib", "flint", "shard", "blimp", "crave"]
legendary_words = ["nymph", "glyph", "sphinx", "joust", "fjord", "quark", "wharf", "zilch", "flask", "gnash", "knave", "tryst", "whorl", "lynch", "crust", "plumb", "sworn", "whisk", "blitz", "quill", "shirk", "quaff", "wrung"]

enemies = {
    "Chump": {"easy": 30, "medium": 40, "hard": 30},
    "Bully": {"easy": 20, "medium": 50, "hard": 30},
    "Thug": {"medium": 20, "hard": 50, "expert": 30},
    "Greaser": {"hard": 30, "expert": 50, "legendary": 20},
    "Don": {"expert": 40, "legendary": 60}
}

# Function to select a word based on difficulty distribution
def select_word(enemy_name):
    difficulty_weights = enemies[enemy_name]
    difficulties = list(difficulty_weights.keys())
    weights = list(difficulty_weights.values())
    chosen_difficulty = random.choices(difficulties, weights=weights, k=1)[0]
    
    if chosen_difficulty == "easy":
        return random.choice(easy_words)
    elif chosen_difficulty == "medium":
        return random.choice(medium_words)
    elif chosen_difficulty == "hard":
        return random.choice(hard_words)
    elif chosen_difficulty == "expert":
        return random.choice(expert_words)
    elif chosen_difficulty == "legendary":
        return random.choice(legendary_words)

# Function to select a book after winning a round
def choose_book():
    books = [
        "BOOK: First Position - 4 in 10 chance FIRST letter is revealed", 
        "BOOK: Last Position - 4 in 10 chance LAST letter is revealed", 
        "BOOK: Middle Position - 4 in 10 chance MIDDLE letter is revealed",
        "BOOK: Spot Vowel - 4 in 10 chance a vowel will be revealed"
    ]
    # Exclude books that are already in the bookbag
    available_books = [book for book in books if book not in bookbag]
    if len(available_books) >= 2:
        chosen_books = random.sample(available_books, 2)  # Player gets to choose between two books
    elif len(available_books) == 1:
        chosen_books = available_books  # Only one book available to choose
    else:
        chosen_books = []  # No books available
    return chosen_books

# Initial game setup
print("Welcome to GAME")
start_game = input("Start Game: Y / N\n").strip().lower()
if start_game != 'y':
    print("Game not started.")
    exit()

debug_mode = input("Debug Mode: Y / N\n").strip().lower() == 'y'

# Set up enemy distribution for 8 rounds
enemy_sequence = ["Chump", "Chump", "Bully", "Bully", "Thug", "Thug", "Greaser", "Don"]
round_number = 1
bookbag = {}

guessed_letters = set()
correct_letters = []
incorrect_letters = []

# Loop through 8 rounds
def game_loop():
    global round_number, guessed_letters, correct_letters, incorrect_letters
    for enemy_name in enemy_sequence:
        # Reset correct and incorrect letters at the beginning of each round
        correct_letters = []
        incorrect_letters = []
        guessed_letters.clear()

        current_guess = ['_'] * 5
        guess_history = [['_', '_', '_', '_', '_'] for _ in range(6)]

        # Select the answer for the current enemy
        debug_answer = select_word(enemy_name)

        # Trigger book effects before the round
        for book in bookbag.keys():
            if "BOOK: Spot Vowel" in book:
                vowels = [ch for ch in debug_answer if ch in 'aeiou']
                if vowels and random.randint(1, 10) <= 4:  # 4 in 10 chance
                    revealed_vowel = random.choice(vowels).upper()
                    correct_letters.append(revealed_vowel)
                    bookbag[book] = "YES!"
                else:
                    bookbag[book] = "NOPE"
            if "BOOK: Position 1" in book:
                if random.randint(1, 10) <= 4:  # 4 in 10 chance
                    current_guess[0] = debug_answer[0].upper()
                    bookbag[book] = "YES!"
                else:
                    bookbag[book] = "NOPE"
            elif "BOOK: Last Position" in book:
                if random.randint(1, 10) <= 4:  # 4 in 10 chance
                    current_guess[-1] = debug_answer[-1].upper()
                    bookbag[book] = "YES!"
                else:
                    bookbag[book] = "NOPE"
            elif "BOOK: Middle Position" in book:
                if random.randint(1, 10) <= 4:  # 4 in 10 chance
                    middle_index = len(current_guess) // 2
                    current_guess[middle_index] = debug_answer[middle_index].upper()
                    bookbag[book] = "YES!"
                else:
                    bookbag[book] = "NOPE"

        # Display UI for each round (with debug mode option)
        while True:
            player_guess = display_ui(round_number, enemy_name, bookbag, current_guess, guess_history, correct_letters, incorrect_letters, debug_answer if debug_mode else None)
            
            if len(player_guess) != len(current_guess):
                print("Invalid guess length. Try again.\n")
                continue
            
            # Maintain correct and incorrect letters across all guesses in the round
            round_correct_letters = set(correct_letters)
            round_incorrect_letters = set(incorrect_letters)
            
            # Update guessed letters
            guessed_letters.update(player_guess.lower())
            
            # Update guess history with the player's guess
            for i in range(len(guess_history)):
                if guess_history[i] == ['_', '_', '_', '_', '_']:
                    guess_history[i] = list(player_guess.upper())
                    break
            
            # Update current guess based on correct positions only
            for i, letter in enumerate(player_guess.lower()):
                if letter == debug_answer[i].lower():
                    current_guess[i] = letter.upper()
                    round_correct_letters.add(letter)
                else:
                    round_incorrect_letters.add(letter)
            
            # Update correct and incorrect letters
            correct_letters = [letter.upper() for letter in round_correct_letters]
            incorrect_letters = [letter.upper() for letter in round_incorrect_letters]

            # Check win condition
            if ''.join(current_guess).lower() == debug_answer.lower():
                clear_screen()
                print(f"Congratulations! You've defeated {enemy_name} in Round {round_number}!")
                
                # Offer a book reward
                new_books = choose_book()
                if len(new_books) == 2:
                    print(f"""Choose your reward:
1) {new_books[0]}
2) {new_books[1]}""")
                    choice = input("Enter 1 or 2 to choose your book: ").strip()
                    if choice == '1':
                        bookbag[new_books[0]] = ""
                    elif choice == '2':
                        bookbag[new_books[1]] = ""
                elif len(new_books) == 1:
                    print(f"You have received: {new_books[0]}")
                    bookbag[new_books[0]] = ""
                else:
                    print("No books available to choose.")
                
                # Offer to replace a book if the bookbag is full
                if len(bookbag) >= 5:
                    print("Your Bookbag is full! Choose a book to remove to add a new one.")
                    new_books = choose_book()
                    if new_books:
                        print(f"""New Books Available:
1) {new_books[0]}""" + (f"\n2) {new_books[1]}" if len(new_books) > 1 else ""))
                        book_to_remove = input("Enter the name of the book to remove or 'none' to skip: ")
                        if book_to_remove in bookbag:
                            del bookbag[book_to_remove]
                            choice = input("Enter 1 or 2 to choose your new book: ").strip()
                            if choice == '1':
                                bookbag[new_books[0]] = ""
                            elif choice == '2' and len(new_books) > 1:
                                bookbag[new_books[1]] = ""
                
                break
            elif all(guess != ['_', '_', '_', '_', '_'] for guess in guess_history):
                clear_screen()
                print(f"Game over! You've lost to {enemy_name} in Round {round_number}.")
                return
        round_number += 1

# Start game loop
game_loop()
print("You've completed the game! Great job!")
