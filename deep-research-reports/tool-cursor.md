# Cursor: A Technical Reference Guide for Production Software Engineering

## Overview

Cursor is an AI-first code editor built on the Visual Studio Code architecture, designed to streamline multi-file code generation, editing, and project-wide refactoring through integrated autonomous AI agents. Unlike traditional AI coding assistants that operate as overlays or extensions, Cursor consolidates code completion, chat-based editing, codebase navigation, and terminal command generation into a unified IDE with persistent context management and configurable AI governance.

The tool is particularly suited for engineering contexts requiring multi-file coordination, such as feature implementation across multiple services, large-scale refactoring, debugging distributed systems, and test-driven development workflows. This guide covers documented functionality, operational patterns, security considerations, and practical trade-offs for teams evaluating Cursor against alternative approaches.

***

## Architecture and Deployment Model

Cursor is a standalone IDE, not a VS Code extension. This architectural choice provides several technical implications:

**Code-First Integration**: The IDE is built on VS Code's codebase and inherits its extension system, theme support, and keyboard bindings. Teams can import existing VS Code configurations directly—themes, keybindings, and 99% of extensions work without modification. This eliminates vendor lock-in at the UI configuration layer.

**Local Processing and Privacy Considerations**: Cursor creates embeddings of indexed codebases without storing filenames or source code on Cursor servers. Filenames are obfuscated, and code chunks are encrypted before transmission. When agents search the codebase, Cursor retrieves encrypted embeddings and decrypts locally. However, indexed codebases are deleted after 6 weeks of inactivity, requiring re-indexing if a project goes dormant.

**Network Isolation in Privacy Mode**: Cursor offers a Privacy Mode for enterprise deployments that prevents data retention by model providers (OpenAI, Anthropic, Google, xAI Grok). When enabled, prompts and code are not logged for product improvement, though this may affect response optimization.

***

## Core Feature Set and Operational Patterns

### Tab: Contextual Autocompletion

Tab is Cursor's custom-trained autocomplete model that extends beyond single-line suggestions. It operates on a reinforcement learning loop: accepting suggestions (Tab key) or rejecting them (Escape) trains the model to understand your coding patterns and project structure.

**Key behaviors**:
- Multi-line edits: Tab can generate edits spanning multiple lines or across file boundaries with a single keystroke.
- Auto-import detection: In TypeScript and Python, Tab automatically suggests missing import statements when you reference a function from another module.
- Context-aware: Tab observes recent edits, linter errors, and accepted suggestions to predict your next action.
- Cross-file coordination: Tab can suggest edits in related files simultaneously (e.g., updating a function signature in one file and its call sites in others).

**Configuration and constraints**:
- Tab can be disabled globally, for specific file extensions (e.g., Markdown, JSON), or temporarily via a snooze feature.
- Suggestion filtering in comments can be disabled per-project to reduce noise during documentation writing.
- Partial accepts allow accepting the next word via Ctrl+Arrow-Right for fine-grained control.
- Tab does not apply rules or customs modes—it is independent of project-specific AI guidance.

**Real-world pitfall**: In projects using Python type hints, Tab may suggest imports incorrectly if your language server is misconfigured. Verify that your project's language server extension is installed before relying on auto-import.

### Inline Edit (Ctrl+K): Targeted Code Modification

Pressing Ctrl+K opens a natural language editing interface. When code is selected, Ctrl+K edits only that selection. Without selection, Cursor generates new code at the cursor position, automatically including relevant surrounding context (e.g., if you trigger on a function name, the entire function becomes context).

**Operational modes within Inline Edit**:
- **Edit Selected**: Modify highlighted code based on your instructions.
- **Quick Question**: Press Alt+Enter to ask about selected code without making changes; type "do it" or similar to convert responses to code.
- **Full File Edit**: Ctrl+Shift+Enter for multi-line, large-scale rewrites while maintaining control.
- **Send to Chat**: Ctrl+L escalates to Chat for multi-file edits and more complex reasoning.

