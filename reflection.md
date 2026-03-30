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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
