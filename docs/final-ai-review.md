# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails
- Repo-specific stack and commands included: Yes
- Docs-first/read-first guardrail included: Yes
- Unexpected app/frontend edits rule included: Yes

## AI Code Review Mini-Log
Reviewed file: `Dockerfile`

| AI Comment | Grade | Reason | Decision |
|---|---|---|---|
| Suggested a conditional shell check (`if [ -f app/main.py ]`) in the `CMD` instruction to handle two possible project layouts | Noise | The project structure is fixed and known -- `app/main.py` always exists in this repo, so the conditional adds unnecessary complexity for a case that will never occur | Flagged for simplification to a direct `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` |
| Added `chown -R appuser:appuser /app` after creating the non-root `appuser` | Useful | Without it, the container crashed on startup -- confirmed via CI logs showing `curl: (7) Failed to connect to 127.0.0.1 port 8000` -- because the non-root user could not write `tasks.db` into a root-owned directory | Accepted; this was the actual fix for a real CI failure |
| Suggested adding explicit `VALID_STATUSES`/`VALID_PRIORITIES` validation to `app/routers.py`'s `get_tasks()` so invalid filter values return 400 instead of silently returning an empty list | Useful | Closed a real gap between documented behavior and actual implementation | Accepted; covered by `test_invalid_status_filter_returns_400` and `test_invalid_priority_filter_returns_400` in `tests/test_tasks.py` |

## AI Security Mini-Review
| Finding | File Evidence | Grade | Reason | Next Action |
|---|---|---|---|---|
| Exposing SQLite DB file in git history | .gitignore | False Positive | tasks.db is already listed in .gitignore. | Retain gitignore rules |
| Container running as default root | Dockerfile | Valid | Hardening required non-root user creation. | Added appuser in Dockerfile |
| Potential hardcoded secret in config | app/database.py | Noise | Local SQLite connection string contains no credentials. | Ignored |

## Manual Security Check
Manually searched the full commit history for leaked secrets by running `git log --all -p | Select-String -Pattern "password|secret|api_key|token"` across every commit in the repository (not just the current file tree), and separately ran `git ls-files | Select-String "\.env"` to confirm no `.env` file has ever been tracked. The first command returned 20 matches, but every one was the word "secret"/"password"/"token" appearing inside my own documentation and rules (e.g. "Secret Isolation," "Never-Paste Rule," "No credentials... into AI prompts," a note that the SQLite connection string "contains no credentials") -- not an actual leaked credential value. The second command returned no results. This matters because the AI security review above only scans the current working tree for obvious patterns; checking full commit history separately closes a real gap an AI pass on the live files alone would miss, e.g. a secret that was committed and later deleted but still recoverable from git history.

## One AI Output I Rejected or Corrected
AI suggested adding JWT authentication and user registration endpoints. I rejected this recommendation to prevent scope creep and keep the application simple and focused on task tracking.

## Three AI Usage Rules
1. Never paste: Passwords, tokens, enterprise paths, or private credentials into AI prompts.
2. Always verify: Run pytest and check endpoint behaviors manually after accepting any AI code snippet.
3. Record AI contributions by: Documenting key prompt interactions and grading AI suggestions in review logs.

## Ownership Statement
I am completely confident submitting this repository as my own work. While AI assisted with formatting, test structure, and security auditing, I personally reviewed, validated, and tested every line of code. I actively rejected suggestions that violated project constraints and understand the complete codebase architecture.

