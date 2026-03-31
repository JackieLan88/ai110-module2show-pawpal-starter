# PawPal+ Project Reflection

## 1. System Design

Three core actions the user should be able to perform in the app are:
check pet's medical records
Make a grooming appointment
Add preferenced veterinary

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For the initial design of the pet app, I have included the 4 main classes: Owner, Pet, Scheduler and Task.
I also thought about adding a class for the owner's preferred vet. Each class does coherently connect with one another giving the primary lead to the owner class. The owner class has a pet and uses the scheduler class to check any current tasks or appointments that are recorded within a calendar. The scheduler class has the ability to manage and create future tasks that the user or owner would like to request for their pet. The pet class and the owner class have basic information such as name and age, however the pet class has more attributes related to health status and medications.

The vet class has attributes regarding the veterinary contact information(name, location, phone number and doctor), where some of the behaviors of this class is to provide prescriptions or checkups when necessary.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

  Yes, the design did change when prompting the AI agent if there was any potential bottlenecks. Claude created clear relationships between objects/classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Previously, in my first draft of the classes, the scheduler would only consider overlapping cases of tasks falling in the same time-slot, however I noticed there are various ways constraints can be seen in this context as I brainstormed with Claude.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Scheduler only provided an output of tasks for one pet when assigning similar tasks to the other pets of an owner. Since tasks are objects, trying to avoid recurrent tasks also neglected the fact of assigning similar tasks to other pets.
A better approach was to refactor the scheduler methods to handle multiple pets simultaneously, creating separate task instances for each pet rather than relying on a single task object. This would enable proper assignment of recurring tasks across all pets while maintaining independent task states.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

During the development of this project, I used AI tools to brainstorm the last details of my design as I felt like there weren't meaningful relationships within my classes. I also learned new features of coding with the streamlit library as I prompted Claude for extra documentation regarding the streamlit functionality.

Some of the prompts and questions that were most helpful was asking Claude to help me built test-cases for the backend logic of our application. I am not a proefficient python code reader however, prompting claude to explain certain blocks of code before continuing to problem solve, allowed me to think twice before implementing a solution, understand the outer perspective of our app, and identify edge-cases that are crucial if they appear for everyday user.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept AI suggestions was when it wanted to modify the init function from the Scheduler class. It specifically wanted to remove some parameters that instantiated the object but also allow a connection towards the Pet and Owner class.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Testing our app is a crucial part before submitting or deploying it. Some of the main behaviors that had to be tested in order for the application to execute successfully were verifying if the user input was received and processed into the different classes; such as storing owner's name and pets, adding tasks/responsabilties the owner has to complete, providing a schedule of all tasks that feature prioritized organization throughout the day.

Another feature that is being tested is checking if there are any existent calendars that the user might already have. The scheduler will then display existent calendar with tasks, given the priority and the scheduled time.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am very confident that the scheduler class will function correctly as the user/owner attempts to add a pet and assign a task to it. One edge case I would've liked testing more, was considering the number of tasks permitted throughout the day, and if there are any tasks the owner might want to delete from their schedule. It would also be great to include if the owner/user missed any tasks with high priority and how the application can alert them.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how well the backend logic integrates with the UI. The organized code structure made it easy to connect the scheduler and class functionalities to the Streamlit interface, and testing confirmed that the visual display works as intended.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

During the development of this project, I was considering having a section where owners could add information of their preferred veterinary. When successfully entering a preferred vet, the owner can now make an appointment for their pets. This feature hasn't been expanded yet, however it is considered within the pawpal_system.py

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One thing I learned about designing systems with AI and being the lead architect is that there are no limits to what you can imagine throughout your application. There will always be small details or ideas you would like to include and we should consider the higher probability edge-cases will appear. AI tools are very efficient when prompting templates or skeletons of functions/classes, but the key takeaway is rooted into always testing what we are given by AI and never accept AI code as the direct solution to the problem.
