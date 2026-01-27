# Fact-Checker Skill

## When to use
- Verify technical accuracy in documents/directories
- Check software versions are latest (unless specific version stated)
- Audit for hallucinations or gross reality deviations
- Commands: "fact check @docs/", "verify README accuracy"

## Target Input
- Single file: Selected text or @filename
- Directory: @docs/, reports/ (recursively scans .md, .txt)
- Fallback: Current open file

## Steps
1. **Parse Content:** Extract all technical claims, software mentions, version numbers
2. **Version Check:** For each software/tool:
   - No version → Verify against January 2026 latest stable
   - Specific version → Validate claims for that version only
3. **Reality Audit:** Cross-check against known facts:
   - APIs deprecated in 2025+?
   - Companies/projects still exist?
   - Technical limits correct?
4. **Generate Report:**