**Context inclusion**:
Inline Edit automatically includes default context beyond what you explicitly reference:
- Related files inferred from your selection
- Recently viewed code
- Active linter errors (in Chat mode)
- Definitions of referenced symbols via @Definitions

This implicit context can accelerate small edits but may surface unexpected suggestions. For precise control, explicitly include or exclude context via @ symbols.

**Important limitation**: Inline Edit includes project rules and memories, but Tab completion does not. This means project-specific coding standards (e.g., "always use error handling pattern X") apply to deliberate code edits but not to background suggestions.

### Chat and Agent Modes: Multi-File Autonomy

Chat is Cursor's AI sidebar interface that unified what were previously separate "Composer" and "Chat" features. It operates in three modes:

| Mode       | Purpose                         | Capabilities                                                                          | Control                                                               |
| ---------- | ------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Agent**  | Complex features, refactoring   | Autonomous codebase exploration, multi-file edits, terminal execution, error recovery | Requires approval for terminal commands; file edits saved immediately |
| **Ask**    | Learning, planning, exploration | Search-only, no automatic changes, provides explanations and answers                  | Read-only; can retrieve PRs, commits, git history                     |
| **Custom** | Specialized workflows           | User-defined tool combinations and instructions                                       | Scoped to project or user-level via configuration                     |

**Agent mode execution**:
When you describe a task in Agent mode, the AI autonomously:
1. Searches the codebase for relevant files using semantic indexing.
2. Reads and analyzes them to understand context.
3. Plans changes across multiple files.
4. Edits files and runs tests.
5. Fixes errors and iterates.
6. Applies checkpoints automatically at each step, allowing rollback to previous states.

**Real-world use case**: Adding a new API endpoint requires updating route handlers, middleware, tests, documentation, and deployment configuration. Agent mode can coordinate these changes across a multi-service architecture, running tests after each change to verify continuity.

**Checkpoints and rollback**:
Cursor creates automatic checkpoints at each Agent request and after every AI-induced file change. To revert, click "Restore Checkpoint" in the chat input or click the plus button on a previous message. This removes the need for manual version control management during exploration.

**Multi-tab conversations**:
Press Ctrl+T to open a new Chat tab. Unlike chat history, tabs execute in parallel and maintain independent context. This is useful for exploring multiple refactoring approaches simultaneously without losing previous work.

***

## Context Management: @ Symbols and Scoping

Cursor uses @ symbols to control what the AI can access and reference. This is the primary mechanism for managing hallucinations and ensuring accuracy in large codebases.

| Symbol           | Function                             | Use Case                                                                                      |
| ---------------- | ------------------------------------ | --------------------------------------------------------------------------------------------- |
| **@Files**       | Reference specific files             | Include only relevant source files, avoiding noise from configuration files or generated code |
| **@Folders**     | Reference entire directories         | Scope context to a backend service, frontend app, or specific domain                          |
| **@Code**        | Reference specific functions/classes | Pin exact implementations without loading entire files                                        |
| **@Docs**        | Reference project documentation      | Ensure AI understands project conventions, architecture, APIs                                 |
| **@Git**         | Access git history and branches      | Ask about recent changes, commits, or implementation patterns from PRs                        |
| **@Web**         | Search external documentation        | Fetch latest framework docs, library examples, or API specifications                          |
| **@Definitions** | Auto-include symbol definitions      | Inline Edit only; includes related code structures automatically                              |
| **@Past Chats**  | Reference summarized conversations   | Restore context from previous sessions without re-explaining                                  |
| **@Lint Errors** | Include linter errors                | Focus AI on fixing specific warnings or violations                                            |

**Codebase indexing**:
Cursor automatically indexes all files except those in `.gitignore` and `.cursorignore`. Configure indexing in `Cursor Settings > Indexing & Docs`. The indexing process creates semantic embeddings, allowing natural-language searches like "How are services initialized?" to return relevant code blocks even if the exact wording doesn't appear in comments.

**Multi-root workspace support**:
Cursor indexes all codebases in a multi-root workspace simultaneously. Each codebase's context is available to AI, and project rules apply across all folders.

