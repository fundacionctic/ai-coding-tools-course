# Fact-Checker Skill

## When to Use
- Verify technical accuracy in documents/directories, including architecture designs.
- Check software versions are latest (unless specific version stated).
- Audit for hallucinations, gross reality deviations, non-consensus architectures, and disputable hard claims.
- Triggers: "fact check @docs/", "verify README accuracy", "audit architecture @design-docs/".

## Target Input
- Single file: Selected text or @filename (e.g., architecture.md).
- Directory: @docs/, reports/ (recursively scans .md, .txt, .yaml).
- Fallback: Current open file.

## Steps
1. **Parse Content:** Extract all technical claims, software mentions, version numbers, architectural patterns (e.g., microservices, scaling), and hard assertions (e.g., "scales infinitely"). Flag potential myths like "monoliths are always simpler" or "architecture optional."

2. **Version Check:** For each software/tool:
   - No version → Verify against January 2026 latest stable (e.g., Kubernetes 1.32+, Docker 27.0).
   - Specific version → Validate claims for that version only.

3. **Reality Audit:** Cross-check against known facts:
   - APIs deprecated post-2025? Companies/projects exist? Limits correct?
   - **Architecture Validation:** Check vs. consensus best practices (NIST SP 500-291r2, ICSA guidelines, DevOps anti-patterns). Flag unbacked designs like rigid monoliths for high-scale or ignoring trade-offs.
   - **Dispute Hard Claims:** Challenge absolutes (e.g., "zero-downtime guaranteed", overstated vendor perf) with contradicting evidence.

4. **Generate Report:**
   - **✅ Verified Claims:** Accurate facts with sources.
   - **⚠️ Potential Issues:** Versions, minor drifts.
   - **🚨 Architectural Flags:** Non-consensus (e.g., "vertical scale first" vs. horizontal baseline).
   - **❌ Disputed Claims:** Contradicted assertions with counters.
   - **Recommendations:** Specific fixes.

   Use Markdown table for clarity:

   | Claim                          | Doc Location | Verdict        | Evidence [cite]                 |
   | ------------------------------ | ------------ | -------------- | ------------------------------- |
   | Monolith for scalability       | arch.md:12   | 🚨 Anti-pattern | Microservices for deploy indep. |
   | Infinite scaling no trade-offs | design.md:5  | ❌ Disputed     | Requires sharding, costs rise.  |
