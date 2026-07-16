from fastapi import HTTPException, status

# Allowed workflow transitions on the Kanban board
VALID_TRANSITIONS = {
    ("ToDo", "InProgress"),
    ("InProgress", "Done"),
    ("Done", "InProgress")
}

def validate_status_transition(current_status: str, new_status: str) -> None:
    """Raise HTTP 422 if the status transition is invalid."""
    if current_status == new_status:
        return
    if (current_status, new_status) not in VALID_TRANSITIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid transition from {current_status} to {new_status}."
        )