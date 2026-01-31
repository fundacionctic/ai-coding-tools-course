# AI Coding Tools Course

This repository contains documentation and references—primarily AI-generated using the Deep Research feature of Perplexity or Gemini—to support the knowledge base for a 2-hour course focused on AI coding tools and agentic IDEs such as Claude Code, Codex CLI and GitHub Copilot.

## Document Relationships

The following diagram illustrates how the different documents in this repository relate to each other in terms of concepts and contents:

```mermaid
graph TB
    %% Core Concepts
    ASE[agentic-software-engineering-report.md<br/>Technical Foundations & Architectures]
    COMP[agentic-ide-tools-comparison.md<br/>Comparative Analysis 2021-2026]
    
    %% Specific Tools
    CLAUDE[tool-claude-code.md<br/>Claude Code Analysis]
    CURSOR[tool-cursor.md<br/>Cursor IDE Guide]
    COPILOT[tool-github-copilot.md<br/>GitHub Copilot Analysis]
    
    %% Risks & Constraints
    RISKS[llm-risks-research.md<br/>Security Vulnerabilities]
    CONSTRAINTS[llm-constraints-software-engineering.md<br/>Technical & Economic Constraints]
    
    %% Local Solutions
    SOVEREIGN[sovereign-local-llm-ecosystems.md<br/>Privacy-First LLM Systems]
    LOCAL[local-only-setups.md<br/>Hardware Configurations]
    
    %% Enhancement & Support
    ENHANCE[enhancement-ecosystem.md<br/>AI Tools Enhancement Projects]
    DOCS[documentation-tools.md<br/>AI Documentation Platforms]
    MCP[model-context-protocol.md<br/>MCP Architecture]
    
    %% Course Materials
    PROMPT[research-tool.md<br/>Research Prompt Template]
    SLIDES[slides.md<br/>Course Slide Guidelines]
    
    %% Relationships - Core to Tools
    ASE -->|implements| CLAUDE
    ASE -->|implements| CURSOR
    ASE -->|implements| COPILOT
    COMP -->|compares| CLAUDE
    COMP -->|compares| CURSOR
    COMP -->|compares| COPILOT
    
    %% Relationships - Tools to Risks
    CLAUDE -.->|has| RISKS
    CURSOR -.->|has| RISKS
    COPILOT -.->|has| RISKS
    ASE -.->|faces| CONSTRAINTS
    
    %% Relationships - Alternatives
    RISKS -->|motivates| SOVEREIGN
    CONSTRAINTS -->|motivates| SOVEREIGN
    SOVEREIGN -->|requires| LOCAL
    
    %% Relationships - Enhancement
    CLAUDE -->|enhanced by| ENHANCE
    CURSOR -->|enhanced by| ENHANCE
    COPILOT -->|enhanced by| ENHANCE
    ENHANCE -->|uses| MCP
    ASE -->|benefits from| DOCS
    
    %% Relationships - Course Support
    PROMPT -->|generates| ASE
    PROMPT -->|generates| CLAUDE
    PROMPT -->|generates| CURSOR
    PROMPT -->|generates| COPILOT
    SLIDES -->|presents| ASE
    SLIDES -->|presents| COMP
    SLIDES -->|presents| RISKS
    SLIDES -->|presents| SOVEREIGN
    
    %% Styling
    classDef foundation fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef tools fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef risks fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef local fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef support fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef course fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class ASE,COMP foundation
    class CLAUDE,CURSOR,COPILOT tools
    class RISKS,CONSTRAINTS risks
    class SOVEREIGN,LOCAL local
    class ENHANCE,DOCS,MCP support
    class PROMPT,SLIDES course
```

**Legend:**
- **Blue (Foundation)**: Core concepts and comparative analyses
- **Purple (Tools)**: Specific tool implementations
- **Red (Risks)**: Security and constraint analyses
- **Green (Local)**: Privacy-focused alternatives
- **Orange (Support)**: Enhancement and documentation tools
- **Pink (Course)**: Course materials and templates

The diagram shows solid arrows for direct implementation/comparison relationships and dashed arrows for concerns/motivations.

## Markdown Files

- [agentic-ide-tools-comparison.md](./deep-research-reports/agentic-ide-tools-comparison.md) - Comparative analysis of agentic software engineering environments and IDEs (2021-2026)
- [agentic-software-engineering-report.md](./deep-research-reports/agentic-software-engineering-report.md) - Technical foundations, architectures, and enterprise governance frameworks for agentic software engineering
- [documentation-tools.md](./deep-research-reports/documentation-tools.md) - Market landscape report on AI-powered software documentation tools covering repository-level generators, API documentation platforms, and embedded code documentation systems
- [enhancement-ecosystem.md](./deep-research-reports/enhancement-ecosystem.md) - Research on GitHub repositories (200+ stars) that enhance AI coding tools through pre-packaged skills, configuration management, format conversion, and context optimization frameworks
- [llm-constraints-software-engineering.md](./deep-research-reports/llm-constraints-software-engineering.md) - Analysis of technical, economic, and structural constraints of LLMs in software engineering
- [llm-risks-research.md](./deep-research-reports/llm-risks-research.md) - Comprehensive analysis of five high-impact research papers on security vulnerabilities, reproducibility threats, and hidden costs of using LLMs in software engineering
- [research-tool.md](./prompts/research-tool.md) - Prompt template for conducting in-depth research on AI tools using official documentation
- [sovereign-local-llm-ecosystems.md](./deep-research-reports/sovereign-local-llm-ecosystems.md) - Guide to engineering local, privacy-first large language model ecosystems
- [tool-claude-code.md](./deep-research-reports/tool-claude-code.md) - Technical analysis and practical developer guide for Claude Code terminal-native agentic coding tool
- [tool-cursor.md](./deep-research-reports/tool-cursor.md) - Technical reference guide for Cursor AI-first code editor
- [tool-github-copilot.md](./deep-research-reports/tool-github-copilot.md) - Comprehensive technical analysis of GitHub Copilot AI-assisted pair programmer