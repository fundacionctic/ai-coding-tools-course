# Markdown Citation Cleanup Skill

## When to use
- Paste reports from Gemini Deep Research with citation numbers (e.g., "sandboxing.2", "prompt for edits/shell.1").
- Markdown tables/text polluted by superscripts (.1, .2, .3).
- Clean before commit or repo integration.

## Target Artifacts
- End-of-sentence: "text.1", "feature.2" → "text", "feature"
- Table cells: "| Isolation | sandboxing.2 |" → "| Isolation | sandboxing |"
- Inline: Preserve Markdown structure; no regex overkill.

## Steps
1. **Scan Content:** Identify all Gemini-style citations: word-ending digits (e.g., `.1`, `.2`, `.3`, `.4`) in tables/paragraphs.
2. **Validate Tables:** Parse Markdown tables; remove citations from cells without breaking pipes/alignment.
3. **Clean Text:** Strip `.N` from sentences; preserve punctuation if separate (e.g., "files.2," → "files,").
4. **Preserve Structure:** Keep headers, lists, bold/italics, links intact.
5. **Examples Check:**
   | Before                                       | After                                      |
   | -------------------------------------------- | ------------------------------------------ |
   | OS-level sandboxing (Filesystem & Network).2 | OS-level sandboxing (Filesystem & Network) |
   | Read-only; prompt for edits/shell.1          | Read-only; prompt for edits/shell          |
6. **Output:** Rewritten clean Markdown; highlight changes as diff.
7. **Done:** Confirm no citations remain.

## Tools/Scripts
- Semantic: "Remove all .1 .2 etc citations from this Markdown."
- Test on selected text or @file.

## Examples
Input table → Clean table without numbers.
