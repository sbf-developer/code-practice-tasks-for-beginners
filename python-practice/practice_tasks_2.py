# ============================================================
# Python Practice Tasks 2
# Write your solution below each task comment.
#
# Stuck? Write pseudocode first — plain-English steps of what your
# program should do. Once the logic makes sense, translate it into code.
#
# These tasks focus on NEW topics not covered in practice_tasks_1.py:
#   f-strings, subtraction, 3-way branching, elif chains,
#   countdown/reverse range, .split(), second-largest logic,
#   list transformation, word splitting, exponentiation,
#   substring search, string multiplication, two-pass problems,
#   digit manipulation, prime checking, interleaving lists,
#   percentage math, while-loop validation, game logic
# ============================================================


# --- Task 1: Greet by name ---
# Ask the user for their name and print "Hello, <name>!"
# Use an f-string: f"Hello, {name}!"
# Example: name = "Alex" -> Hello, Alex!


# --- Task 2: Difference of two numbers ---
# Ask the user for two numbers and print the first minus the second.
# Example: 10 and 3 -> 7


# --- Task 3: Positive, negative, or zero ---
# Ask the user for a number and print "Positive", "Negative", or "Zero".
# Use if / elif / else with three outcomes.


# --- Task 4: Letter grade ---
# Ask the user for a test score (0-100) and print the letter grade:
#   90-100 -> A
#   80-89  -> B
#   70-79  -> C
#   60-69  -> D
#   below 60 -> F
# Practice chaining several elif branches.


# --- Task 5: Countdown ---
# Ask the user for a positive integer n and print a countdown from n down to 1,
# one number per line.
# Example: n=5 -> 5, 4, 3, 2, 1
# Hint: range(n, 0, -1)


# --- Task 6: Count words ---
# Ask the user for a sentence and print how many words it contains.
# Example: "hello world python" -> 3
# Hint: sentence.split() splits a string into a list of words.


# --- Task 7: Second largest ---
# Given a list of numbers, find and print the second largest value.
# Use this list: numbers = [3, 17, 8, 42, 1, 9]
# Example result: 17
# Do not sort the list — use a loop.


# --- Task 8: Product of a list ---
# Given a list of numbers, compute and print the product (multiply all together).
# Use this list: numbers = [2, 3, 4]
# Example: 2 * 3 * 4 = 24


# --- Task 9: Power of a number ---
# Ask the user for a base and an exponent (two integers) and print base ** exponent.
# Example: base=2, exponent=10 -> 1024
# Hint: ** is Python's power operator.


# --- Task 10: Leap year check ---
# Ask the user for a year and print True if it is a leap year, otherwise False.
# Rules: divisible by 4 AND (not divisible by 100 OR divisible by 400).
# Examples: 2000 -> True, 1900 -> False, 2024 -> True
# Practice using and / or together.


# --- Task 11: Contains substring ---
# Ask the user for two strings: a sentence and a word.
# Print True if the word appears anywhere in the sentence, otherwise False.
# Example: sentence="I love Python", word="Python" -> True
# Hint: use the `in` keyword.


# --- Task 12: Star triangle ---
# Ask the user for a positive integer n and print a right triangle of stars
# with n rows.
# Example for n=4:
#   *
#   **
#   ***
#   ****
# Hint: "*" * 3 gives "***"


# --- Task 13: Count above average ---
# Given a list of test scores, count how many are above the average.
# Use this list: grades = [85, 92, 78, 90, 88]
# Print the count. (You need to compute the average first, then count.)


# --- Task 14: Double each value ---
# Given a list of integers, create a NEW list where every value is doubled.
# Use this list: values = [1, 2, 3, 4, 5]
# Print the result: [2, 4, 6, 8, 10]
# Hint: start with an empty list and use .append() inside a loop.


# --- Task 15: Longest word ---
# Given a sentence, find and print the longest word.
# Use this sentence: "the quick brown fox jumps"
# If two words tie for longest, print either one.
# Hint: use .split() to break the sentence into words.


# --- Task 16: Sum of digits ---
# Ask the user for a non-negative integer and print the sum of its digits.
# Example: 12345 -> 15 (1 + 2 + 3 + 4 + 5)
# Hint: convert to string and loop, OR use n % 10 to peel off digits.


# --- Task 17: Prime check ---
# Ask the user for an integer greater than 1 and print True if it is prime,
# otherwise False.
# A prime number is only divisible by 1 and itself.
# Examples: 7 -> True, 9 -> False, 2 -> True


# --- Task 18: Interleave two lists ---
# Given two lists of equal length, build a new list that alternates items.
# Use these lists: a = [1, 2, 3] and b = [4, 5, 6]
# Print the result: [1, 4, 2, 5, 3, 6]


# --- Task 19: Tip calculator ---
# Ask the user for a bill amount (float) and a tip percentage (integer).
# Calculate and print the tip amount and the total (bill + tip).
# Example: bill=100.0, tip=15 -> tip is 15.0, total is 115.0
# Use float() for the bill and round() if you want neat decimals.


# --- Task 20: Keep asking until valid ---
# Ask the user for their age. If they enter 0 or a negative number,
# ask again until they enter a positive number. Then print "Your age is <age>".
# Use a while loop that repeats until the input is valid.
