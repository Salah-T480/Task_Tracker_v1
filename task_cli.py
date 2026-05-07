import argparse
import json
from datetime import datetime


if __name__=='__main__':

    # database's file name
    DB_PATH='dataBase.json'


    # 1_ initialize the database

    # a dictionary to manipulate the database easily
    # the structure will be like this:
    """
        data={
            id:{
                "description": "new Project",
                "status": "in-progress",
                "createdAt": "2026-05-06 10:30:00",
                "updatedAt": "2026-05-06 10:30:00"
            }
        }
    """
    data={}

    # try to fetch tasks from database and store them in data
    # if it fails then create an empty json file
    try :
        with open(DB_PATH,'r',encoding='utf-8') as f:
            data=json.load(f)
    except (FileNotFoundError,json.JSONDecodeError) as e:
        print(f'ERROR: {e}')
        try:
            with open(DB_PATH,'w',encoding='utf-8') as f:
                json.dump({},f)
            print(f"File created ({DB_PATH})")
        except (FileNotFoundError,json.JSONDecodeError) as e:
            print(f'ERROR: {e}')
    

    # 2_ helper functions

    def get_time():
        """Returns the current time as a string in 'YYYY-MM-DD HH:MM:SS' format."""
        return datetime.now().isoformat(sep=' ',timespec='seconds')

    def print_header(head: list[str]):
        """Prints a formatted table header with the given column names."""
        print('-'*27*5)
        for h in head:
            print(f'{h:^26}|',end='')
        print()
        print('-'*27*5)

    def display_all_tasks(data: tuple[str,dict]):
        """Displays all tasks in a formatted table and prints the total count."""
        count=0
        for id , details in data:
            print(f"{id:^26}|",end='')
            count+=1
            for value in details.values():
                print(f'{value:<26}|',end='')
            print()
        print('-'*27*5)
        print(f'the total number of tasks is : {count}')

    def display_specific_tasks(data: tuple[str,dict], status: str):
        """Displays only tasks matching the given status and prints their count."""
        count=0
        for id , details in data:
            if details['status']==status:
                count+=1
                print(f"{id:^26}|",end='')
                for value in details.values():
                    print(f'{value:<26}|',end='')
                print()
        print('-'*27*5) 
        print(f'the total number of tasks of type ({status}) is : {count}')

    def to_data_base(source: dict, destination: str):
        """
        Writes the given dictionary to a JSON file at the specified path.
        Returns True on success, False on failure.
        """
        try:
            with open(destination,'w',encoding='utf-8') as f:
                json.dump(source,f,indent=2)
            return True
        except (FileNotFoundError,json.JSONDecodeError) as e:
            print(f'ERROR: {e}')
            return False

    def mark_task(id: str, status: str, data: dict):
        """
        Updates the status of a task by its ID.
        Returns True on success, prints an error and returns None if ID not found.
        """
        if id in data:
            data[id]["status"]=status
            return to_data_base(data,DB_PATH)
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
        

    # 3_ create parser
    parser=argparse.ArgumentParser()
    
    # create a subparser named 'command'
    subparser= parser.add_subparsers(dest='command')


    # 4_ create positional arguments

    # add section — 'add <description>'
    add_parser=subparser.add_parser('add',help='enter your task here')
    add_parser.add_argument('description',type=str)

    # update section — 'update <id> <description>'
    update_parser=subparser.add_parser('update',help='enter the id and the new task to update')
    update_parser.add_argument('id',type=str)
    update_parser.add_argument('description',type=str)

    # delete section — 'delete <id>'
    delete_parser= subparser.add_parser('delete',help="enter the id to delete a specific task")
    delete_parser.add_argument('id',type=str)

    # mark-in-progress section — 'mark-in-progress <id>'
    mark_in_progress_parser = subparser.add_parser('mark-in-progress',help="enter the task's id to mark it in progress")
    mark_in_progress_parser.add_argument('id',type=str)

    # mark-done section — 'mark-done <id>'
    mark_done_parser = subparser.add_parser('mark-done',help="enter the task's id to mark it done")
    mark_done_parser.add_argument('id',type=str)

    # mark-todo section — 'mark-todo <id>' (bonus: allows reverting a task back to todo)
    mark_todo_parser = subparser.add_parser('mark-todo',help="enter the task's id to mark it todo")
    mark_todo_parser.add_argument('id',type=str)

    # list section — 'list <status>'
    # status choices: all | todo | in-progress | done
    # defaults to 'all' if no status is provided
    list_parser=subparser.add_parser('list',help="enter a status ['all','todo','in-progress','done'] to list specific tasks or all of them")
    list_parser.add_argument('status',choices=['all','todo','in-progress','done'],nargs='?',default='all')

    # the commented section below is an alternative version using flags instead of positional arguments
    """
    #parser.add_argument('-add',type=str,help='enter your task here')
    #parser.add_argument('-update',metavar='<id task>',nargs=2,help='enter the id and the new task to update')
    #parser.add_argument('-delete',type=str,metavar='<id>',help="enter the id to delete a specific task")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-mark-in-progress','--mark_in_progress',type=str,metavar='<id>',help="enter the task's id to mark it in progress")
    group.add_argument('-mark-done','--mark_done',type=str,metavar='<id>',help="enter the task's id to mark it done")
    group.add_argument('-mark-todo','--mark_todo',type=str,metavar='<id>',help="enter the task's id to mark it todo")
    #parser.add_argument('-list',choices=['all','todo','in-progress','done'],nargs='?',const='all')
    """


    # 5_ initialize the parser
    arg=parser.parse_args()


    # 6_ logic

    # add a new task
    if arg.command=='add':
        createdAt=get_time()
        numeric_id=[int(k) for k in data if k.isdigit()]   # get all numeric keys as ints
        id= max(numeric_id)+1 if numeric_id else 1          # generate next available id
        data[str(id)]=dict(description=arg.description,status='todo',createdAt=str(createdAt),updatedAt=str(createdAt))
        if to_data_base(data,DB_PATH):
            print(f'Task added successfully ID({id})')
    
    # update an existing task's description
    if arg.command=="update":
        updatedAt=get_time()
        id=arg.id
        newTask=arg.description
        if id in data:
            data[id]["description"]=newTask
            data[id]["updatedAt"]=str(updatedAt)
            if to_data_base(data,DB_PATH):
                print(f'Task updated successfully ID({id})')
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
    
    # delete a task by id
    if arg.command=='delete':
        id=arg.id
        if id in data:
            del data[id]
            if to_data_base(data,DB_PATH):
                print(f'Task deleted successfully ID({id})')
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
    
    # change task status
    if arg.command=='mark-in-progress':
        id=arg.id
        if mark_task(id,'in-progress',data):
            print(f'Task with ID({id}) set to (in-progress)')
    if arg.command=='mark-done':
        id=arg.id
        if mark_task(id,'done',data):
            print(f'Task with ID({id}) set to (done)')
    if arg.command=='mark-todo':
        id=arg.id
        if mark_task(id,'todo',data):
            print(f'Task with ID({id}) set to (todo)')

    # list tasks
    if arg.command=='list':
        print_header(['task id','description','status','created at',"updated at"])
        tasks=list(data.items())

        if arg.status=='all':
            display_all_tasks(tasks)
        else:
            display_specific_tasks(tasks,arg.status)
    
    # if no command is provided, display help
    if arg.command==None:
        parser.print_help()