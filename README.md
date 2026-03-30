# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling

Allows user to program tasks and reminders at their convenience as they carry their responsibility as pet owners. The app filters schedules by individual pet or completion status, and also detects potential time-slot conflicts across multiple pets without the instant multiple tasks are booked for the exact same time. User also promptly receives organized to-do tasks with meeting due dates and priortization.

### Testing PawPal+
**System Reliability:** ⭐⭐⭐⭐ (4/5 Stars)

Behaviors to verify:

- calendar creation when no calendar is passed into the scheduler class
- Processing existing calendar when passed to scheduler`
- verify what is returned when there is no owner record (instance) passed to scheduler
- Revise if all tasks are sorted by priority and date

#### Test Suite Overview (`test_pawpal.py`)

The test_pawpal file ensures the core scheduling logic works smoothly for the pet owner. It contains detailed tests that target potential edge-cases:

- **Task Updates:** Checks that when you mark a task as "complete," the app actually remembers it's done.
- **Recurring Chores:** Confirms that when you finish a daily or weekly task (like feeding or walking), the app automatically creates the _next_ occurrence for the correct future date
- **Pet Links:** Makes sure that when you assign a task to a pet object, that specific pet's personal to-do list is counted correctly.
- **Organizing the Day:** Verifies that when the app builds your daily schedule, it puts the most important (high-priority) tasks at the top, and then organizes the rest chronologically by time. It also ensures tasks from yesterday or tomorrow don't accidentally overlap with "today's" view.
- **Conflict Warnings:** Tests the system's ability to warn you if you accidentally schedule two different tasks for two different pets at the exact same time
- **Safe Defaults:** Ensures the app doesn't crash in weird situations, such as when a task doesn't have an assigned priority, when starting a brand new empty calendar, or when viewing a schedule that hasn't been linked to a specific user yet.

To test and verify behavior of application features, run the following command:

```bash
python -m pytest
```



