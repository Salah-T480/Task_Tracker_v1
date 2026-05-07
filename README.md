# Task Tracker CLI

Task Tracker is a simple command line interface (CLI) used to track and manage your tasks.
It lets you track what you need to do, what you have done, and what you are currently working on.
All tasks are stored locally in a JSON file that is auto-created on first run.

---

## Requirements

- Python 3.12.3 or higher
- No external libraries required

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Salah-T480/Task_Tracker_v1.git

# Navigate to the project directory
cd Task_Tracker_v1
```

---

## Usage

```bash
python task_cli.py <command> [arguments]
```

| Command | Example | Description |
|---|---|---|
| `add` | `python task_cli.py add "Buy groceries"` | Add a new task |
| `update` | `python task_cli.py update 1 "Buy groceries and cook dinner"` | Update an existing task |
| `delete` | `python task_cli.py delete 1` | Delete a task by ID |
| `mark-in-progress` | `python task_cli.py mark-in-progress 1` | Mark a task as in progress |
| `mark-done` | `python task_cli.py mark-done 1` | Mark a task as done |
| `mark-todo` | `python task_cli.py mark-todo 1` | Revert a task back to todo |
| `list` | `python task_cli.py list` | List all tasks |
| `list todo` | `python task_cli.py list todo` | List all todo tasks |
| `list in-progress` | `python task_cli.py list in-progress` | List all in-progress tasks |
| `list done` | `python task_cli.py list done` | List all done tasks |

---

## Examples

```bash
$ python task_cli.py add "Buy groceries"
Task added successfully ID(1)

$ python task_cli.py add "Read a book"
Task added successfully ID(2)

$ python task_cli.py mark-in-progress 1
Task with ID(1) set to (in-progress)

$ python task_cli.py update 2 "Read Clean Code book"
Task updated successfully ID(2)

$ python task_cli.py list
-----------------------------------------------------------------------------
          task id           |        description       |         status         |        created at        |        updated at        |
-----------------------------------------------------------------------------
            1               |  Buy groceries           |  in-progress           |  2026-05-06 10:30:00     |  2026-05-06 10:30:00     |
            2               |  Read Clean Code book    |  todo                  |  2026-05-06 10:30:00     |  2026-05-06 10:35:00     |
-----------------------------------------------------------------------------
the total number of tasks is : 2

$ python task_cli.py delete 1
Task deleted successfully ID(1)
```

---

## Task Properties

Each task is stored in `dataBase.json` with the following structure:

```json
{
  "1": {
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2026-05-06 10:30:00",
    "updatedAt": "2026-05-06 10:30:00"
  }
}
```

| Property | Description |
|---|---|
| `id` | Unique identifier, auto-generated |
| `description` | Short description of the task |
| `status` | Current status: `todo`, `in-progress`, or `done` |
| `createdAt` | Date and time when the task was created |
| `updatedAt` | Date and time when the task was last updated |

---

## Project Structure

```
Task_Tracker_v1/
    |__ task_cli.py       ← main application
    |__ dataBase.json     ← auto-created on first run
    |__ README.md
```

---

## Notes

- `dataBase.json` is automatically created if it does not exist
- Task IDs are auto-generated and never reused after deletion
- `mark-todo` allows you to revert a task back to todo in case of mistakes
- Run `python task_cli.py` with no arguments to display the help message