# ============================================================
# Python Practice Tasks
# Write your solution below each task comment.
# ============================================================


# --- Task 1: Hello ---
# Print "Hello, World!" to the console.
print("Hello, World!")



# --- Task 2: Sum two numbers ---
# Ask the user for two numbers and print their sum.

first_number = int(input("First number: "))
second_number = int(input("Second number: "))

print(first_number + second_number)


# --- Task 3: Even or odd ---
# Ask the user for an integer and print whether it is even or odd.

number = int(input("Insert a random number here: "))

if number % 2 == 0:
    print("Even")
else:
    print("Odd")


# --- Task 4: FizzBuzz (single number) ---
# Ask for a number n. If n is divisible by 3, print "Fizz".
# If divisible by 5, print "Buzz". If divisible by both, print "FizzBuzz".
# Otherwise print the number itself.

number = int(input("Insert a number here: "))

if number % 3 == 0 and number % 5 == 0:
    print("FizzBuzz")
elif number % 3 == 0:
    print("Fizz")
elif number % 5 == 0:
    print("Buzz")
else:
    print(number)


# --- Task 5: Count to n ---
# Ask the user for a positive integer n and print numbers 1 through n,
# one per line.

n=0
while n <= 0:
    n = int(input("Insert a number: "))

for i in range(1, n + 1):
    print (i)


# --- Task 6: Reverse a string ---
# Ask the user for a word and print it reversed.
# Example: "hello" -> "olleh"

word = input("Insert a word: ")
print(word[::-1])


# --- Task 7: Find the maximum ---
# Given a list of numbers, find and print the largest one.
# Use this list: numbers = [3, 17, 8, 42, 1, 9]



# --- Task 8: Sum a list ---
# Given a list of numbers, compute and print the total.
# Use this list: numbers = [10, 20, 30, 40, 5]



# --- Task 9: Count vowels ---
# Ask the user for a sentence and count how many vowels (a, e, i, o, u) it contains.
# Ignore uppercase/lowercase.



# --- Task 10: Factorial ---
# Ask the user for a non-negative integer n and compute n! (factorial).
# Example: 5! = 5 * 4 * 3 * 2 * 1 = 120



# --- Task 11: Palindrome check ---
# Ask the user for a word and print True if it reads the same forwards
# and backwards, otherwise False.
# Example: "radar" -> True, "hello" -> False



# --- Task 12: Multiplication table ---
# Ask the user for a number n and print its multiplication table from 1 to 10.
# Example for n=3:
#   3 x 1 = 3
#   3 x 2 = 6
#   ...



# --- Task 13: Average of grades ---
# Given a list of test scores, compute and print the average.
# Use this list: grades = [85, 92, 78, 90, 88]



# --- Task 14: Filter positives ---
# Given a list of integers, create a new list containing only the positive ones.
# Use this list: values = [-3, 7, 0, 12, -1, 5, -8]
# Print the result.



# --- Task 15: Word frequency ---
# Given a sentence, count how many times each word appears.
# Use this sentence: "the cat and the dog and the bird"
# Print each word and its count.



# --- Task 16: Guess the number ---
# Pick a secret number (e.g. 7). Let the user guess until they get it right.
# After each wrong guess, print "Too high" or "Too low".



# --- Task 17: Fibonacci sequence ---
# Ask the user for n and print the first n numbers of the Fibonacci sequence.
# Example for n=7: 0, 1, 1, 2, 3, 5, 8



# --- Task 18: Remove duplicates ---
# Given a list with duplicate values, return a new list with duplicates removed.
# Use this list: items = [1, 2, 2, 3, 4, 4, 4, 5]
# Print the result (order does not matter).



# --- Task 19: Celsius to Fahrenheit ---
# Ask the user for a temperature in Celsius and convert it to Fahrenheit.
# Formula: F = C * 9/5 + 32



# --- Task 20: Simple password check ---
# Ask the user for a password. It is valid if it has at least 8 characters
# and contains at least one digit. Print "Valid" or "Invalid".
