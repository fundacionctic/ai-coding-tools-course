# README Markdown Sync Skill

## When to use
- New .md files added anywhere in repo.
- Root README.md missing entries for existing .md files.
- After git commits/pulls with Markdown changes.

## Prerequisites
- Repo has root README.md.
- Target only: All .md files except README.md, .cursor/, .git/, CHANGELOG.md.

## Steps
1. **Scan Repo:** List all .md files recursively: `find . -name "*.md" | grep -v -E "(README.md|.git/|.cursor/|CHANGELOG.md|node_modules/)"` or semantic equivalent [web:31].
2. **Parse README:** Extract "## Markdown Files" section or similar from root README.md; note listed files.
3. **Infer Descriptions:** For each unlisted/new .md:
   - Read full content.
   - Generate 1 concise sentence: topic/purpose (e.g., "Overview of Docker deployment workflow.").
4. **Update README:** Add/append alphabetical list under "## Markdown Files":
