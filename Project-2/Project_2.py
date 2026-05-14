# ================================
# DecodeLabs Internship - Batch 2026
# Project 2: Expense Tracker
# Developer: Fiza Zulfiqar
# ================================


# ----------------------------
# STORAGE
# This list stores all expense records (like a database table)
# Each expense is a dictionary - same concept as Project 1
# ----------------------------
expenses = []

# ----------------------------
# total = 0 means: our running total starts at zero
# ----------------------------
total = 0


# ----------------------------
# INPUT FUNCTION - "THE GATE"
# input() always gives us a STRING like "100"
# We MUST convert it to int using int() for math to work
# '100' + '50' = '10050'  <-- DISASTER (string joining)
# int('100') + int('50') = 150  <-- TRUTH (real math)
# ----------------------------
def get_expense():

    # If user types 'done', we stop the loop
    # If user types a number, we add it to total
    user_input = input("Enter expense amount (or type 'done' to finish): ")

    # Check if user wants to stop - this is the Sentinel Value
    if user_input == "done":
        return "done"

  
    # try: attempt to convert input to a number
    # except ValueError: if user types "ten" instead of "10", catch the error
    # This prevents the program from crashing - called error-proofing
    try:
        # THE GATEKEEPER: int() converts String "100" -> Integer 100
        # Without int(), Python treats "100" as text, not a number
        expense_amount = int(user_input)

        # Make sure the number is positive (extra validation)
        if expense_amount <= 0:
            print("Please enter a number greater than zero.")
            return None

        return expense_amount

    except ValueError:
        # If user typed something like "abc" or "ten"
        # ValueError is caught here so the program does NOT crash
        print("Invalid input! Please enter a number like 100 or 50.")
        return None


# ----------------------------
# PROCESS FUNCTION - "THE ENGINE"
# This adds the new expense to our list and updates the total
# total += new_expense means: total = total + new_expense
# This is the core of all financial software
# ----------------------------
def add_expense(amount):

    # Make total accessible inside this function
    global total

    # Store expense as a dictionary (same as Project 1 - row in a table)
    expense_record = {
        "id"    : len(expenses) + 1,   # Auto ID (Primary Key)
        "amount": amount               # The actual amount
    }

    # Add to our expenses list (like INSERT INTO in a database)
    expenses.append(expense_record)

    
   
    # total starts at 0, then grows with each expense
    # Example: 0 + 100 = 100, then 100 + 50 = 150, then 150 + 20 = 170
    total = total + amount
    # Same as writing: total += amount

    print("Expense of", amount, "added! Running total:", total)


# ----------------------------
# OUTPUT FUNCTION - "THE DISPLAY"
# The math happens in add_expense(), display happens here separately
# Final output shows: FINAL TOTAL: $150.00 
# ----------------------------
def show_summary():

    print("\n" + "=" * 40)
    print("       EXPENSE SUMMARY")
    print("=" * 40)

    # If no expenses were added
    if len(expenses) == 0:
        print("No expenses recorded.")
    else:
        # Loop through all recorded expenses and display them
        for expense in expenses:
            print("  ID:", expense["id"], "  |  Amount:", expense["amount"])

    print("-" * 40)

    # Display the final total - this is the OUTPUT phase of IPO
    # Shown in PDF as: FINAL TOTAL: $150.00
    print("  FINAL TOTAL SPENT:", total)
    print("=" * 40)


# ----------------------------
# MAIN FUNCTION - THE CONTINUOUS AUDIT LOOP
# It only stops when user types 'done' (The Kill Switch / Sentinel Value)
# This is the core engine of the program
# ----------------------------
def main():

    print("\nWelcome to DecodeLabs Expense Tracker!")
    print("Batch 2026 | Project 2")
    print("Type a number to add expense. Type 'done' to finish.\n")

        # This loop keeps asking for expenses until the Kill Switch is triggered
    while True:

        # PHASE 1: INPUT - Get data from user (The Gate)
        result = get_expense()

        # THE KILL SWITCH activated - user typed 'done' (Sentinel Value)
        # break stops the while True loop gracefully
        if result == "done":
            break

        # If input was invalid (None returned), skip and ask again
        if result is None:
            continue

        # PHASE 2: PROCESS - Add expense and update total (The Engine)
        add_expense(result)

    # PHASE 3: OUTPUT - Show the final summary (The Display)
    # This runs AFTER the loop ends (after user types 'done')
    show_summary()

    print("\nGoodbye! Remember: This data lives in RAM.")
    print("Next level: Save to a file for persistence!")


# ----------------------------
# THE GATEKEEPER ENTRY POINT
# if __name__ == "__main__" means:
# Only run main() if we directly run this file
# (Same concept used in Project 1)
# ----------------------------
if __name__ == "__main__":
    main()