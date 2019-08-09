import csv

FILE_NAME = 'life_os_spread.csv'


def decide_task():
    with open(FILE_NAME, 'r') as csv_file:
        priorities, rows = get_rows(csv_file)
        del rows[0]
    csv_file.close()
    tasks = [x for _, x in sorted(zip(priorities, rows), reverse=True)]
    return tasks[0]


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
        if row[1] != 'Priority':
            print(row)
            raise ValueError("Priority must be an integer number")


def mark_as_done():
    to_mark = decide_task()
    to_mark[3] = 'TRUE'
    with open(FILE_NAME, 'r') as csv_file:
        _, rows = get_rows(csv_file)
        csv_file.close()
    for i, row in enumerate(rows):
        if row[0] == to_mark[0]:
            rows[i] = to_mark
    with open(FILE_NAME, 'w') as write_file:
        c = csv.writer(write_file)
        c.writerows(rows)
        write_file.close()


if __name__ == '__main__':
    print(decide_task())
    # mark_as_done()
    print(decide_task())
