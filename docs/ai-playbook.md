# Personal AI Playbook

## When I reach for AI first
- Drafting repetitive boilerplate code (e.g., standard FastAPI endpoints or Pydantic models).
- Generating initial CI workflow YAML syntax and Dockerfile templates.
- Writing test suite assertions and edge-case test parameters.
- Auditing local terminal errors and formatting markdown documentation templates.

## When I do not reach for AI first
- Making architectural decisions that alter the core scope of the application.
- Analyzing sensitive system paths, passwords, or credentials.
- Debugging path casing or environment issues where local manual inspection is faster.

## My non-negotiables
- **Zero Credentials:** Never paste `.env` contents, enterprise paths, or private credentials into prompts.
- **Scope Discipline:** Never accept unrequested features (e.g., auth, third-party databases) that cause scope creep.
- **Execution Verification:** Every line of code proposed by AI must be verified by running `pytest -v` or testing endpoints manually before committing.

## My review rules
1. **Diff First:** Always inspect `git diff` before accepting AI modifications.
2. **Grade Output:** Categorize AI suggestions as Useful, Noise, or Wrong.
3. **Reject Overengineering:** Immediately reject suggestions that add unnecessary complexity or violate single-container deployment rules.

## What I am still figuring out
- Optimizing prompt context length to get precise fixes without feeding irrelevant codebase files.
- Balancing automated security linting with manual verification in CI pipelines.

## Decision Card
| Trigger Task | Strategy |
|---|---|
| New Feature | Reject if outside core brief scope. |
| Code Review | Inspect diffs line-by-line; grade findings before applying. |
| Debugging | Copy error logs without environment secrets; test fix locally. |
| Infrastructure | Verify non-root permissions and network host bindings. |
| Never-Paste Rule | No credentials, `.env` values, API tokens, or proprietary paths. |
| Golden Rule | I own every single line of code merged into `final-project`. |
