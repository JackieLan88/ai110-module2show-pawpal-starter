import datetime
from datetime import date, time
from pawpal_system import Owner,Pet,Scheduler,Task 
# importing classes to instantiate objects


owner1 = Owner("Crystal","Smith",45)
pt1 = Pet("Mochi",3,"healthy")
pt2 = Pet("Yeontan",5,"needs medication")

owner1.add_pet(pt1)
owner1.add_pet(pt2)

task1 = Task("Morning walk", time(10, 0, 0), "high", False, date.today())
task2 = Task("Feed breakfast", time(15, 0, 0), "high", False, date.today())
task3 = Task("Playtime", time(20, 0, 0), "medium", False, date.today())


scheduler = Scheduler(date.today(), owner=owner1)
owner1.pets[0].tasks.append(task1)
owner1.pets[0].tasks.append(task2)
owner1.pets[1].tasks.append(task3)
owner1.pets[1].tasks.append(task2)
owner1.pets[1].tasks.append(task1)

print("-"*35)
print("Today's schedule:")
sch = scheduler.check_calendar()

for task in sch:
    print(f"  • {task.description} at {task.time_due} [{task.frequency}]")
print("-"*35)