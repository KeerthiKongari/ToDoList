# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
 
 
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=lambda: datetime.today().date())
 
    def __repr__(self):
        return self.task
 
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
 
def week_task():
    today = datetime.today().date()
    for i in range(7):
        day = today + timedelta(days=i)
        print('\n', DAYS[day.weekday()], day.day, today.strftime('%b'))
        rows = session.query(Table).filter(Table.deadline == day).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i_row, row in enumerate(rows):
                print(i_row + 1, row)
 
 
def today_tasks():
    today = datetime.today().date()
    print("Today:")
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for row in rows:
            print(row)
 
 
def add_task():
    new_row = Table(task=input("Enter task"), deadline=datetime(*map(int, input("Enter deadline").split('-'))))
    session.add(new_row)
    session.commit()
    print("The task has been added!")
 
 
def all_task():
    print("All tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("No task!")
    else:
        for i_row, row in enumerate(rows):
            print(f"{i_row + 1})", row)
 
 
def missed_task():
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for i_row, row in enumerate(rows):
            print(f"{i_row + 1})", row)
 
 
def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        for i_row, row in enumerate(rows):
            print(f"{i_row + 1})", row)
        session.delete(rows[int(input("Chose the number of the task you want to delete:")) - 1])
        session.commit()
 
 
MENU = {'0': exit, '1': today_tasks, '2': week_task, '3': all_task, '4': missed_task, '5': add_task, '6': delete_task}
CHOICES = ['\n', "1) Today's tasks", "2) Week's tasks", "3) All tasks",
           "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit"]
while True:
    MENU[input("\n".join(CHOICES))]()