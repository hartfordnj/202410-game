import os

def clear_screen():
    # Clears the terminal screen for a clean UI
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ui(round_number, enemy_name, bookbag, current_guess, guessed_letters, guess_history, debug_answer=None):
    # Clear the screen each time before displaying the UI
    clear_screen()
    
    # Display round and enemy
    print(f"Round {round_number} - {enemy_name}")
    print(f"Bookbag: {', '.join(bookbag) if bookbag else '[empty]'}\n")

    # Display debug information if debug_answer is provided
    if debug_answer:
        print(f"DEBUG: {debug_answer}\n")

    # Current guess
    print(f"Current Guess:")
    print(' '.join(current_guess) + "\n")

    # Keyboard
    keyboard_lines = [
        "Q W E R T Y U I O P",
        "A S D F G H J K L",
        "Z X C V B N M"
    ]
    for line in keyboard_lines:
        line_chars = line.split()
        print(' '.join([char if char.lower() not in guessed_letters else '_' for char in line_chars]))
    print("\n")

    # Guess history
    print("Guess History:")
    for guess in guess_history:
        print(' '.join(guess))
    print("\n")

    # Guess prompt
    player_guess = input("Guess: ")
    return player_guess

# Initial game setup
print("Welcome to GAME")
start_game = input("Start Game: Y / N\n").strip().lower()
if start_game != 'y':
    print("Game not started.")
    exit()

debug_mode = input("Debug Mode: Y / N\n").strip().lower() == 'y'
debug_answer = "PLUMB" if debug_mode else None

# Mocked data for initial display
round_number = 1
enemy_name = "Grunt"
bookbag = []
current_guess = ['_'] * 5
guessed_letters = set()
guess_history = [['_', '_', '_', '_', '_'] for _ in range(6)]

# Display UI for the first round (with debug mode option)
while True:
    player_guess = display_ui(round_number, enemy_name, bookbag, current_guess, guessed_letters, guess_history, debug_answer)
    
    if len(player_guess) != len(current_guess):
        print("Invalid guess length. Try again.\n")
        continue
    
    # Update guessed letters
    guessed_letters.update(player_guess.lower())
    
    # Update guess history with the player's guess
    for i in range(len(guess_history)):
        if guess_history[i] == ['_', '_', '_', '_', '_']:
            guess_history[i] = list(player_guess.upper())
            break
    
    # Update current guess based on correct letters
    for i, letter in enumerate(player_guess.lower()):
        if debug_answer and debug_answer[i].lower() == letter:
            current_guess[i] = letter.upper()

    # Check win condition
    if '_' not in current_guess:
        clear_screen()
        print("Congratulations! You've guessed the word!")
        break
    elif all(guess != ['_', '_', '_', '_', '_'] for guess in guess_history):
        clear_screen()
        print("Game over! You've used all your guesses.")
        break