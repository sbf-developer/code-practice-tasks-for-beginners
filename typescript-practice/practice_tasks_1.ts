// ============================================================
// TypeScript Practice Tasks 1
// Write your solution below each task comment.
//
// Stuck? Write pseudocode first — plain-English steps of what your
// program should do. Once the logic makes sense, translate it into code.
//
// Run: npx ts-node practice_tasks_1.ts
//
// For user input (like Python's input()), install readline-sync:
//   npm install readline-sync
//   npm install -D @types/readline-sync typescript ts-node
//
// Each task below has its own import line (like practicing alone).
// Only ONE import can be uncommented at a time — otherwise TypeScript
// shows red. When you start a new task, comment out the previous task's
// import and uncomment the new one.
//
//   import readlineSync from "readline-sync";
//   const n = parseInt(readlineSync.question("Insert a number: "));
//
// Cheatsheet vs Python:
//   print(x)           -> console.log(x)
//   int(x)             -> parseInt(x)  or Number(x)
//   float(x)           -> parseFloat(x)
//   len(arr)           -> arr.length
//   word[::-1]         -> word.split("").reverse().join("")
//   char in "aeiou"    -> "aeiou".includes(char)
//   char.lower()       -> char.toLowerCase()
//   list.append(x)     -> arr.push(x)
//   range(1, n + 1)    -> for (let i = 1; i <= n; i++)
// ============================================================


// --- Task 1: Hello ---
// Print "Hello, World!" to the console.
console.log("Hello, World!")

// --- Task 2: Sum two numbers ---
// Ask the user for two numbers and print their sum.

import readlineSync from "readline-sync";

const first = parseInt(readlineSync.question("First number: "));
const second = parseInt(readlineSync.question("Second number: "));
console.log(first + second);


// --- Task 3: Even or odd ---
// Ask the user for an integer and print whether it is "Even" or "Odd".

import readlineSync from "readline-sync";

const number = parseInt(readlineSync.question("Insert number here: "));
if (number % 2 === 0) {
    console.log("Even");
} else {
    console.log("Odd");
}



// --- Task 4: FizzBuzz (single number) ---
// Ask for a number n. If n is divisible by 3, print "Fizz".
// If divisible by 5, print "Buzz". If divisible by both, print "FizzBuzz".
// Otherwise print the number itself.

// import readlineSync from "readline-sync";




// --- Task 5: Count to n ---
// Ask the user for a positive integer n and print numbers 1 through n,
// one per line.


// --- Task 6: Reverse a string ---
// Ask the user for a word and print it reversed.
// Example: "hello" -> "olleh"
// Hint: word.split("").reverse().join("")


// --- Task 7: Find the maximum ---
// Given an array of numbers, find and print the largest one.
// Use this array: const numbers = [3, 17, 8, 42, 1, 9];


// --- Task 8: Sum an array ---
// Given an array of numbers, compute and print the total.
// Use this array: const numbers = [10, 20, 30, 40, 5];


// --- Task 9: Count vowels ---
// Ask the user for a sentence and count how many vowels (a, e, i, o, u) it contains.
// Ignore uppercase/lowercase.
// Hint: use .toLowerCase() and "aeiou".includes(char)


// --- Task 10: Factorial ---
// Ask the user for a non-negative integer n and compute n! (factorial).
// Example: 5! = 5 * 4 * 3 * 2 * 1 = 120


// --- Task 11: Palindrome check ---
// Ask the user for a word and print true if it reads the same forwards
// and backwards, otherwise false.
// Example: "radar" -> true, "hello" -> false


// --- Task 12: Multiplication table ---
// Ask the user for a number n and print its multiplication table from 1 to 10.
// Example for n=3:
//   3 x 1 = 3
//   3 x 2 = 6
//   ...


// --- Task 13: Average of grades ---
// Given an array of test scores, compute and print the average.
// Use this array: const grades = [85, 92, 78, 90, 88];
// Hint: use grades.length instead of len(grades)


// --- Task 14: Filter positives ---
// Given an array of integers, create a new array containing only the positive ones.
// Use this array: const values = [-3, 7, 0, 12, -1, 5, -8];
// Print the result.
// Hint: use .push() to add items to a new array


// --- Task 15: Word frequency ---
// Given a sentence, count how many times each word appears.
// Use this sentence: "the cat and the dog and the bird"
// Print each word and its count.
// Hint: sentence.split(" ") gives you an array of words.
//       A Record<string, number> or plain object works as a counter map.


// --- Task 16: Guess the number ---
// Pick a secret number (e.g. 7). Let the user guess until they get it right.
// After each wrong guess, print "Too high" or "Too low".
// Hint: use a while loop that keeps asking until the guess is correct.


// --- Task 17: Fibonacci sequence ---
// Ask the user for n and print the first n numbers of the Fibonacci sequence.
// Example for n=7: 0, 1, 1, 2, 3, 5, 8


// --- Task 18: Remove duplicates ---
// Given an array with duplicate values, return a new array with duplicates removed.
// Use this array: const items = [1, 2, 2, 3, 4, 4, 4, 5];
// Print the result (order does not matter).
// Hint: [...new Set(items)] removes duplicates (bonus topic!)


// --- Task 19: Celsius to Fahrenheit ---
// Ask the user for a temperature in Celsius and convert it to Fahrenheit.
// Formula: F = C * 9/5 + 32


// --- Task 20: Simple password check ---
// Ask the user for a password. It is valid if it has at least 8 characters
// and contains at least one digit. Print "Valid" or "Invalid".
// Hint: use a loop or .match(/\d/) to check for a digit
