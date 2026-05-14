# ============================================================
#  DecodeLabs Internship - Batch 2026
#  Project 1: The To-Do List
#  Developer: Fiza Zulfiqar
# ============================================================

# ----------------------------
# STORAGE: The Volatile Container
# my_tasks acts as our in-memory database (a list of dicts)
# Each dictionary = one row in a database table
# ----------------------------
my_tasks = []
task_id_counter = 1   # mimics an auto-increment PRIMARY KEY


# ----------------------------
# PROCESS: Add a task (INSERT INTO equivalent)
# Uses list.append() - O(1) amortized on the heap
# ----------------------------
def add_task(task_name):
    global task_id_counter

    # Each task is a dictionary -> maps to a database table row
    new_task = {
        "id":     task_id_counter,   # Primary Key
        "task":   task_name,         # Data column
        "status": "Pending"          # Extra column - good engineering habit
    }

    my_tasks.append(new_task)        # INSERT INTO tasks VALUES (...)
    task_id_counter += 1

    print(f"\n  Task added successfully -> '{task_name}'")


# ----------------------------
# OUTPUT: View all tasks (SELECT * FROM tasks)
# Uses enumerate() - the professional Pythonic way
# (avoids the old range(len(my_tasks)) anti-pattern)
# ----------------------------
def view_tasks():
    print("\n" + "=" * 45)
    print("         YOUR TO-DO LIST")
    print("=" * 45)

    if not my_tasks:
        print("  No tasks yet. Add something to get started!")
    else:
        # enumerate() gives us (index, value) simultaneously - no manual indexing
        for index, task in enumerate(my_tasks, start=1):
            status_icon = "v" if task["status"] == "Done" else "o"
            print(f"  {index}. [{status_icon}] (ID:{task['id']}) {task['task']}  |  {task['status']}")

    print("=" * 45)


# ----------------------------
# PROCESS: Mark a task as done
# ----------------------------
def mark_done(task_id):
    for task in my_tasks:
        if task["id"] == task_id:
            task["status"] = "Done"
            print(f"\n  Task ID {task_id} marked as Done!")
            return
    print(f"\n  No task found with ID {task_id}.")


# ----------------------------
# PROCESS: Delete a task
# ----------------------------
def delete_task(task_id):
    for task in my_tasks:
        if task["id"] == task_id:
            my_tasks.remove(task)
            print(f"\n  Task ID {task_id} deleted.")
            return
    print(f"\n  No task found with ID {task_id}.")


# ----------------------------
# VIEW: User Interface (the terminal menu)
# Decoupled from data logic - follows Model/View architecture shown in the PDF
# ----------------------------
def show_menu():
    print("\n" + "-" * 45)
    print("  DecodeLabs To-Do Manager")
    print("-" * 45)
    print("  1. Add a Task")
    print("  2. View All Tasks")
    print("  3. Mark Task as Done")
    print("  4. Delete a Task")
    print("  5. Exit")
    print("-" * 45)


# ----------------------------
# MAIN ENGINE - The Gatekeeper
# if __name__ == "__main__" ensures this only runs when executed directly
# (not when imported as a module - professional Python standard)
# ----------------------------
def main():
    print("\n  Welcome to DecodeLabs To-Do List App!")
    print("  Batch 2026 | Project 1")

    while True:
        show_menu()

        choice = input("  Enter your choice (1-5): ").strip()

        if choice == "1":
            task_name = input("  Enter task name: ").strip()
            if task_name:
                add_task(task_name)
            else:
                print("  Task name cannot be empty.")

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            view_tasks()
            try:
                tid = int(input("  Enter Task ID to mark as Done: "))
                mark_done(tid)
            except ValueError:
                print("  Please enter a valid number.")

        elif choice == "4":
            view_tasks()
            try:
                tid = int(input("  Enter Task ID to delete: "))
                delete_task(tid)
            except ValueError:
                print("  Please enter a valid number.")

        elif choice == "5":
            print("\n  Exiting... Remember: RAM is volatile. Data will be lost.")
            print("  (Next level: save tasks to a JSON file for persistence!)\n")
            break

        else:
            print("  Invalid choice. Please enter a number between 1 and 5.")


# The Gatekeeper - standard Python entry point
if __name__ == "__main__":
    main()
