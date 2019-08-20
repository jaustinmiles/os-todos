import csv

FILE_NAME = 'life_os_spread.csv'
TASK_NAME_COL = 0
PRIORITY_COL = 1
DAILY_COL = 2
COMPLETED_COL = 3


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
        elif row[3] == 'TRUE':
            continue
        elif row[1] == '':
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
    rows = open_file_and_get_rows()
    replace_row(rows, to_mark)
    write_rows_to_file(rows)


def write_rows_to_file(rows):
    with open(FILE_NAME, 'w') as write_file:
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


def mark_as_in_progress():
    to_mark = decide_task()
    num = int(to_mark[PRIORITY_COL]) - 1
    to_mark[PRIORITY_COL] = str(num)
    rows = open_file_and_get_rows()
    replace_row(rows, to_mark)
    write_rows_to_file(rows)


if __name__ == '__main__':
    print(decide_task())
    # mark_as_done()
    mark_as_in_progress()
    print(decide_task())
