import streamlit as st
from datetime import date, time
from pawpal_system import Task, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Define your CSS styling
page_bg_color = """
<style>
/* This targets the main content area */
.stApp {
    background-color: #A3D9FF;
}

/* Labels for all input widgets */
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stTimeInput label, .stDateInput label {
    color: darkblue !important;
}

/* Success message */
div[data-testid="stNotification"],
.stSuccess,
[data-baseweb="notification"] {
    background-color: skyblue !important;
    color: darkblue !important;
}

/* Table borders */
.stTable table, .stTable th, .stTable td {
    border-color: darkblue !important;
    color: darkblue !important;
}

/* Text inside input boxes and selectboxes */
.stTextInput input, .stNumberInput input,
.stTimeInput input, .stDateInput input,
.stSelectbox [data-baseweb="select"] span {
    color: gray !important;
}
</style>
"""

# Inject the CSS into the app
st.markdown(page_bg_color, unsafe_allow_html=True)

# Initialize owner in session state once
if "owner" not in st.session_state:
    st.session_state.owner = Owner(first_name="Jordan", last_name="", age=0)

st.title(":blue[🐾PawPal+]")

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("[Owner name]", value=st.session_state.owner.first_name)
st.session_state.owner.first_name = owner_name

st.divider()

# --- Add Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("[Pet name]", value="Mochi")
with col2:
    species = st.selectbox("[Species]", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("[Pet age]", min_value=0, max_value=30, value=1)

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
    selected_pet_name = st.selectbox("[Assign to pet]", pet_names)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("[Task title]", value="Morning walk")
    with col2:
        task_time = st.time_input("[Time due]", value=time(8, 0))
    with col3:
        frequency = st.selectbox("[Frequency]", ["daily", "weekly", "monthly"])
    with col4:
        task_date = st.date_input("[Date due]", value=date.today())
    with col5:
        priority = st.selectbox("[Priority]", ["high", "medium", "low"], index=1)

    if st.button("Add Task"):
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        new_task = Task(
            description=task_title,
            time_due=task_time,
            frequency=frequency,
            completion_status=False,
            date_due=task_date,
            priority=priority,
        )
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}!")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    schedule = st.session_state.owner.view_schedule()
    conflicts = st.session_state.owner.scheduler.detect_conflicts()

    if conflicts != ["No conflicts found."]:
        for warning in conflicts:
            st.warning(warning)

    if schedule:
        st.write(f"Schedule for {date.today()} (sorted by priority, then time):")
        st.table([
            {
                "Pet": task.pet.name if task.pet else "Unknown",
                "Task": task.description,
                "Priority": task.priority,
                "Time": task.time_due.strftime("%I:%M %p"),
                "Frequency": task.frequency,
                "Done": "Yes" if task.completion_status else "No",
            }
            for task in schedule
        ])
    else:
        st.info("No tasks scheduled for today.")
