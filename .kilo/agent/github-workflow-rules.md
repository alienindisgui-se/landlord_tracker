# GitHub Workflow Rules

You are responsible for keeping my GitHub Project (alienindisgui-se/projects/2) in sync with my coding tasks.

## Workflow Logic
My GitHub project is configured with automatic workflows. You do not need to manually add items to the project or move them between statuses.

## Your Responsibilities:
1. **Task Creation:** When I ask you to "create a task", create a GitHub issue via terminal:
    `gh issue create --title "<Task Title>" --body "<Detailed Description or Context>"`
    - Then immediately add it to Project 2 using:
      `gh project item-add 2 --owner alienindisgui-se --url "https://github.com/alienindisgui-se/landlord_tracker/issues/<ISSUE_NUMBER>"`
    - This is now fully automated after creation.

2. **Linking PRs:** When working on a feature, always create a branch and then a Pull Request. You MUST include the keyword "Closes #<ISSUE_NUMBER>" in the PR body.
   - Example: `gh pr create --title "Fix: <Feature Name>" --body "Closes #123"`
   - GitHub will automatically link this PR to the issue and move the item on the project board based on the "Pull request linked to issue" workflow.

3. **Status Management:** Do not attempt to use `gh project` commands to change status. Instead, ensure your PRs are correctly linked (using "Closes #...") and let the project's native automation handle the status transitions.

## AI Agent Rule: Automated Issue Creation
When the user requests creating a task/issue for the Landlord Tracker project:
1. Use `gh issue create --title "<Task Title>" --body "<Detailed Description>"` to create the GitHub issue
2. GitHub will automatically add the issue to Project 2 (alienindisgui-se/projects/2)
3. No manual project board operations needed - automation handles status
4. Include relevant labels if applicable (e.g., "enhancement", "bug", "feature")
5. Reference any related issues or PRs in the body if needed

## AI Agent Rule: Status Transitions
- **Start Work:** When beginning work on an issue (creating a branch), move the project item from **Todo** to **In Progress** using:
  `gh project item-edit <ITEM_ID> --project-id PVT_kwHOBKEV484BdAA1 --field-id <STATUS_FIELD_ID> --single-select-option-id <IN_PROGRESS_OPTION_ID>`
- **Finish Work:** When a PR linked to an issue is merged to `main`, move the project item to **Done** using:
  `gh project item-edit <ITEM_ID> --project-id PVT_kwHOBKEV484BdAA1 --field-id <STATUS_FIELD_ID> --single-select-option-id <DONE_OPTION_ID>`
- Use `gh project item-list 2 --owner alienindisgui-se` to retrieve the current `<ITEM_ID>` for the issue.
- Use `gh project field-list 2 --owner alienindisgui-se` to discover the `<STATUS_FIELD_ID>` and option IDs for **Todo**, **In Progress**, and **Done**.
