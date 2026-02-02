## GitHub Copilot: Comprehensive Technical Analysis

GitHub Copilot is an AI-assisted pair programmer engineered by GitHub (Microsoft) that operates across multiple environments—code editors, terminal interfaces, and the GitHub web platform. This report synthesizes documentation-based analysis of the tool's architecture, capabilities, limitations, and operational integration patterns for professional software development workflows.

### Overview and Core Architecture

GitHub Copilot functions as a large language model wrapper operating in a request-response pipeline that processes context and generates code suggestions. The system consists of several discrete components: the user-facing client (IDE extension, web interface, or CLI), a security proxy layer hosted on GitHub-owned Microsoft Azure infrastructure, content filtering systems, and the underlying language models. [docs.github](https://docs.github.com/en/copilot/get-started/what-is-github-copilot)

When a developer triggers a suggestion (e.g., by pausing while typing), the surrounding code—typically 100-300 lines of context from open editor tabs—is pre-processed and combined with metadata such as the current filename, open file extensions, and cursor position. This enriched prompt is transmitted to the proxy, where it undergoes filtering for toxic language, prompt injection attempts, and irrelevance to coding. Assuming the checks pass, the prompt is sent to the selected language model. [docs.github](https://docs.github.com/en/copilot/responsible-use-of-github-copilot-features/responsible-use-of-github-copilot-code-completion)

The model generates a response, which is then post-processed: tested for code quality (detection of common vulnerabilities like SQL injection and XSS), scanned for unique identifiers (email addresses, API keys, IP addresses), and optionally checked for matches against public GitHub repositories if the developer has enabled public code matching detection. The final suggestion is returned to the user as ghost text—visually distinct, non-committal inline text that only enters the file upon explicit acceptance. [resources.github](https://resources.github.com/learn/pathways/copilot/essentials/how-github-copilot-handles-data/)

This architecture establishes a critical operational principle: **inline code completions are ephemeral**. Prompts used to generate inline suggestions are discarded immediately; they are not retained for model retraining when using Copilot in IDEs. In contrast, Copilot Chat and CLI interactions retain conversation history to maintain continuity across sessions, but GitHub has stated that chat prompts are also not retained for retraining of foundational models. [resources.github](https://resources.github.com/learn/pathways/copilot/essentials/how-github-copilot-handles-data/)

### Supported Development Environments and Languages

Copilot operates natively across widely used IDEs, reflecting GitHub's strategy to minimize friction during adoption. [docs.github](https://docs.github.com/copilot/using-github-copilot/getting-code-suggestions-in-your-ide-with-github-copilot)

| **Environment**        | **Status**             | **Notes**                                                 |
| ---------------------- | ---------------------- | --------------------------------------------------------- |
| **Visual Studio Code** | Fully supported        | Extensions auto-install on first launch                   |
| **Visual Studio**      | 2022 v17.8+ required   | v17.10+ includes built-in integration                     |
| **JetBrains IDEs**     | Full suite supported   | IntelliJ IDEA, PyCharm, WebStorm, Rider, RubyMine, others |
| **Xcode**              | Supported              | macOS development workflows                               |
| **Eclipse**            | Supported              | Cross-platform environments                               |
| **Azure Data Studio**  | Supported              | Database development context                              |
| **Vim/Neovim**         | Supported              | v9.0.0185+ (Vim), v0.6+ (Neovim)                          |
| **Windows Terminal**   | Terminal Chat (Canary) | Command-line interface                                    |
| **GitHub Web**         | Copilot Chat           | Browser-based PR review, documentation                    |
| **GitHub Mobile**      | Chat interface only    | Limited mobile capability                                 |

Linguistically, Copilot supports over 30 programming languages. The tool performs optimally on well-represented languages in its training data: **Python, JavaScript, TypeScript, Ruby, Go, C#, and C++** receive documented best-in-class support. The model includes training coverage for Java, Kotlin, Scala, PHP, Rust, Swift, C, Shell, CSS, HTML, and markup languages (Dockerfile, Markdown, LaTeX). For languages with sparse public repository representation—such as Cobol, Haskell, or domain-specific languages—suggestion quality degrades predictably. [docs.github](https://docs.github.com/en/copilot/concepts/completions/code-suggestions)

Importantly, language quality is not uniform across all Copilot features. Code completion, chat, and the coding agent may perform differently on the same language based on which model variant is used and how the feature was fine-tuned.

### Feature Taxonomy and Operational Patterns

Copilot consists of distinct, sometimes independently toggled features. [docs.github](https://docs.github.com/en/copilot/get-started/features)

**Inline Code Completions (Code Autocomplete)**
- Real-time suggestions as you type, appearing as ghost text
- Triggered by pausing or explicit hotkey invocation (typically Ctrl/Cmd+Enter)
- Can accept entire suggestions or partial completions
- Best suited for routine boilerplate, method/function completion, and simple algorithmic scaffolding
- Governed by separate model selection from Chat features

**Copilot Chat (Conversational AI)**
- Natural language Q&A interface within IDEs and on GitHub.com
- Available in VS Code, Visual Studio, JetBrains, Eclipse, Xcode, and browser
- Can reference selected code, open files as context, or previous messages in a session
- Supports predefined commands: `/tests` (generate test suites), `/explain` (code explanation), `/fix` (bug fixing), `/refactor` (refactoring suggestions)
- Different feature set on GitHub.com vs. in IDEs (GitHub.com has broader repository context but fewer edit capabilities)

**Copilot Edits (Multi-file Edit Mode)**
- Available in VS Code, Visual Studio, and JetBrains IDEs
- Two operational modes:
  - **Edit Mode**: User selects specific files; Copilot proposes changes incrementally with user review after each iteration
  - **Agent Mode**: Copilot determines files to modify autonomously, iterating without pause until the task is complete
- Edits are local; user approves before committing

**Copilot CLI**
- Terminal-native interface accessible via `copilot` command (public preview)
- Operates in interactive or programmatic mode
- Can autonomously modify files and execute shell commands with user approval gates
- Supports task delegation to Copilot coding agent on GitHub with `/delegate` command
- Access requires Pro, Pro+, Business, or Enterprise plans

**Copilot Coding Agent**
- Autonomous task executor operating in GitHub Actions environment (not locally)
- Triggered by assigning GitHub issues to @copilot or requesting PR creation from chat
- Creates branches with `copilot/*` namespace; cannot merge PRs (human approval mandatory)
- Logs all changes and actions; co-authors commits for compliance attribution
- Can iterate based on PR review comments from humans
- Model selection is available for Pro/Pro+; Business/Enterprise currently default to Claude Sonnet 4.5, with broader selection rolling out

**Code Review Integration**
- Request Copilot review on any PR in seconds (typically <30 seconds)
- Provides automated feedback with suggested code edits
- Can be configured with repository-level custom instructions to enforce style, security, or domain practices
- PR review summary generation (AI-generated summary of changes and focus areas)

**Copilot Spaces**
- User-created or organization-shared contexts combining code, documentation, images, and notes
- Can be shared privately, with specific users, or publicly (read-only)
- Grounds Copilot Chat responses to specific task context, reducing hallucination
- Any Copilot user (including Free) can create personal spaces; no special permissions required

### Pricing, Tiers, and Model Access

GitHub offers five distinct Copilot plans, each with different feature availability and usage quotas. [docs.github](https://docs.github.com/en/copilot/get-started/plans)

| **Plan**       | **Price**      | **Inline Suggestions** | **Chat Messages** | **Premium Requests/mo** | **Available Models**    | **Target User**                |
| -------------- | -------------- | ---------------------- | ----------------- | ----------------------- | ----------------------- | ------------------------------ |
| **Free**       | $0             | 2,000/month            | 50/month          | 50                      | Included only           | Exploratory/learning           |
| **Pro**        | $10/month      | Unlimited              | Unlimited         | 300                     | Included + some premium | Active individual developer    |
| **Pro+**       | $39/month      | Unlimited              | Unlimited         | 1,500                   | Full access             | AI power user/researcher       |
| **Business**   | $19/user/month | Unlimited              | Unlimited         | 300/user                | Included + some premium | Team/organizational deployment |
| **Enterprise** | $39/user/month | Unlimited              | Unlimited         | 1,000/user              | Full access             | Large-scale governance         |

"Premium requests" are usage units consuming against quota. Certain features (e.g., use of advanced models like Claude Opus 4.5 or gpt-5-codex) consume premium requests at different rates. Free and Pro tier users can purchase additional premium requests at $0.04 USD per request.

Students, teachers, and open source maintainers qualify for free Pro tier access.

### AI Model Selection and Differentiation

A distinguishing operational capability of Copilot is user-selectable language models, though availability varies by tier and context. [docs.github](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/use-copilot-agents/coding-agent/changing-the-ai-model)

**Available Models (as of Jan 2026):**

For **Inline Code Completions**: gpt-4.1, gpt-5-codex, gpt-5.1-codex, gpt-5.2-codex, gpt-5.1-codex-mini, Grok Code Fast 1, Raptor mini.

For **Copilot Chat**: Claude Haiku 4.5, Claude Sonnet 4.5, Claude Opus 4.5, GPT-5, GPT-5.2, GPT-5-Codex (preview), GPT-5.1-Codex, o3 (thinking model), o4-mini, Grok Code Fast 1, Raptor mini (derived from GPT-5-mini family).

For **Copilot Coding Agent**: Pro/Pro+ users can select from available models; Business/Enterprise plans currently default to Claude Sonnet 4.5, with broader selection rolling out.

Model selection at individual or organizational level is supported in VS Code, Visual Studio, and JetBrains IDEs. The "Auto" selection mode leverages GitHub's heuristic to reduce rate limiting and select optimal models based on task complexity.

**Bring Your Own Key (BYOK)** allows organizations and enterprises to supply API keys from Anthropic, OpenAI, Microsoft Foundry, or xAI, enabling use of custom fine-tuned or proprietary models within Copilot Chat. Organizations configure custom models in settings; users then access these models from the model picker in chat interfaces. [docs.github](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/use-your-own-api-keys)

### Specific Capabilities Differentiating Copilot from General-Purpose AI Tools

1. **IDE-Native Integration with Zero Configuration**: Unlike standalone AI chat applications, Copilot extensions auto-install in Visual Studio Code and are built-in to Visual Studio 2022 v17.10+, eliminating the configuration friction that hampers adoption of external tools. This native embedding means developers never context-switch from code to browser; suggestions appear inline.

2. **Real-Time Inline Suggestions**: Copilot uniquely offers sub-second, position-aware inline code completion as ghost text. This is fundamentally different from chat-based code generation; it operates at the keystroke level, matching the UX paradigm of traditional autocomplete (as in IntelliSense) while powered by LLMs. Developers can accept suggestions with a single keystroke or ignore them by continuing to type. [docs.github](https://docs.github.com/en/copilot/get-started/what-is-github-copilot)

3. **Autonomous Task Execution with GitHub Integration**: Copilot Coding Agent can autonomously work on GitHub issues, execute terminal commands, run CI/CD checks, and propose pull requests in a GitHub Actions environment. This is distinct from LLM-powered editor agents (e.g., Claude's edit mode in VS Code), which operate locally. GitHub integration means the agent has access to issues, pull request history, branch protection rules, and organizational policies—enabling it to respect repository constraints that local agents cannot. [docs.github](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/coding-agent/coding-agent)

4. **Public Code Matching Detection and Attribution**: When Copilot generates a suggestion matching code in public GitHub repositories, it optionally displays the repository URL, license type, and code snippet. This reference capability addresses a real operational concern—developers using Copilot can verify whether a suggestion is a common pattern (e.g., FizzBuzz) or novel synthesis. Competitors often do not surface this. [docs.github](https://docs.github.com/copilot/using-github-copilot/finding-public-code-that-matches-github-copilot-suggestions)

5. **Content Exclusion and Governance Controls**: Organizations can exclude files or directories from Copilot's context at the repository, organization, and enterprise level using fnmatch patterns. Excluded content does not inform code completions, chat responses, or code reviews. This is critical for protecting proprietary algorithms, secrets, or regulated code (e.g., healthcare, finance) from being processed by external LLMs. [docs.github](https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion/excluding-content-from-github-copilot?tool=visualstudio)

6. **Organization and Enterprise Policy Management**: GitHub Business and Enterprise plans include policy controls for feature availability (e.g., enable/disable code review, CLI, Spaces), model access, suggestion matching filtering, audit logging, and seat management. This enables IT/security teams to govern Copilot deployment without manual per-user configuration. [docs.github](https://docs.github.com/en/copilot/how-tos/administer/organizations/managing-policies-for-copilot-in-your-organization)

7. **Copilot Spaces for Context Curation**: Spaces allow teams to assemble code, documentation, images, and notes into task-specific contexts, then share these with collaborators or publicly. Answers grounded in Spaces are more contextually accurate than generic chat. This differs from typical AI assistants, which have no mechanism for persistent, curated context repositories. [docs.github](https://docs.github.com/en/copilot/concepts/context/spaces)

8. **Repository-Level Custom Instructions**: Teams can add `.github/copilot-instructions.md` files to repositories, providing coding standards, architectural patterns, security requirements, or language-specific guidance. Copilot Code Review, Chat, and the Coding Agent can then apply these instructions without per-user configuration. This enables org-wide standardization of AI-generated code to match internal practice. [docs.github](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

### Limitations: Core Constraints and Operational Pitfalls

**Language Representation Asymmetry**
Languages well-represented in public repositories (JavaScript, Python, Go, Rust) receive higher-quality suggestions than niche or domain-specific languages. This is not a bug; it reflects training data distribution. Organizations using minority languages should validate generated code more rigorously. [docs.github](https://docs.github.com/en/copilot/responsible-use/copilot-cli)

**Architectural and Design Blindness**
Copilot cannot see beyond the immediate context provided (typically 100-300 lines). It cannot identify larger design issues, suggest system-wide refactoring, or reason about cross-repository dependencies. It is tactical, not strategic. Large refactoring or architectural changes should not be delegated to the coding agent without explicit, well-scoped issue descriptions. [docs.github](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

**Security Vulnerability Generation**
Copilot can generate code that appears syntactically valid but contains security defects: hardcoded credentials, SQL injection vulnerabilities, unvalidated user input handling, missing error boundaries, or cryptographically weak algorithms. The proxy filters for *obvious* bugs (e.g., hardcoded API keys) and common vulnerabilities, but sophisticated security defects may slip through. Human code review remains mandatory, especially for security-sensitive code. [docs.github](https://docs.github.com/copilot/using-github-copilot/code-review/using-copilot-code-review)

**Potential Biases in Training Data**
Copilot's training data comprises public GitHub repositories, which reflect existing coding patterns, conventions, and mistakes. If a pattern is prevalent in the training set—e.g., a particular (suboptimal) logging idiom—Copilot may reproduce it, normalizing the bias. The tool may also overfit to dominant languages and frameworks (JavaScript/Node.js, Python) and produce weaker suggestions for less common stacks. [docs.github](https://docs.github.com/en/copilot/responsible-use-of-github-copilot-features/responsible-use-of-github-copilot-code-completion)

**Inaccurate Responses to Non-Coding Queries**
Copilot Chat is designed for coding-related questions only. If asked about project management, business logic, or non-technical topics, it may produce irrelevant or nonsensical answers. The tool explicitly disclaims capability for general-purpose knowledge. [docs.github](https://docs.github.com/en/copilot/responsible-use/chat-in-github)

**Public Code Recitation (Low but Non-Zero Probability)**
While GitHub claims the probability is "low," Copilot may occasionally suggest code that closely matches or exactly replicates public examples, particularly for common patterns (e.g., FizzBuzz algorithm). Users can enable public code matching detection to flag and display these instances, but the burden of verification remains on the developer. [docs.github](https://docs.github.com/copilot/using-github-copilot/finding-public-code-that-matches-github-copilot-suggestions)

**Coding Agent Limitations**
- Cannot make changes across multiple repositories in a single task [docs.github](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Model selection for the coding agent varies by plan; Pro/Pro+ can choose models, while Business/Enterprise currently default to Claude Sonnet 4.5 with broader selection rolling out [docs.github](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/use-copilot-agents/coding-agent/changing-the-ai-model)
- Cannot directly merge pull requests; requires human approval [docs.github](https://docs.github.com/en/copilot/tutorials/reduce-technical-debt)
- Can only push to `copilot/*` branches; restricted by repository branch protection rules and required checks [docs.github](https://docs.github.com/en/copilot/tutorials/reduce-technical-debt)
- Requires well-scoped, explicit issue descriptions; vague requirements lead to poor results [docs.github](https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks)
- Cannot run arbitrary Git commands; limited to simple push operations [docs.github](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

**Platform Constraints**
- Copilot CLI is public preview with data protection considerations; subject to change [docs.github](https://docs.github.com/en/copilot/responsible-use/copilot-cli)
- Copilot coding agent only works with repositories hosted on GitHub; no support for GitLab, Bitbucket, or on-premise git servers [docs.github](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Certain repository rulesets or branch protection rules (e.g., "Require signed commits") block Copilot agent access unless the agent is explicitly bypassed [docs.github](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

### Setup, Configuration, and Operational Best Practices

**Installation and Authentication**
Copilot requires a GitHub account with an active subscription (or Free access). IDE extensions authenticate via OAuth to GitHub, inheriting org/enterprise policies and seat assignments. For enterprise-managed accounts, additional setup steps may be required to authenticate from development environments on non-GitHub.com instances. [docs.github](https://docs.github.com/copilot/managing-copilot/configure-personal-settings/installing-the-github-copilot-extension-in-your-environment)

**Language-Specific Configuration**
Individual IDE settings allow per-language enable/disable of Copilot. For example, a developer can disable suggestions in certain file types (e.g., `.txt`, `.json`) to reduce noise while keeping suggestions active in `.py` and `.js` files. Configuration is managed in IDE settings or via `github-copilot.xml` (JetBrains) or VS Code settings files. [github](https://github.com/github/docs/blob/main/content/copilot/managing-copilot/configure-personal-settings/configuring-github-copilot-in-your-environment.md)

**Effective Prompting for Chat and Completions**
- **Be specific and scoped**: "Write a function to validate email addresses" > "Write code"
- **Provide context through surrounding code**: Open related files in editor tabs; Copilot uses them as implicit context [docs.github](https://docs.github.com/en/copilot/tutorials/write-tests)
- **Use comments to guide code completions**: Comments like "// Use quicksort algorithm" or "// Return a Set to avoid duplicates" steer Copilot toward preferred implementations [docs.github](https://docs.github.com/en/copilot/responsible-use-of-github-copilot-features/responsible-use-of-github-copilot-code-completion)
- **For test generation**: Explicitly request edge cases, exception handling, and boundary conditions; Copilot's default test coverage is often incomplete without explicit guidance [docs.github](https://docs.github.com/en/copilot/tutorials/write-tests)
- **For debugging**: Paste error messages and stack traces into Copilot Chat; provide minimal reproducible examples

**Code Review Workflow**
- Request Copilot review on PRs to identify common issues (missing error handling, hardcoded values, performance concerns)
- Use Copilot review as a *first pass*, not final authority; implement custom instructions to enforce org standards
- Manually review all security-critical code; Copilot's security suggestions are not exhaustive [docs.github](https://docs.github.com/en/copilot/tutorials/optimize-code-reviews)
- Combine Copilot code review with static analysis tools (CodeQL, SonarQube) for comprehensive coverage

**Testing and Quality Assurance**
- Use `/tests` slash command to generate test suites; always review for coverage gaps
- Copilot generates unit tests well; integration tests and end-to-end tests often require manual refinement [docs.github](https://docs.github.com/en/copilot/tutorials/write-tests)
- Validate generated tests execute correctly and cover documented requirements, not just Copilot's assumptions
- For complex test scenarios, provide existing test files as context (open in editor tabs) so Copilot matches your testing framework conventions

**Coding Agent Task Definition**
Well-scoped issues yield better results. Include:
- Clear problem statement
- Acceptance criteria (what constitutes "done")
- Pointers to relevant files or architectural docs
- Constraints or build/test commands (e.g., "Run `npm test` before marking complete")
- Custom instructions in `.github/copilot-instructions.md` specifying coding style, security checks, or dependencies [docs.github](https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks)

### Data Privacy and Trust

**Data Handling and Retention**
- Inline code completions: Prompts are **not retained** for model retraining. They are discarded after suggestion generation when using Copilot in IDEs.
- Chat/CLI: Prompts are **retained for session continuity** but not for foundational model retraining.
- Public code matching: When enabled, suggestions are checked against ~150 characters of surrounding code against GitHub's public repository index.
- Toxic language and prompt injection filtering occurs on the proxy layer before transmission to LLMs. [resources.github](https://resources.github.com/learn/pathways/copilot/essentials/how-github-copilot-handles-data/)

**Content Exclusion**
Repository, organization, and enterprise administrators can exclude files and paths from Copilot processing. Excluded content will not inform suggestions, chat responses, or code reviews. This is critical for protecting proprietary algorithms or regulated code. [docs.github](https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion/excluding-content-from-github-copilot?tool=visualstudio)

**Public Code Matching**
Developers can configure Copilot to block suggestions matching public code or to display matches with attribution. When enabled, matched suggestions show the repository URL, license type, and code snippet. Users are responsible for validating and attributing matched code according to its license. [docs.github](https://docs.github.com/copilot/using-github-copilot/finding-public-code-that-matches-github-copilot-suggestions)

**Trust Center Documentation**
GitHub publishes detailed privacy principles and data handling practices in the GitHub Copilot Trust Center, specifying security controls, compliance frameworks, and audit mechanisms. Organizations should review this for regulatory and compliance requirements. [docs.github](https://docs.github.com/site-policy/privacy-policies/github-copilot-business-privacy-statement)

### Practical Workflows and Integration Patterns

**Rapid Prototyping**
Copilot excels at generating boilerplate and scaffolding. For green-field projects, use inline suggestions and Chat to quickly generate class stubs, API endpoints, and standard patterns. Follow up with design review and security validation.

**Refactoring**
Use Copilot Chat to identify performance bottlenecks, suggest algorithmic improvements, or propose refactoring for code quality. For large-scale refactoring, scope tasks tightly and assign to Copilot Coding Agent in small batches. Use PR review comments to steer iterations.

**Onboarding and Documentation**
Create Copilot Spaces for each project containing README, architecture diagrams, and key files. New team members can ask Copilot questions grounded in the Space, reducing context-switching and ramp-up time.

**Multi-Model Experimentation**
For complex tasks (e.g., LLM-based code analysis), experiment with different models (Claude Sonnet 4.5 vs. gpt-5-codex) to find which performs best on your codebase. Some models favor certain languages or coding paradigms.

**Audit and Compliance**
Organizations can review Copilot usage via audit logs and usage dashboards. Track which features are used, by whom, and when. Use this data to identify bottlenecks in adoption or misuse patterns.

### Conclusion

GitHub Copilot is operationally mature for inline code completion and chat-based coding assistance, with well-defined IDE integration, multi-model support, and governance controls suitable for enterprise deployment. Its autonomous coding agent (Copilot Coding Agent) introduces workflow automation—delegating routine tasks—but remains bounded by repository scope, design blindness, and security limitations.

Differentiation from general-purpose LLM chat tools (e.g., ChatGPT, Claude) stems from IDE embedding, public code attribution, governance policies, and GitHub platform integration. These address the operational needs of software teams—reducing context-switching, managing security/compliance, and enforcing team standards—that generic chat interfaces do not.

Critical limitations—inability to reason about system-wide architecture, residual security vulnerability generation, and training data biases—mean human review remains mandatory. Copilot is best used as a pair programmer for tactical tasks (completion, boilerplate, testing, refactoring), not as a design authority or security validator.

***

**Sources referenced:** [github](https://github.com/features/copilot/cli)
