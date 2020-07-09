# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
 
 
class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())
 
    def __repr__(self):
        return self.task
 
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
 
def today_task():
    rows = session.query(Table).all()
    if len(rows) == 0:
        return 'Nothing to do!'
    list_of_tasks = []
    for i in rows:
        list_of_tasks.append(i.task)
    return list_of_tasks
 
 
def enter_task(task_descr):
    new_row = Table(task=task_descr, deadline=datetime.today())
    session.add(new_row)
    session.commit()
    return 'The task has been added!'
 
 
while True:
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")
 
    user_choice = int(input())
    if user_choice == 1:
        tasks = today_task()
        if tasks == 'Nothing to do!':
            print(tasks)
        else:
            for i in tasks:
                print(i)
    elif user_choice == 2:
        print('Enter task')
        task = input()
        print(enter_task(task))
    elif user_choice == 0:
        print('Bye!')
        break