**Performance consideration**: In very large codebases (100,000+ lines), semantic search may surface multiple candidate files. Adding specific @ references (e.g., `@backend/services/payment.ts`) narrows results and accelerates reasoning.

***

## Rules System: Persistent AI Governance

Cursor's rules system encodes project-specific knowledge, architectural decisions, and coding standards so they persist across sessions without manual repetition.

### Project Rules (Version-Controlled)

Project rules live in `.cursor/rules/` and are checked into version control:

```
project/
├── .cursor/rules/
│   ├── naming-conventions.mdc
│   ├── error-handling.mdc
│   └── backend/
│       └── .cursor/rules/
│           └── database-patterns.mdc
└── frontend/
    └── .cursor/rules/
        └── component-structure.mdc
```

Each rule is an MDC file (metadata + markdown) with a frontmatter block:

```yaml
---
description: "Error handling pattern for async operations"
globs: ["src/api/**/*.ts"]
alwaysApply: true
---

- Use try-catch blocks for async/await operations
- Always log errors before responding to client
- Return 500 status with minimal error details
```

**Rule types**:
- **Always**: Included in every Agent and Inline Edit operation.
- **Auto Attached**: Included when files matching specified glob patterns are referenced.
- **Agent Requested**: Available to the AI, which decides whether to use them based on relevance.
- **Manual**: Only included when explicitly mentioned via `@ruleName` in chat.

**Nested rules**: Subdirectories can have their own `.cursor/rules` directory, scoped to that folder. This allows backend-specific rules (database queries, RPC patterns) to apply only when working on backend files.

**Limitations**: Rules apply only to Agent mode and Inline Edit. They do not affect Tab completion. This is a deliberate design choice to keep background suggestions fast and responsive.

### User Rules (Global Preferences)

User rules are defined in `Cursor Settings > Rules` and apply globally across all projects. Use these for communication style, general coding preferences, or organization-wide standards:

```
Please write concise responses.
Always use descriptive variable names.
Prefer async/await over callbacks.
```

### Legacy .cursorrules

The `.cursorrules` file in project root is still supported but deprecated. Migrate to Project Rules for better control and visibility.

***

## Model Selection and Multi-Provider Support

Cursor provides access to multiple frontier models and allows custom API keys for self-hosted or proprietary deployments.

**Available models** (as of January 2026):
- Claude Sonnet 4.5, Claude Opus 4.5 (Anthropic)
- gpt-4.1, gpt-5.2 (OpenAI)
- Gemini 2.5 Pro, Gemini 2.5 Flash (Google)
- o3 (OpenAI reasoning model)
- Grok 4 (xAI)

**Model selection strategy**:

| Model                  | Strengths                                                   | Best For                                                                          |
| ---------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Claude Sonnet 4.5**  | Fast, clear instructions, strong directionality             | Precise edits, feature implementation when you know exactly what you want         |
| **Claude Opus 4.5**    | Deep reasoning, asks clarifying questions                   | Complex refactoring, architectural decisions, ambiguous requirements              |
| **Gemini 2.5 Pro**     | Large context window (1M tokens, 2M coming soon), confident decision-making | Processing entire large codebases, multi-file architectural analysis              |
| **o3**                 | Reasoning-focused, slowest but most capable                 | Solving difficult algorithmic problems, hard-to-debug production issues           |
| **Auto**               | Model selection based on task                               | Default choice; detects performance degradation and switches models automatically |

**Custom API keys**:
You can provide your own API keys in `Cursor Settings > Models`. Supported providers:
- OpenAI (standard and reasoning models)
- Anthropic (all Claude models)
- Azure OpenAI (your deployed instances)
- AWS Bedrock (via access keys or IAM roles)

**Important limitation**: Custom API keys work only with standard chat models. Features requiring Cursor-specific models (Tab completion, specialized agents) continue using Cursor's built-in infrastructure.

**Context window sizing**:
By default, Cursor uses a 200k token context window. In Max Mode, context can expand to the full limit supported by the model (1M tokens for Gemini 2.5 Pro with 2M in development, 200k for most others). Max Mode is slower and more expensive; use it for large-scale refactoring or when you need your entire codebase in context.

