from fastapi import HTTPException

# Define the valid status transition matrix
VALID_TRANSITIONS = {
    "ToDo": {"InProgress"},
    "InProgress": {"Done", "ToDo"},
    "Done": {"InProgress"}  # Allow moving back to InProgress if task needs rework
}

def validate_status_transition(current_status: str, new_status: str):
    """
    Validates if a task can transition from current_status to new_status.
    Raises an HTTPException (400 Bad Request) if the transition is invalid.
    """
    # If the status isn't changing, it is always valid
    if current_status == new_status:
        return

    # Check if current status exists in our matrix
    if current_status not in VALID_TRANSITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid current status: '{current_status}'"
        )

    # Validate the transition
    allowed_next_states = VALID_TRANSITIONS[current_status]
    if new_status not in allowed_next_states:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: '{current_status}' -> '{new_status}' is not allowed."
        )