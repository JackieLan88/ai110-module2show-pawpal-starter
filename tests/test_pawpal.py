from datetime import date, time
from pathlib import Path
import sys
#Adds that specific pawpal directory to Python's system path
sys.path.append(str(Path(__file__).resolve().parents[1])) # path is converted to string

from pawpal_system import Task, Pet, Scheduler, Owner


def test_mark_complete_sets_completion_status_true():
	task = Task( # creating a task instance
		description="Morning walk",
		time_due=time(8, 0),
		frequency="daily",
		completion_status=False, # currently false
		date_due=date.today(),
	)

	task.mark_complete()

	assert task.completion_status is True # checks if completion_status is true after invoking mark_complete function, is false pytest will fail


def test_add_task_increases_pet_task_count():
	pet = Pet(name="Mochi", age=3, health_status="healthy")
	initial_count = len(pet.tasks) #creating a pet object and checking the length of tasks = 0

	task = Task(
		description="Afternoon walk",
		time_due=time(14, 0),
		frequency="daily",
		completion_status=False,
		date_due=date.today(),
	) # creating a task instance

	pet.add_task(task)# adding the task object to the pet list of tasks

	assert len(pet.tasks) == initial_count + 1  # increment counter and compare it to current length of list of tasks the resides in pet object
	assert task in pet.tasks # check if the actual reference task in list of pet's tasks
	assert task.pet == pet # check if the reference pet is inside task instance


# Testing PawPal+ (from README.md)

def test_scheduler_no_calendar_creation():
    """Verify calendar creation when no calendar is passed into the scheduler class"""
    scheduler = Scheduler(date=date.today()) # creating instance of scheduler without passing a calendar
    assert scheduler.calendar == [] # verify that the calendar is an empty list
    assert isinstance(scheduler.calendar, list) # also check if the calendar attribute of the scheduler object is explicitly built as a python list

def test_scheduler_existing_calendar():
    """Verify processing existing calendar when passed to scheduler"""
    task1 = Task(description="Walk", time_due=time(8, 0), frequency="daily", completion_status=False, date_due=date.today())
    task2 = Task(description="Feed", time_due=time(9, 0), frequency="daily", completion_status=False, date_due=date.today())
    custom_calendar = [task1, task2] # creating two tasks and pass it as a list to the scheduler instance below
    
    scheduler = Scheduler(date=date.today(), calendar=custom_calendar)
    assert scheduler.calendar == custom_calendar # check if calendars are exactly the same
    assert len(scheduler.calendar) == 2 # check quantity of tasks

def test_scheduler_no_owner():
    """Verify what is returned when there is no owner record (instance) passed to scheduler"""
    task1 = Task(description="Walk", time_due=time(8, 0), frequency="daily", completion_status=False, date_due=date(2023, 10, 2))
    task2 = Task(description="Feed", time_due=time(9, 0), frequency="daily", completion_status=False, date_due=date(2023, 10, 1))
    custom_calendar = [task1, task2]
    # scheduler object should take owner parameter, however we are not passing an owner object
    scheduler = Scheduler(date=date(2023, 10, 1), calendar=custom_calendar)
    
    # Check what is returned: no owner attached -> sorted by date and time
    result = scheduler.check_calendar()# should return a list of tasks sorted by date and time, not priority since no owner is attached
    assert result == [task2, task1] # time(9,0) on 10/1 is before time(8,0) on 10/2

def test_scheduler_sorting_priority_and_date():
    """Revise if all tasks are sorted by priority and date (time)"""
    owner = Owner(first_name="John", last_name="Doe", age=30)
    pet = Pet(name="Rex", age=2, health_status="healthy")
    owner.add_pet(pet)
    
    today = date(2023, 10, 1)
    
    # Priority values: "high", "medium", "low"
    t1 = Task(description="Low priority early", time_due=time(8, 0), frequency="daily", completion_status=False, date_due=today, priority="low")
    t2 = Task(description="High priority late", time_due=time(10, 0), frequency="daily", completion_status=False, date_due=today, priority="high")
    t3 = Task(description="High priority early", time_due=time(7, 0), frequency="daily", completion_status=False, date_due=today, priority="high")
    t4 = Task(description="Medium priority", time_due=time(9, 0), frequency="daily", completion_status=False, date_due=today, priority="medium")
    
    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)
    pet.add_task(t4)
    
    # Re-initialize scheduler with the owner
    scheduler = Scheduler(date=today, owner=owner)
    
    result = scheduler.check_calendar()
    
    # Expected sort order: High priority early, High priority late, Medium priority, Low priority early
    assert result == [t3, t2, t4, t1]


# --- Edge Case Tests ---

# 1. Recurring Tasks Edge Cases

def test_mark_complete_no_pet_assigned():
    """Verify that a task with no pet assigned fails gracefully and just marks completion"""
    task = Task(description="Walk", time_due=time(8,0), frequency="daily", completion_status=False, date_due=date(2023,10,1))
    task.mark_complete()
    assert task.completion_status is True
    # If no pet is attached, it shouldn't crash trying to append to a list


def test_mark_complete_double_completion():
    """Verify behaviour when mark_complete is called twice on the same task"""
    pet = Pet(name="Mochi", age=3, health_status="healthy")
    task = Task(description="Walk", time_due=time(8,0), frequency="daily", completion_status=False, date_due=date(2023,10,1))
    pet.add_task(task)
    
    task.mark_complete()
    assert len(pet.tasks) == 2  # Original task + the next occurrence
    
    task.mark_complete()
    # It blindly appends again, resulting in duplicate future tasks
    assert len(pet.tasks) == 3