***

## Terminal Integration and Command Execution

In Cursor's terminal, press Ctrl+K to open a command suggestion bar at the bottom. Describe your action in natural language, and Inline Edit generates a shell command.

**Execution model**:
- Commands run in your login shell ($SHELL environment variable).
- Commands inherit the CLI's working directory and environment variables.
- To run commands in subdirectories, chain with `cd`: `cd src && npm test`.
- Large outputs are automatically truncated; long-running processes timeout to prevent performance degradation.
- Every command is independent—directory changes do not persist between commands.

**Terminal approval and auto-run**:
- By default, every terminal command requires user approval.
- You can enable auto-run, allowing agents to execute all commands without approval. This introduces data exfiltration risk (attackers could trick agents into uploading code to malicious servers).
- Guardrails allow you to specify allowlists (e.g., only permit `npm test`, `git` commands). Cursor explicitly disclaims allowlists as security controls; they are best-effort.
- Troubleshooting: If a shell prompt theme (e.g., Powerlevel10k) interferes with terminal output, disable it during agent runs using the `$CURSOR_AGENT` environment variable check.

**Real-world workflow**: Generate test-fix-verify cycles automatically by enabling auto-run in development environments, but disable it in production deployments.

***

## Memories: Persistent Session Context

Cursor's Memories system automatically extracts and stores important information across development sessions.

**How it works**:
- Cursor uses a sidecar observer model that watches your conversations and automatically creates memories in the background.
- Memories require user approval before being saved, ensuring control over what gets retained.
- Agent can directly create memories via tool calls when you explicitly ask it to remember something or when it detects important information.

**Use cases**:
- "Remember that we use `NotFoundException` for missing resources in all APIs."
- "The auth service runs on port 3001 and uses JWT tokens in the `Authorization` header."
- "We store user preferences in Redis with the key pattern `user:{id}:prefs`."

**Distinction from Rules**:
- **Rules**: Project-wide, version-controlled, architectural guidance. Use for "how we build things."
- **Memories**: Personal notes and session context. Use for "this specific project detail I always forget."

Memories are useful for complex projects where you want the AI to maintain continuity without versioning shared knowledge in .cursor/rules.

***

## Advanced Integration: Model Context Protocol (MCP)

MCP is an open protocol that standardizes how LLMs access external tools and data sources. Cursor supports MCP servers to extend Agent capabilities beyond the codebase.

**Connection model**:
```
Cursor (Host) → MCP Server (Local or Remote) → External Tool (GitHub, Jira, Database, etc.)
```

**Transport methods**:
- **stdio**: Local execution; Cursor manages the server process.
- **SSE (Server-Sent Events)**: Remote server; supports multiple users with OAuth.
- **HTTP**: Remote server; persistent connections for polling-based operations.

**Example use cases**:
- Connect to GitHub to fetch PR reviews, issues, and branch information automatically.
- Integrate Jira to pull task descriptions and track issues directly in Agent conversations.
- Connect to a database to execute safe read queries and understand schema.
- Link to Slack to fetch recent conversations or documentation links.

