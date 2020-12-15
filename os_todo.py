import csv
import datetime
import getopt
import json
import sys
from pprint import pprint

FILE_NAME = "life_os_spread.csv"
TASK_NAME_COL = 0
PRIORITY_COL = 1
DAILY_COL = 2
COMPLETED_COL = 3
MAX_PRIORITY = 16
SIGN_IN_FILE = 'sign_in.json'


# TODO: Make a display all function to look and see if a certain task is already there


def decide_task():
    with open(FILE_NAME, 'r') as csv_file:
        priorities, rows = get_rows(csv_file)
        del rows[0]
    csv_file.close()
    tasks = [x for _, x in sorted(zip(priorities, rows), reverse=True)]
    return tasks[TASK_NAME_COL]


def get_rows(csv_file):
    rows = []
    priorities = []
    csvreader = csv.reader(csv_file)
    for row in csvreader:
        if len(row) == 0:
            continue
        elif row[COMPLETED_COL] == 'TRUE' and row[DAILY_COL] != 'TRUE':
            continue
        elif row[PRIORITY_COL] == '':
            continue
        rows.append(row)
        get_priority(priorities, row)
    return priorities, rows


def get_priority(priorities, row):
    try:
        priorities.append(int(row[1]))
    except ValueError:
        if row[PRIORITY_COL] != 'Priority':
            print(row)
            raise ValueError("Priority must be an integer number")


def mark_as_done():
    to_mark = decide_task()
    to_mark[COMPLETED_COL] = 'TRUE'
    if to_mark[DAILY_COL] == 'TRUE':
        to_mark[PRIORITY_COL] = str(1)
    rows = open_file_and_get_rows()
    replace_row(rows, to_mark)
    write_rows_to_file(rows)


def write_rows_to_file(rows):
    with open(FILE_NAME, 'w', newline='') as write_file:
        c = csv.writer(write_file)
        c.writerows(rows)
        write_file.close()


def replace_row(rows, to_mark):
    for i, row in enumerate(rows):
        if row[TASK_NAME_COL] == to_mark[TASK_NAME_COL]:
            rows[i] = to_mark


def open_file_and_get_rows():
    with open(FILE_NAME, 'r') as csv_file:
        _, rows = get_rows(csv_file)
        csv_file.close()
    return rows


def mark_as_in_progress(decrement):
    to_mark = decide_task()
    num = int(to_mark[PRIORITY_COL]) - decrement
    if num < 0:
        num = 0
    to_mark[PRIORITY_COL] = str(num)
    rows = open_file_and_get_rows()
    replace_row(rows, to_mark)
    write_rows_to_file(rows)


def show_all_tasks():
    with open(FILE_NAME, 'r') as csv_file:
        priorities, rows = get_rows(csv_file)
        tasks = [x for _, x in sorted(zip(priorities, rows), reverse=True)]
        csv_file.close()
    pprint(tasks)


def main(argv):
    # print(decide_task())
    check_last_sign_in()
    try:
        opts, args = getopt.getopt(argv, 'pcxdars')
    except getopt.GetoptError:
        print("Use os_todo.py -p to postpone a task by 1 day")
        print("Use os_todo.py -c to complete a task")
        print("Use os_todo.py -x to extend the due date of a task by 5 days")
        print("Use os_todo.py -d to increment the priorities of every undone task")
        print("Use os_todo.py -a to add a new task")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-p":
            mark_as_in_progress(1)
        elif opt == "-c":
            mark_as_done()
        elif opt == "-x":
            mark_as_in_progress(5)
        elif opt == "-d":
            end_day()
        elif opt == "-a":
            add_task()
        elif opt == "-r":
            mark_as_in_progress(16)
        elif opt == "-s":
            show_all_tasks()
    print(decide_task())


def end_day():
    rows = open_file_and_get_rows()
    for row in rows:
        if row[PRIORITY_COL] == 'Priority':
            continue
        if row[COMPLETED_COL] == 'FALSE' and row[DAILY_COL] == 'TRUE':
            row[PRIORITY_COL] = str(int(row[PRIORITY_COL]) + 4)
        elif row[COMPLETED_COL] == 'TRUE' and row[DAILY_COL] == 'TRUE':
            row[PRIORITY_COL] = str(9)
            row[COMPLETED_COL] = "FALSE"
        else:
            row[PRIORITY_COL] = str(int(row[PRIORITY_COL]) + 1)
    write_rows_to_file(rows)


def add_task():
    name = input("What is the name of your task?")
    priority = input("In how many days is this task due? Enter 'Daily' if this is a daily task.")
    try:
        priority = str(MAX_PRIORITY + 1 - int(priority))
        daily = 'FALSE'
    except ValueError:
        if 'daily' in priority.lower():
            daily = 'TRUE'
            priority = 9
        else:
            print("The value you entered was not a valid option. Please try again")
            return
    row = [[name, priority, daily, 'FALSE']]
    rows = open_file_and_get_rows()
    rows = rows + row
    write_rows_to_file(rows)
    print("Success!")


def check_last_sign_in():
    with open(SIGN_IN_FILE, 'r') as f:
        sign = json.load(f)
    last = sign['last_sign_in']
    year = last["year"]
    month = last["month"]
    day = last["day"]
    last_sign = datetime.datetime(year, month, day)
    today = datetime.datetime.now()
    sign['last_sign_in']['year'] = today.year
    sign['last_sign_in']['month'] = today.month
    sign['last_sign_in']['day'] = today.day
    with open(SIGN_IN_FILE, 'w') as out_file:
        json.dump(sign, out_file)
    days = today.day - last_sign.day
    for i in range(days):
        end_day()


if __name__ == '__main__':
    main(sys.argv[1:])
