from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass
import json

to_do_list = []
next_id = 1
status_list = ["done", "todo", "in-progress"]

print("--------- To-Do List ------------")
current_time = datetime.now(timezone.utc)
print(f"Date: {current_time} \n")


# create a class task
@dataclass
class Task:
    id: int 
    description: str 
    status: str 
    createdAt: datetime 
    updatedAt: datetime 

def main():
    #menu 
    class menu(Enum):
        ADD = 0
        UPDATE = 1
        DELETE = 2
        LIST = 3
        STATUS_MARKING = 4
    
    # call to load the JSON file
    global next_id
    load_json(to_do_list)
    # taking the max id + 1 to prevent the program resuse the old id as the program reset to next_id = 1 everytime 
    next_id = max((task.id for task in to_do_list), default=0) + 1

    while True: 

        for choice in menu:
            print(f"{choice.value+1}. {choice.name.title()}")

        while True: 
            try: 
                user_choice = int(input(f"\nEnter your choice[1-{len(menu)}]: "))
                if 1 <= user_choice <= len(menu):
                    break
                else:
                    raise ValueError
            except ValueError as e:
                print(f"\nPlease enter an option [1-{len(menu)}] as number! Error: {e}")


        match(user_choice):
            case 1: 
                add_task()
                save_to_json(to_do_list)
            case 2: 
                update_task()
                save_to_json(to_do_list)
            case 3:
                delete_task()
                save_to_json(to_do_list)
            case 4:
                list_task()
            case 5:
                task_status_marking()
                save_to_json(to_do_list)
            case _:
                print(f"Please enter an integer for menu option[1-{len(menu)}]")
        
        end_loop = input("\nDo you want to continue?[Y/N]  ").strip().lower()
        
        if (end_loop == "no") or (end_loop == "n"):
            break


# take the description from user then create the Task object
def task_creation(task_description: str):
    task_creation_time = datetime.now(timezone.utc)
    new_task = Task(next_id, task_description, "todo", task_creation_time, task_creation_time )
    return new_task

# Add task 
def add_task():
    global next_id
    print("\nEnter your task description: ")
    while True:
        new_description = input().strip()
        
        if new_description == "":
            break
        new_task = task_creation(new_description)
        next_id += 1

        to_do_list.append(new_task)
    print("Tasks successfully added!\n")

# Use the id to find the matching task to update 
def matching_task():
    for task in to_do_list:
        print(f"{task.id}. {task.description}")
    
    try:    
        task_to_find = int(input("\nEnter the id of the task: "))
        
    except ValueError as e:
        print(f"Please only use a whole number for the task id! Error: {e}")
        return None
    
    else:  
        for task in to_do_list:
            if task_to_find == task.id :
                print("\nFound the matching task\n")
                return task
                    
    print("No matching task found")
    return None

# function to change the status of the task
def task_status_marking():
    task = matching_task()
    if task is None:
        return
    
    while True: 
        new_task_status = input(f"\nEnter new status of the task:[{"/".join(status_list)}] ").strip().lower()
        if new_task_status in status_list:
            task.status = new_task_status
            task.updatedAt = datetime.now(timezone.utc)
            return
        else:
            print("Please enter a valid status!")
            
            
# update function
def update_task():
    task_to_update = matching_task()
    if task_to_update is None:
        return
    
    while True: 
        description_to_update = input("\nEnter new description to update: ").strip()
        
        if description_to_update != "":
            task_to_update.description = description_to_update
            task_to_update.updatedAt = datetime.now(timezone.utc)
            print("Successfully updated the task!")
            return
        
        else:
            print("Please enter a valid description!")
    

# delete function
def delete_task():       
    task_to_delete = matching_task()
    if task_to_delete is None:
        return
    
    to_do_list.remove(task_to_delete)
    print("Successfully deleted the task!")
    

    
# Finding task with matching status: 
def found_matching_task_status(list_to_find: list, menu_option: int):
    found_matching_status = False
    if menu_option == 1:
        for task in list_to_find:
            print(f"\n{task.description.title()}(Id: {task.id})")
            found_matching_status = True
            
    else:
        for task in list_to_find:
            if task.status == status_list[menu_option-2]:
                print(f"\n{task.description}(Id: {task.id})")
                found_matching_status = True
    
    if not found_matching_status:
        print("No tasks found")
        return None
    
# list_task function 

def list_task():
    print("\n------Type of Task -------")
    print("1. All Tasks")
    for status_position, task_status in enumerate(status_list,start=2):
        print(f"{status_position}. {task_status.title()}")
    
    while True:
        try:
            task_to_list= int(input(f"\nEnter your choice[1-{len(status_list)+1}]:  "))
            if 1<= task_to_list <= len(status_list) + 1:
                break
        except ValueError as e:
            print(f"Please only enter a whole number[1-{len(status_list)+1}]. Error: {e}")
    
    found_matching_task_status(to_do_list, task_to_list)    
    
           
# Load function (Tasks stored in JSON file --> Python), run 1 after menu(Enum) to get the prior stored tasks
def load_json(list_to_store):
    try:
        with open("task_tracker.json", "r") as jfile:
            loaded_file = json.load(jfile)
    except FileNotFoundError as e1:
        print(f"Can not find any matching JSON file. Error:{e1}")
    except json.JSONDecodeError as e2:
        print(f"Detected damaged JSON file! Error: {e2}")
    
    else: 
        for task_dict in loaded_file:
            task = Task(task_dict["id"], task_dict["description"], task_dict["status"], datetime.fromisoformat(task_dict["createdAt"]), datetime.fromisoformat(task_dict["updatedAt"]))
            list_to_store.append(task)
            
# Save function ( Load Task in Python --> JSON file), run every time changes happen
def save_to_json(list_to_save):
    converted_dicts = []
    for task in list_to_save:
        task_dict = {
            "id": task.id,
            "description": task.description,
            "status":task.status, 
            "createdAt": task.createdAt.isoformat(),
            "updatedAt": task.updatedAt.isoformat()
            }
        converted_dicts.append(task_dict)
    try:
        with open("task_tracker.json","w") as task_json:
            json.dump(converted_dicts, task_json, indent=4)
    except OSError as e:
        print(f"Your tasks could not be saved. Please check that the file is not open or locked. Error: {e}")

if __name__ == "__main__":
    main()

        


        
                
    
    
    




