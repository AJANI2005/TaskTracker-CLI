# Check if file exist
import os
import datetime
import json


file_path = "data.json"

data = {"tasks": []}
# If file doesn't exist or is empty, initialize it
if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    with open(file_path, "w") as f:
        json.dump(data, f)

# Now safe to read
with open(file_path, "r") as f:
    data = json.load(f)


def createTask(
    id: int,
    descriptions: str,
    status: str,
    createdAt: str,
    updatedAt: str,
):
    return {
        "id": id,
        "descriptions": descriptions,
        "status": status,
        "createdAt": createdAt,
        "updatedAt": updatedAt,
    }


def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f)


def add_task(task):
    data["tasks"].append(task)
    save_data()


def get_task(id):
    for task in data["tasks"]:
        if task["id"] == id:
            return task
    return None


def delete_task(id):
    task = get_task(id)
    if task is None:
        print("Task not found")
        return

    data["tasks"].remove(task)
    save_data()


def update_task_description(id, description):
    task = get_task(id)
    if task is None:
        print("Task not found")
        return

    task["descriptions"] = description
    task["updatedAt"] = str(datetime.datetime.now())
    save_data()


def mark_task(id, status):
    task = get_task(id)
    if task is None:
        print("Task not found")
        return

    task["status"] = status
    save_data()


def list_tasks(status="all"):
    tasks = []
    for task in data["tasks"]:
        if task["status"] == status or status == "all":
            tasks.append(task)
    return tasks


def pretty_print(status):
    tasks = data["tasks"]
    if len(tasks) == 0:
        print("No tasks found")
        return
    # Headers
    headers = ["ID", "Description", "Status", "Created", "Updated"]

    # Convert data to rows (including headers)
    rows = [
        [
            str(task["id"]),
            task["descriptions"],
            task["status"],
            task["createdAt"],
            task["updatedAt"],
        ]
        for task in tasks
    ]
    rows.insert(0, headers)

    # Calculate column widths
    col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(headers))]

    # Function to format a row
    def format_row(row):
        return " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))

    # Print table
    print(format_row(headers))
    print("-+-".join("-" * w for w in col_widths))
    for task in tasks:
        if task["status"] != status and status != "all":
            continue
        print(
            format_row(
                [
                    task["id"],
                    task["descriptions"],
                    task["status"],
                    task["createdAt"],
                    task["updatedAt"],
                ]
            )
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # add
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Task description")

    # list
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.add_argument("--status", type=str, default="all", help="Task status")

    # delete
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task id")

    # update
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", type=int, help="Task id")
    parser_update.add_argument("description", type=str, help="Task description")

    # mark in progress
    parser_mark_in_progress = subparsers.add_parser(
        "mark-in-progress", help="Mark a task"
    )
    parser_mark_in_progress.add_argument("id", type=int, help="Task id")

    # mark done
    parser_mark_done = subparsers.add_parser("mark-done", help="Mark a task")
    parser_mark_done.add_argument("id", type=int, help="Task id")

    # mark todo
    parser_mark_todo = subparsers.add_parser("mark-todo", help="Mark a task")
    parser_mark_todo.add_argument("id", type=int, help="Task id")

    args = parser.parse_args()

    if args.command == "add":
        date = str(datetime.datetime.now())
        add_task(
            createTask(len(data["tasks"]) + 1, args.description, "todo", date, date)
        )
    elif args.command == "list":
        pretty_print(args.status)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task_description(args.id, args.description)
    elif args.command == "mark-in-progress":
        mark_task(args.id, "in-progress")
    elif args.command == "mark-done":
        mark_task(args.id, "done")
