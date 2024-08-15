# vanraj-demo
import os

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the menu
def display_menu():
    print("To-Do List Application")
    print("----------------------")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print()

# Function to view tasks
def view_tasks(tasks):
    clear_screen()
    print("Tasks:")
    if not tasks:
        print("No tasks.")
    else:
        for idx, task in enumerate(tasks, start=1):
            status = "Done" if task['completed'] else "Not Done"
            print(f"{idx}. {task['title']} - {task['description']} [{status}]")
    input("Press Enter to continue...")

# Function to add a task
def add_task(tasks):
    clear_screen()
    title = input("Enter task title: ")
    description = input("Enter task description (optional): ")
    tasks.append({'title': title, 'description': description, 'completed': False})
    print("Task added successfully!")
    input("Press Enter to continue...")

# Function to complete a task
def complete_task(tasks):
    clear_screen()
    view_tasks(tasks)
    try:
        task_num = int(input("Enter task number to complete: ")) - 1
        tasks[task_num]['completed'] = True
        print("Task marked as completed!")
    except (IndexError, ValueError):
        print("Invalid task number!")
    input("Press Enter to continue...")

# Function to delete a task
def delete_task(tasks):
    clear_screen()
    view_tasks(tasks)
    try:
        task_num = int(input("Enter task number to delete: ")) - 1
        del tasks[task_num]
        print("Task deleted successfully!")
    except (IndexError, ValueError):
        print("Invalid task number!")
    input("Press Enter to continue...")

# Main function
def main():
    tasks = []
    while True:
        clear_screen()
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




