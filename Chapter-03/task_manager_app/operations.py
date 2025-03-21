import csv
from typing import Optional

from models import Task, TaskV2WithID, TaskWithID

DATABASE_FILENAME = "tasks.csv"

column_fields = ["id", "title", "description", "status"]


def read_all_tasks() -> list[TaskWithID]:
    with open(DATABASE_FILENAME) as csv_file:
        reader = csv.DictReader(csv_file)
        return [TaskWithID(**row) for row in reader]


def read_task(task_id) -> Optional[TaskWithID]:
    with open(DATABASE_FILENAME) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if int(row["id"]) == task_id:
                return TaskWithID(**row)


def get_next_id():
    try:
        with open(DATABASE_FILENAME, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1


def write_task_into_csv(task: TaskWithID):
    with open(DATABASE_FILENAME, "a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_fields)
        writer.writerow(task.model_dump())


def create_task(task: Task) -> TaskWithID:
    id = get_next_id()
    task_with_id = TaskWithID(id=id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id


def modify_task(id: int, task: dict) -> Optional[TaskWithID]:
    updated_task: Optional[TaskWithID] = None
    tasks = read_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            updated_task = task_.model_copy(update=task)
            tasks[number] = updated_task
    # 更新后的对象写入CSV文件
    with open(DATABASE_FILENAME, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_fields)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.model_dump())
    if updated_task:
        return updated_task


def remove_task(id: int) -> Optional[Task]:
    deleted_task: Optional[Task] = None
    tasks = read_all_tasks()
    with open(DATABASE_FILENAME, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=column_fields,
        )
        writer.writeheader()
        for task in tasks:
            if task.id == id:
                deleted_task = task
                continue
            writer.writerow(task.model_dump())
    if deleted_task:
        dict_task_without_id = deleted_task.model_dump()
        del dict_task_without_id["id"]
        return Task(**dict_task_without_id)


def read_all_tasks_v2() -> list[TaskV2WithID]:
    with open(DATABASE_FILENAME) as csv_file:
        reader = csv.DictReader(
            csv_file,
        )
        return [TaskV2WithID(**row) for row in reader]
