import datetime
from copy import copy
from datetime import date, time
from pawpal_system import Owner,Pet,Scheduler,Task 
# importing classes to instantiate objects


owner1 = Owner("Crystal","Smith",45)
pt1 = Pet("Mochi",3,"healthy")
pt2 = Pet("Yeontan",5,"needs medication")

owner1.add_pet(pt1)
owner1.add_pet(pt2)

task1 = Task("Morning walk", time(10, 0, 0), "daily", False, date.today(), priority="high")
task2 = Task("Feed breakfast", time(11, 0, 0), "daily", False, date.today(), priority="high")
task3 = Task("Playtime", time(20, 0, 0), "daily", False, date.today(), priority="medium")
task4 = Task("Vet appointment", time(9, 0, 0), "weekly", False, date.today(), priority="high")
task5 = Task("Grooming", time(11, 0, 0), "weekly", False, date.today(), priority="low")
task6 = Task("Medication", time(18, 0, 0), "daily", False, date.today(), priority="high")
task7 = Task("Training session", time(15, 0, 0), "weekly", False, date.today(), priority="medium")
task8 = Task("Socialization", time(20, 0, 0), "weekly", False, date.today(), priority="low")

scheduler = Scheduler(date.today(), owner=owner1)
owner1.pets[0].tasks.append(task1)
owner1.pets[0].tasks.append(task2)
owner1.pets[0].tasks.append(task4)
owner1.pets[0].tasks.append(task5)
owner1.pets[0].tasks.append(copy(task3))
owner1.pets[0].tasks.append(task8)

owner1.pets[1].tasks.append(copy(task1))
owner1.pets[1].tasks.append(copy(task2))
owner1.pets[1].tasks.append(task3)
owner1.pets[1].tasks.append(task6)
owner1.pets[1].tasks.append(task7)

print("-"*35)
print("Today's schedule:")
sch = scheduler.check_calendar()

for task in sch:
    print(f"  • [{task.priority.upper()}] {task.description} at {task.time_due}")
print("-"*35)

task1.mark_complete()


for i in range(len(owner1.pets)):
    print(f"\n{owner1.pets[i].name}'s tasks:")
    for task in scheduler.filter_tasks(pet_name=owner1.pets[i].name):
        status = "done" if task.completion_status else "pending"
        print(f"  • {task.description} [{status}]")

print("\nIncomplete tasks (all pets):")
for task in scheduler.filter_tasks(completion_status=False):
    print(f"  • [{task.pet.name}] {task.description} at {task.time_due}")

print("\nConflicts:")
for message in scheduler.detect_conflicts():
    print(f"  {message}")
print("-"*35)