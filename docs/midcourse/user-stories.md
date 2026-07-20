# User Stories

## Feature 1: Tags & Labels

1. **Create Task with Tags**  
   *As a* project manager,  
   *I want to* add comma-separated tags when creating or updating a task,  
   *So that* I can categorize work items by component (e.g., `frontend`, `database`, `urgent`).

2. **Normalize Empty and Whitespace Tags**  
   *As a* developer,  
   *I want* the system to automatically clean up extra spaces and remove empty entries from tags,  
   *So that* the tags remain consistent and clean across the system.

3. **View Tags on Kanban Cards**  
   *As a* team member,  
   *I want to* see visually distinct tag chips rendered on each card on the Kanban board,  
   *So that* I can instantly identify task categories at a glance.

4. **Filter Board by Tag**  
   *As a* QA engineer,  
   *I want to* filter tasks by entering a specific tag in the tag filter box,  
   *So that* I can focus solely on tasks relevant to my current testing focus.

---

## Feature 2: Search & Combined Filters

1. **Search Across Title and Description**  
   *As a* user,  
   *I want to* enter a keyword in the search field to filter tasks by title or description,  
   *So that* I can quickly locate specific tasks without reading every card.

2. **Combine Status and Priority Filters**  
   *As a* team lead,  
   *I want to* filter tasks by combining status (e.g., `ToDo`) and priority (e.g., `High`),  
   *So that* I can isolate urgent tasks that haven't been started yet.

3. **Handle Unmatched Searches Gracefully**  
   *As a* user,  
   *I want* the application to return an empty array with an HTTP 200 status when no tasks match my search,  
   *So that* the interface displays a clean, empty state without breaking.

4. **Validate Filter Input Values**  
   *As an* API consumer,  
   *I want* the backend to return an HTTP 400 or 422 error when an invalid status or parameter is sent,  
   *So that* client applications receive clear validation feedback.