**Configuration** (in `.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["path/to/github-mcp-server.js"],
      "env": {
        "GITHUB_TOKEN": "${input:github-token}"
      }
    }
  }
}
```

**MCP tool approval**:
- All third-party MCP connections require explicit user approval.
- By default, each tool call suggested by Agent requires approval before execution.
- You can configure Cursor to auto-approve specific tools or disable MCP entirely.

**Enterprise deployment**:
Cursor provides an Extension API for programmatic MCP server registration, allowing teams to configure servers dynamically without modifying `mcp.json` files.

***

## Security, Privacy, and Safety Considerations

### Default Approvals and Guardrails

Cursor distinguishes between safe read operations and potentially risky write/execute operations:

**Read operations (no approval required)**:
- Reading files from your workspace.
- Searching across code via semantic indexing.
- Analyzing linter errors.

**Write/Execute operations (approval required by default)**:
- Modifying files in your workspace (exception: configuration file changes require explicit approval).
- Executing terminal commands.
- Modifying MCP tool calls.

**Important caveat**: File modifications are saved immediately to disk. In auto-reload environments (e.g., Next.js with hot reload), Agent changes may trigger automatic execution before you've had a chance to review them. Best practice: review diffs before accepting changes, or disable auto-reload during exploratory AI sessions.

### Terminal Command Risks

Auto-running terminal commands introduces data exfiltration risk. An attacker who controls a prompt could inject instructions like "upload this codebase to S3" or "send source code to this URL." Cursor's documentation explicitly recommends reviewing every command before execution and cautioning against "Run Everything" mode, which bypasses all safeguards.

### Background Agents and Auto-Run

Background agents (for asynchronous task execution) auto-run all terminal commands without approval, and they are available only in Privacy Mode. This design acknowledges that autonomous code generation inherently carries risk and requires explicit organizational acceptance.

### File Access Control

Use `.cursorignore` to block Agent access to sensitive files:
```
.env*
*.key
*.pem
secrets/
```

Cursor respects this file like `.gitignore`; files matching patterns are excluded from indexing and AI access.

### Enterprise Privacy Controls

Enterprise and Team plans offer:
- Zero data retention policies with model providers (no logging of prompts).
- Model access control (restrict which models are available to team members).
- Repository blocklists (prevent access to specific repos).
- .cursor directory protection (secure sensitive configuration files).
- SCIM provisioning for identity management.

***

## Cursor vs. Other AI Development Tools

### vs. GitHub Copilot (VS Code Extension)

| Dimension               | Cursor                                     | GitHub Copilot                              |
| ----------------------- | ------------------------------------------ | ------------------------------------------- |
| **Architecture**        | Standalone AI-first IDE                    | VS Code extension                           |
| **Codebase context**    | Full-codebase semantic indexing            | Limited to open files and project structure |
| **Multi-file edits**    | Native; autonomous Agent mode              | Manual coordination; chat-based suggestions |
| **Model selection**     | Multiple models; custom API keys           | GitHub backend only                         |
| **Rules/Customization** | Project rules, memories, MCP               | Limited to settings and comments            |
| **Startup latency**     | ~500ms (VS Code + AI systems)              | ~100ms (extension overlay)                  |
| **Cost**                | Free tier; Pro $20/month                   | $10-39/month depending on IDE               |
| **Learning curve**      | Requires understanding modes and @ symbols | Minimal; feels like enhanced autocomplete   |

**When to choose Cursor**: Teams doing large-scale refactoring, multi-service feature implementation, or requiring persistent context and governance.

**When to choose Copilot**: Teams embedded in GitHub/VS Code ecosystem, prioritizing ease of adoption and minimal disruption to existing workflows.

### vs. Claude Web or Other Chat-Based Interfaces

| Dimension               | Cursor                                   | Claude Web (Claude.ai)                         |
| ----------------------- | ---------------------------------------- | ---------------------------------------------- |
| **Context integration** | Direct access to your codebase           | Manual copy-paste or file upload               |
| **Code execution**      | Can modify files, run tests, iterate     | Can only suggest code; you apply it            |
| **Workflow continuity** | Persistent across sessions via Memories  | Manual re-context for each session             |
| **IDE integration**     | Native IDE features (debugging, testing) | External interface; context switching required |
| **Speed**               | Optimized for developer workflow         | General-purpose chat optimized for clarity     |

**When to choose Cursor**: Production engineering requiring tight iteration loops and file system integration.

**When to choose Claude Web**: Research, architectural planning, or writing tests/specs before handing to Cursor for implementation.

***

## Common Workflows and Operational Patterns

### Feature Implementation

1. Create a new Chat tab (Ctrl+T).
2. Describe the feature in natural language: "Add a new GET /api/users/:id endpoint that returns user details and their recent orders."
3. Set Agent mode and reference relevant files: "@backend/routes @backend/services @backend/models".
4. Add project rule: "@api-patterns".
5. Agent searches, reads, plans, generates code across multiple files, runs tests, and fixes errors.
6. Review the checkpoint diffs; accept or revert changes.

### Refactoring Legacy Code

1. Use Ask mode (read-only) to understand existing patterns: "How are error responses currently handled?"
2. Create project rule encoding new pattern.
3. Switch to Agent mode: "Refactor all error handlers in /src/api to use the new pattern."
4. Agent identifies affected files, applies changes in batches, runs tests.

### Debugging Production Issues

1. Inline Edit (Ctrl+K): Select error stack trace; ask "What's causing this error?"
2. Reference recent changes: "@recent-changes" to understand what changed.
3. Ask Agent to search for related issues: "Find all places where this service is called."
4. Write a test to reproduce the issue; iterate until fixed.

### Test-Driven Development

1. Write test in Chat with @test-directory reference.
2. Ask Agent to generate implementation to pass tests.
3. Agent runs tests, iterates on failures, refactors for coverage.

***

## Performance and Real-World Trade-Offs

### Indexing Performance

First-time codebase indexing can take 5-10 minutes for large projects (100k+ lines). Cursor schedules this in the background; you can continue working. Indexing is a one-time cost; subsequent searches are fast.

**Optimization**: Use `.cursorignore` to exclude generated code, node_modules, and build artifacts. This improves indexing speed and search accuracy.

### Large Codebases

Cursor is designed for codebases up to several million lines, but practical limits depend on your hardware:
- **Indexing**: Linear in codebase size; ~1-5 minutes for typical enterprise projects.
- **Search**: Semantic search returns results in <1 second.
- **Context window**: With Max Mode and Gemini 2.5 Pro (2M tokens), you can include your entire codebase in a single Agent request.

**Pitfall**: Including your entire codebase in context for every request is expensive and slow. Use @ symbols and scoped rules to keep context focused.

### Token Consumption and Costs

Cursor includes usage-based pricing aligned with model API rates. For example:
- $20 of included usage on Pro plan.
- Overages billed at model provider rates.
- Using gpt-4.1 (~$15 per million tokens) costs more than Claude Sonnet 4.5 (~$3 per million tokens).

**Practical optimization**: Use Claude Sonnet 4.5 for routine edits; reserve o3 for hard problems. Use Auto mode to let Cursor select the appropriate model.

***

## Limitations and Realistic Assessment

1. **Tab is not context-aware to rules**: Background autocomplete doesn't know about project-specific patterns encoded in .cursor/rules. It learns from your accepted/rejected suggestions.

2. **Indexed codebases expire**: After 6 weeks of inactivity, indexed metadata is deleted. Reopen the project to trigger re-indexing (no additional cost).

3. **MCP complexity**: Setting up MCP servers requires engineering effort. For teams not using external tools, benefits are marginal.

4. **Terminal auto-run security**: Enabling auto-run for terminal commands is a high-risk decision. It's suitable only for isolated environments or teams with strong code review discipline.

5. **Hallucinations persist**: Like all LLM-based tools, Cursor can confidently suggest incorrect patterns or non-existent APIs. Always review generated code, especially in critical systems.

6. **No real-time collaboration**: While Cursor supports team deployments, it is not designed for real-time pair programming. Use VS Code Live Share or other tools for that.

***

## Conclusion

Cursor is a technically mature AI code editor that meaningfully extends developer productivity for multi-file editing, codebase navigation, and autonomous refactoring. Its differentiation—codebase-wide context, multiple models, governance via rules and memories, and MCP extensibility—makes it particularly valuable for teams working on large, complex systems.

The tool is not a replacement for manual engineering; it is a force multiplier for tasks that benefit from AI-driven code generation. Real-world success depends on:
- **Clear specification**: The better you describe the task, the better Agent performs.
- **Iterative review**: Review diffs, test generated code, and iterate.
- **Governance**: Use rules and memories to encode project knowledge so AI learns your patterns.
- **Security discipline**: Understand approval workflows and configure guardrails appropriately for your context.

For teams already invested in VS Code, the transition is smooth. For teams prioritizing raw productivity over tool switching cost, Cursor's embedded AI agent capabilities offer a meaningful advantage over extension-based alternatives.