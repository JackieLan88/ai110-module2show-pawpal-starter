from datetime import date, time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Task, Pet


def test_mark_complete_sets_completion_status_true():
	task = Task(
		description="Morning walk",
		time_due=time(8, 0),
		frequency="daily",
		completion_status=False,
		date_due=date.today(),
	)

	task.mark_complete()

	assert task.completion_status is True


	task.mark_complete()

	assert task.completion_status is True


def test_add_task_increases_pet_task_count():
	pet = Pet(name="Mochi", age=3, health_status="healthy")
	initial_count = len(pet.tasks)

	task = Task(
		description="Afternoon walk",
		time_due=time(14, 0),
		frequency="daily",
		completion_status=False,
		date_due=date.today(),
	)

	pet.add_task(task)

	assert len(pet.tasks) == initial_count + 1
	assert task in pet.tasks
	assert task.pet == pet
