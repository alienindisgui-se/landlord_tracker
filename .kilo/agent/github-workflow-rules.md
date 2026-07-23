# GitHub Workflow Rules

You are responsible for keeping my GitHub Project (alienindisgui-se/projects/2) in sync with my coding tasks.

## Workflow Logic
My GitHub project is configured with automatic workflows. You do not need to manually add items to the project or move them between statuses.

## Your Responsibilities:
1. **Task Creation:** When I ask you to "create a task", create a GitHub issue via terminal:
   `gh issue create --title "<Task Title>" --body "<Detailed Description or Context>"`
   - GitHub will automatically add this issue to Project 2.

2. **Linking PRs:** When working on a feature, always create a branch and then a Pull Request. You MUST include the keyword "Closes #<ISSUE_NUMBER>" in the PR body.
   - Example: `gh pr create --title "Fix: <Feature Name>" --body "Closes #123"`
   - GitHub will automatically link this PR to the issue and move the item on the project board based on the "Pull request linked to issue" workflow.

3. **Status Management:** Do not attempt to use `gh project` commands to change status. Instead, ensure your PRs are correctly linked (using "Closes #...") and let the project's native automation handle the status transitions.
