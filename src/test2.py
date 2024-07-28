try:
    import random
except ModuleNotFoundError:
    print("The 'random' module is not installed. Please install it using 'pip install random'.")
    exit(1)

def high_low_game():
    print("Welcome to the High-Low Game!")
    number_to_guess = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            guess = int(input("Guess a number between 1 and 100: "))
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("Please guess a number within the range.")
            elif guess < number_to_guess:
                print("Higher!")
            elif guess > number_to_guess:
                print("Lower!")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

high_low_game()

# 홀수 짝수 판별하는 함수
def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False
