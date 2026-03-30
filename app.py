import streamlit as st
from datetime import date, time
from pawpal_system import Task, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize owner in session state once
if "owner" not in st.session_state:
    st.session_state.owner = Owner(first_name="Jordan", last_name="", age=0)

st.title("🐾 PawPal+")

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.first_name)
st.session_state.owner.first_name = owner_name

st.divider()

# --- Add Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, age=pet_age, health_status=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added to {owner_name}'s pets!")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([
        {"Name": p.name, "Species": p.health_status, "Age": p.age}
        for p in st.session_state.owner.pets
    ])

st.divider()

# --- Add Task ---
st.subheader("Add a Task")

if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time due", value=time(8, 0))
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
    with col4:
        task_date = st.date_input("Date due", value=date.today())

    if st.button("Add Task"):
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        new_task = Task(
            description=task_title,
            time_due=task_time,
            frequency=frequency,
            completion_status=False,
            date_due=task_date,
        )
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}!")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    schedule = st.session_state.owner.view_schedule()
    if schedule:
        st.write(f"Schedule for {date.today()}:")
        st.table([
            {
                "Pet": task.pet.name if task.pet else "Unknown",
                "Task": task.description,
                "Time": task.time_due.strftime("%I:%M %p"), # time formatting I for 12 hrs, M for min and P for am/pm
                "Frequency": task.frequency,
                "Done": "Yes" if task.completion_status else "No",
            }
            for task in schedule
        ])
    else:
        st.info("No tasks scheduled for today.")
