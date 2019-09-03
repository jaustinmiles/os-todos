# os-todos
This task management system helps users minimize the effects of such concepts as the convoy effect in their personal lives! By fusing concepts from Round Robin, Priority-Based, and Time-Based programming philosophies, OSTodos helps users focus on the single most important task without worrying about future tasks. 

# Usage
To add a task to the system, run
```
os_todo.py -a
```

and follow the prompts. The priority of the task will be determined by the days until the task is due, designated by the user at runtime.

To complete a task, run
```
os_todo.py -c
```
This will remove the task from the system if it is not a daily task. Otherwise, it will revert to its priority level as a daily.

If there is no possible way you can do a task at the moment, run 
```
os_todo.py -p
```
to postpone the task by 1 day.

For long term tasks that need to be worked on multiple times per week before completion, but are not dailies, use 
```
os_todo.py -x
```
to extend the task's due date by 5 days. Make sure to enter these tasks as regular tasks, not as dailies.

Finally, when your day is over, run 
```
os_todo.py -d 
```
to end the day. This will increase all the priorities of your tasks by 1 if they are not dailies, and by the appropriate scale if they are. 
