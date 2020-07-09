# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import calendar
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
 
 
def print_menu():
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Add task
0) Exit''')
 
 
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())
 
    def __repr__(self):
        return self.task
 
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
 
def print_one_day(today):
    print(calendar.day_name[today.weekday()], today.day, today.strftime('%b') + ':')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    for i in range(len(rows)):
        print(str(i+1) + '. ' + rows[i].task)
    if len(rows) == 0:
        print("Nothing to do!")
    print()
 
 
def __main__():
    while True:
        print_menu()
        order = int(input())
        if order == 1:     # print today tasks
            today = datetime.today()
            print("Today", today.day, today.strftime('%b') + ':')
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            for i in range(len(rows)):
                print(str(i+1) + '. ' + rows[i].task)
            if len(rows) == 0:
                print("Nothing to do!")
            print()
            continue
 
        elif order == 2:   # print this weeks tasks
            today = datetime.today()
            for i in range(7):
                print_one_day(today + timedelta(days=i))
            continue
 
        elif order == 3:     # print the entire list
            print("All tasks:")
            rows = session.query(Table).all()
            for i in range(len(rows)):
                print(str(i+1) + '. ' + rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b'))
            if len(rows) == 0:
                print("Nothing to do!")
            print()
            continue
 
        elif order == 4:   # add row to table
            task_field = input("Enter task\n")
            date_field = input("Enter deadline\n")
            new_row = Table(task=task_field,
                            deadline=datetime.strptime(date_field, '%Y-%m-%d'))
            session.add(new_row)
            session.commit()
            print("The task has been added")
            print()
            continue
 
        elif order == 0:
            print("Bye!")
            break
 
 
if __name__ == "__main__":
    __main__()