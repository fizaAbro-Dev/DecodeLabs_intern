# ============================================
#   DecodeLabs Internship - Batch 20263
#   PROJECT 4: The General Knowledge Quiz
#   Developer: Fiza Zulfiqar
# ============================================

# --- STORAGE: This variable keeps track of the score ---
score = 0

print("=============================")
print("  Welcome to the Quiz Game!  ")
print("=============================")
print()

# -------------------------------------------------------
# QUESTION 1
# -------------------------------------------------------
print("Question 1: What is the capital of France?")

answer1 = input("Your answer: ")   # INPUT: get raw text from user

# .strip()  → removes extra spaces (e.g. "  paris  " becomes "paris")
# .lower()  → converts to lowercase so "Paris" == "PARIS" == "paris"
answer1 = answer1.strip().lower()

# PROCESS: check if the answer is correct
if answer1 == "paris":
    print("✅ Correct! +1 point")
    score = score + 1          # increase score by 1
else:
    print("❌ Wrong! The correct answer is: Paris")

print()  # blank line for spacing

# -------------------------------------------------------
# QUESTION 2
# -------------------------------------------------------
print("Question 2: What is the largest planet in our Solar System?")

answer2 = input("Your answer: ")
answer2 = answer2.strip().lower()   # sanitize the input

if answer2 == "jupiter":
    print("✅ Correct! +1 point")
    score = score + 1
else:
    print("❌ Wrong! The correct answer is: Jupiter")

print()

# -------------------------------------------------------
# QUESTION 3
# -------------------------------------------------------
print("Question 3: How many sides does a hexagon have?")

answer3 = input("Your answer: ")
answer3 = answer3.strip().lower()   # sanitize the input

# The user might type "6" or "six" — we accept both!
if answer3 == "6" or answer3 == "six":
    print("✅ Correct! +1 point")
    score = score + 1
else:
    print("❌ Wrong! The correct answer is: 6 (six)")

print()

# -------------------------------------------------------
# OUTPUT: Print the final score at the end
# -------------------------------------------------------
print("=============================")
print(f"  Quiz Over! Your score: {score}/3")
print("=============================")

# Give a message based on score (if/elif/else)
if score == 3:
    print("🏆 Perfect score! Amazing job!")
elif score == 2:
    print("👍 Great work! So close to perfect!")
elif score == 1:
    print("📚 Keep practicing, you'll get there!")
else:
    print("💪 Don't give up! Try again!")