# Task-Tracker

A command-line task manager written in Python. You add tasks, change their description or status, delete them and list them. Tasks are saved in a JSON file, so they are still there the next time you run the program.

This project is based on the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh.

## Features

- Add one or more tasks in a row
- Update a task's description
- Change a task's status: `todo`, `in-progress` or `done`
- Delete a task
- List all tasks, or only the tasks with a chosen status
- Tasks are saved automatically after every change and loaded when the program starts

## Requirements

- Python 3.12 or newer
- No external libraries (only Python's built-in modules)

## How to run

1. Clone the repository:
   ```
   git clone https://github.com/athenasou/Task-Tracker.git
   cd Task-Tracker
   ```
2. Start the program:
   ```
   python3 task_tracker.py
   ```

## How to use

The program shows a numbered menu:

| Option | Action | What to do |
|--------|--------|------------|
| 1 | Add | Type a description and press Enter. Repeat for more tasks. Press Enter on an empty line to finish. |
| 2 | Update | Choose a task by its id, then type the new description. |
| 3 | Delete | Choose a task by its id. |
| 4 | List | Choose 1 for all tasks, or 2 to 4 for tasks with one status. |
| 5 | Status_Marking | Choose a task by its id, then type `todo`, `in-progress` or `done`. |

After each action, the program asks whether you want to continue. Type `n` or `no` to quit.

## Task data

Each task stores:

| Field | Meaning |
|-------|---------|
| `id` | A unique number. It never repeats, even after deletions. |
| `description` | A short description of the task |
| `status` | `todo`, `in-progress` or `done` |
| `createdAt` | When the task was created |
| `updatedAt` | When the task was last changed |

Tasks are saved in `task_tracker.json` in the folder where you