def test_mark_complete_invalid_frequency():
    """Verify that tasks with invalid frequencies don't crash and don't schedule new tasks"""
    pet = Pet(name="Mochi", age=3, health_status="healthy")
    task = Task(description="Walk", time_due=time(8,0), frequency="monthly", completion_status=False, date_due=date(2023,10,1))
    pet.add_task(task)
    
    task.mark_complete()
    assert task.completion_status is True
    assert len(pet.tasks) == 1  # No new task scheduled


def test_mark_complete_month_rollover():
    """Verify daily tasks rollover months and leap years correctly"""
    pet = Pet(name="Mochi", age=3, health_status="healthy")
    task = Task(description="Walk", time_due=time(8,0), frequency="daily", completion_status=False, date_due=date(2024,2,29)) # Leap year
    pet.add_task(task)
    
    task.mark_complete()
    assert len(pet.tasks) == 2
    new_task = pet.tasks[-1]
    assert new_task.date_due == date(2024, 3, 1)


# 2. Sorting & Scheduling Edge Cases

def test_scheduler_same_priority_same_time():
    """Verify Stable Sorting when two tasks share the exact same priorities and times"""
    owner = Owner(first_name="John", last_name="Doe", age=30)
    pet = Pet(name="Rex", age=2, health_status="healthy")
    owner.add_pet(pet)
    today = date(2023, 10, 1)
    
    t1 = Task("Task A", time(8,0), "daily", False, today, priority="high")
    t2 = Task("Task B", time(8,0), "daily", False, today, priority="high")
    pet.add_task(t1)
    pet.add_task(t2)
    
    scheduler = Scheduler(date=today, owner=owner)
    result = scheduler.check_calendar()
    
    # Should maintain insertion order
    assert result == [t1, t2]


def test_scheduler_invalid_priority_fallback():
    """Verify priority handles invalid strings (defaults them to Medium/1)"""
    owner = Owner("A", "B", 30)
    pet = Pet("Dog", 2, "healthy")
    owner.add_pet(pet)
    today = date(2023, 10, 1)
    
    # High is level 0, Low is level 2. "urgent" is invalid, so it falls back to 1 (Medium).
    t_high = Task("High", time(9,0), "daily", False, today, priority="high")
    t_invalid = Task("Invalid", time(8,0), "daily", False, today, priority="urgent") 
    t_low = Task("Low", time(7,0), "daily", False, today, priority="low") 
    
    pet.add_task(t_high)
    pet.add_task(t_invalid)
    pet.add_task(t_low)
    
    scheduler = Scheduler(today, owner=owner)
    result = scheduler.check_calendar()
    
    # Order should be High(0), Invalid(defaulted to 1), Low(2)
    assert result == [t_high, t_invalid, t_low]


def test_scheduler_past_dates_excluded():
    """Verify that tasks from previous or future dates are excluded from today's schedule"""
    owner = Owner("A", "B", 30)
    pet = Pet("Dog", 2, "healthy")
    owner.add_pet(pet)
    today = date(2023, 10, 1)
    past_date = date(2023, 9, 30)
    
    t1 = Task("Past Task", time(8,0), "daily", False, past_date)
    t2 = Task("Today Task", time(9,0), "daily", False, today)
    
    pet.add_task(t1)
    pet.add_task(t2)
    
    scheduler = Scheduler(today, owner=owner)
    result = scheduler.check_calendar()
    
    assert len(result) == 1
    assert result[0] == t2


# --- Specific Requirement Tests ---

def test_sorting_correctness_chronological():
    """Sorting Correctness: Verify tasks are returned in chronological order"""
    owner = Owner(first_name="John", last_name="Doe", age=30)
    pet = Pet(name="Rex", age=2, health_status="healthy")
    owner.add_pet(pet)
    today = date.today()

    t1 = Task("Morning Walk", time(8, 0), "daily", False, today, priority="medium")
    t2 = Task("Evening Feeding", time(18, 0), "daily", False, today, priority="medium")
    t3 = Task("Midday Play", time(12, 0), "daily", False, today, priority="medium")

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    scheduler = Scheduler(date=today, owner=owner)
    result = scheduler.check_calendar()

    assert result == [t1, t3, t2]


def test_recurrence_logic_next_day():
    """Recurrence Logic: Confirm that marking a daily task complete creates a new task for the following day"""
    pet = Pet(name="Mochi", age=3, health_status="healthy")
    task_date = date(2023, 10, 1)
    task = Task(description="Walk", time_due=time(8,0), frequency="daily", completion_status=False, date_due=task_date)
    pet.add_task(task)
    
    task.mark_complete()
    
    # Original is complete
    assert task.completion_status is True
    
    # A new task was generated for the next day
    assert len(pet.tasks) == 2
    new_task = pet.tasks[-1]
    assert new_task.date_due == date(2023, 10, 2)
    assert new_task.completion_status == False
    assert new_task.description == "Walk"


def test_conflict_detection_duplicate_times():
    """Conflict Detection: Verify that the Scheduler flags duplicate times"""
    owner = Owner(first_name="John", last_name="Doe", age=30)
    pet1 = Pet(name="Rex", age=2, health_status="healthy")
    pet2 = Pet(name="Mochi", age=3, health_status="healthy")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    today = date.today()
    
    # Same exact time
    t1 = Task("Morning Walk", time(8, 0), "daily", False, today)
    t2 = Task("Give Meds", time(8, 0), "daily", False, today)
    # Different time
    t3 = Task("Evening Feed", time(18, 0), "daily", False, today)
    
    pet1.add_task(t1)
    pet2.add_task(t2)
    pet1.add_task(t3)
    
    scheduler = Scheduler(date=today, owner=owner)
    
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 1
    assert "8:00" in conflicts[0] or "08:00" in conflicts[0] 
    assert "Rex: Morning Walk" in conflicts[0]
    assert "Mochi: Give Meds" in conflicts[0]



