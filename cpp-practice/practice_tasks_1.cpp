// ============================================================
// C++ Practice Tasks 1
// Write your solution below each task comment.
//
// Stuck? Write pseudocode first — plain-English steps of what your
// program should do. Once the logic makes sense, translate it into code.
//
// Compile and run:
//   g++ -std=c++17 practice_tasks_1.cpp -o practice_tasks_1
//   ./practice_tasks_1          (Linux / Mac)
//   practice_tasks_1.exe        (Windows)
//
// Common includes for these tasks:
//   #include <iostream>
//   #include <string>
//   #include <vector>
//   #include <map>       // Task 15 (word frequency)
//   #include <algorithm> // optional helpers (reverse, etc.)
//
// Cheatsheet vs Python:
//   print(x)              -> std::cout << x << std::endl;
//   input / int(input())  -> int n; std::cin >> n;
//   getline for sentences -> std::getline(std::cin, sentence);
//   len(list)             -> vec.size()
//   list.append(x)        -> vec.push_back(x)
//   word[::-1]            -> std::string(word.rbegin(), word.rend())
//   char in "aeiou"       -> std::string("aeiou").find(c) != std::string::npos
//   char.lower()          -> std::tolower(c)
//   range(1, n + 1)       -> for (int i = 1; i <= n; i++)
//   True / False          -> true / false
//   list literal          -> std::vector<int> nums = {3, 17, 8, 42, 1, 9};
// ============================================================


// --- Task 1: Hello ---
// Print "Hello, World!" to the console.


// --- Task 2: Sum two numbers ---
// Ask the user for two numbers and print their sum.


// --- Task 3: Even or odd ---
// Ask the user for an integer and print "Even" or "Odd".


// --- Task 4: FizzBuzz (single number) ---
// Ask for a number n. If n is divisible by 3, print "Fizz".
// If divisible by 5, print "Buzz". If divisible by both, print "FizzBuzz".
// Otherwise print the number itself.


// --- Task 5: Count to n ---
// Ask the user for a positive integer n and print numbers 1 through n,
// one per line.


// --- Task 6: Reverse a string ---
// Ask the user for a word and print it reversed.
// Example: "hello" -> "olleh"
// Hint: std::string reversed(word.rbegin(), word.rend());


// --- Task 7: Find the maximum ---
// Given a vector of numbers, find and print the largest one.
// Use this vector: std::vector<int> numbers = {3, 17, 8, 42, 1, 9};


// --- Task 8: Sum a vector ---
// Given a vector of numbers, compute and print the total.
// Use this vector: std::vector<int> numbers = {10, 20, 30, 40, 5};


// --- Task 9: Count vowels ---
// Ask the user for a sentence and count how many vowels (a, e, i, o, u) it contains.
// Ignore uppercase/lowercase.
// Hint: use std::tolower(c) and check against "aeiou"


// --- Task 10: Factorial ---
// Ask the user for a non-negative integer n and compute n! (factorial).
// Example: 5! = 5 * 4 * 3 * 2 * 1 = 120


// --- Task 11: Palindrome check ---
// Ask the user for a word and print true if it reads the same forwards
// and backwards, otherwise false.
// Example: "radar" -> true, "hello" -> false
// Hint: compare word with std::string(word.rbegin(), word.rend())


// --- Task 12: Multiplication table ---
// Ask the user for a number n and print its multiplication table from 1 to 10.
// Example for n=3:
//   3 x 1 = 3
//   3 x 2 = 6
//   ...


// --- Task 13: Average of grades ---
// Given a vector of test scores, compute and print the average.
// Use this vector: std::vector<int> grades = {85, 92, 78, 90, 88};
// Hint: use grades.size() for the count


// --- Task 14: Filter positives ---
// Given a vector of integers, create a new vector containing only the positive ones.
// Use this vector: std::vector<int> values = {-3, 7, 0, 12, -1, 5, -8};
// Print the result.
// Hint: use push_back() to add items to a new vector


// --- Task 15: Word frequency ---
// Given a sentence, count how many times each word appears.
// Use this sentence: "the cat and the dog and the bird"
// Print each word and its count.
// Hint: split words manually in a loop, or use std::istringstream.
//       std::map<std::string, int> counts; is useful for storing counts.


// --- Task 16: Guess the number ---
// Pick a secret number (e.g. 7). Let the user guess until they get it right.
// After each wrong guess, print "Too high" or "Too low".
// Hint: use a while loop that keeps asking until the guess is correct.


// --- Task 17: Fibonacci sequence ---
// Ask the user for n and print the first n numbers of the Fibonacci sequence.
// Example for n=7: 0, 1, 1, 2, 3, 5, 8


// --- Task 18: Remove duplicates ---
// Given a vector with duplicate values, return a new vector with duplicates removed.
// Use this vector: std::vector<int> items = {1, 2, 2, 3, 4, 4, 4, 5};
// Print the result (order does not matter).
// Hint: loop and push_back only if not already in the new vector,
//       or look up std::sort + std::unique (bonus topic!)


// --- Task 19: Celsius to Fahrenheit ---
// Ask the user for a temperature in Celsius and convert it to Fahrenheit.
// Formula: F = C * 9/5 + 32
// Hint: use double for decimal temperatures


// --- Task 20: Simple password check ---
// Ask the user for a password. It is valid if it has at least 8 characters
// and contains at least one digit. Print "Valid" or "Invalid".
// Hint: loop through characters and check std::isdigit(c)
