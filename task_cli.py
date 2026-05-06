import argparse
import json
from datetime import datetime

if __name__=='__main__':

    DB_PATH='dataBase.json'

    def get_time():
        return datetime.now().isoformat(sep=' ',timespec='seconds')

    def print_header(head : list[str]):
        print('-'*27*5)
        for h in head:
            print(f'{h:^26}|',end='')
        print()
        print('-'*27*5)


    def display_all_tasks(data: tuple[str,dict]):
        count=0
        for id , details in data:
            print(f"{id:^26}|",end='')
            count+=1
            #print(details)
            for value in details.values():
                print(f'{value:<26}|',end='')
            print()
        print('-'*27*5)
        print(f'the total number of tasks is : {count}')

    def display_specific_tasks(data:tuple[str,dict],status:str):
        count=0
        for id , details in data:
            if details['status']==status:
                count+=1
                print(f"{id:^26}|",end='')
                #print(details)
                for value in details.values():
                    print(f'{value:<26}|',end='')
                print()
        print('-'*27*5) 
        print(f'the total number of tasks of type ({status}) is : {count}')

    def to_data_base(id:str,source:dict,distination:str):
        try:
            with open(distination,'w',encoding='utf-8') as f:
                json.dump(source,f,indent=2)
            return True
        except (FileNotFoundError,json.JSONDecodeError) as e:
            print(f'ERROR: {e}')
            return False

    def mark_task(id:str,status:str,data:dict):
        if id in data:
            data[id]["status"]=status
            return to_data_base(id,data,DB_PATH)
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
        
        


    data={}

    try :
        with open(DB_PATH,'r',encoding='utf-8') as f:
            data=json.load(f)
    except (FileNotFoundError,json.JSONDecodeError) as e:
        print(f'ERROR: {e}')
        try:
            with open(DB_PATH,'w',encoding='utf-8') as f:
                json.dump({},f)
            print("File created (dataBase.json)")
        except (FileNotFoundError,json.JSONDecodeError) as e:
            print(f'ERROR: {e}')
        try:
            with open(DB_PATH,'r',encoding='utf-8') as f:
                data=json.load(f)
        except (FileNotFoundError,json.JSONDecodeError) as e:
            print(f'ERROR: {e}')

    parser=argparse.ArgumentParser()
    subparser= parser.add_subparsers(dest='command')

    add_parser=subparser.add_parser('add',help='enter your task here')
    add_parser.add_argument('description',type=str)
    #parser.add_argument('-add',type=str,help='enter your task here')

    update_parser=subparser.add_parser('update')
    update_parser.add_argument('id',type=str)
    update_parser.add_argument('description',type=str)
    #parser.add_argument('-update',metavar='<id task>',nargs=2,help='enter the id and the new task to update')

    delete_parser= subparser.add_parser('delete')
    delete_parser.add_argument('id',type=str)
    #parser.add_argument('-delete',type=str,metavar='<id>',help="enter the id to delete a specefic task")

    """
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-mark-in-progress','--mark_in_progress',type=str,metavar='<id>',help="enter the task's id to mark it in progress")
    group.add_argument('-mark-done','--mark_done',type=str,metavar='<id>',help="enter the task's id to mark it done")
    group.add_argument('-mark-todo','--mark_todo',type=str,metavar='<id>',help="enter the task's id to mark it todo")
    """

    mark_in_progress_parser = subparser.add_parser('mark-in-progress')
    mark_in_progress_parser.add_argument('id',type=str)

    mark_done_parser = subparser.add_parser('mark-done')
    mark_done_parser.add_argument('id',type=str)

    mark_todo_parser = subparser.add_parser('mark-todo')
    mark_todo_parser.add_argument('id',type=str)


    list_parser=subparser.add_parser('list')
    list_parser.add_argument('status',choices=['all','todo','in-progress','done'],nargs='?',default='all')
    #parser.add_argument('-list',choices=['all','todo','in-progress','done'],nargs='?',const='all')


    arg=parser.parse_args()



    #print(arg)


    if arg.command=='add':
        createdAt=get_time()
        numeric_id=[int(k) for k in data if k.isdigit()]
        id= max(numeric_id)+1 if numeric_id else 1
        data[str(id)]=dict(description=arg.description,status='todo',createdAt=str(createdAt),updatedAt=str(createdAt))
        if to_data_base(id,data,DB_PATH):
            print(f'Task added successfully ID({id})')

    if arg.command=="update":
        updatedAt=get_time()
        id=arg.id
        newTask=arg.description
        if id in data:
            data[id]["description"]=newTask
            data[id]["updatedAt"]=str(updatedAt)
            if to_data_base(id,data,DB_PATH):
                print(f'Task updated successfully ID({id})')
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
    
    if arg.command=='delete':
        id=arg.id
        if id in data:
            del data[id]
            if to_data_base(id,data,DB_PATH):
                print(f'Task deleted successfully ID({id})')
        else:
            print(f"Sorry ID({id}) isn't in your dataBase ")
    
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

    if arg.command=='list':
        print_header(['task id','description','status','created at',"updated at"])
        tasks=list(data.items())

        if arg.status=='all':
            display_all_tasks(tasks)
            
        else:
            display_specific_tasks(tasks,arg.status)
    if arg.command==None:
        parser.print_help()
        