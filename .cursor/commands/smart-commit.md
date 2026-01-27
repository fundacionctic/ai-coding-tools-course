# Smart Commit

1. **Analyze Commit Style**:
   Run `!git log -n 10 --pretty=format:"%s"` to review the last 10 commit messages.
   Identify the prevailing style (e.g., Conventional Commits like `feat:`, `fix:`, capitalization rules, tense, or emoji usage).

2. **Stage Changes**:
   If specific $FILES are provided, run `!git add $FILES`.
   Otherwise, run `!git add -A` to stage all.
   Then run `!git diff --staged` to understand exactly what is being committed.

3. **Generate Message**:
   Draft a single, concise commit message that describes the staged changes.
   **CRITICAL**: The message MUST strictly follow the style pattern identified in step 1.

4. **Commit**:
   Run `!git commit -m "YOUR_GENERATED_MESSAGE"`.

5. **Safety Constraint**:
   **DO NOT PUSH**. Stop immediately after the commit is created.
   Print the final commit message you used for user verification.
   Do not mention Claude anywhere in the commit message.
