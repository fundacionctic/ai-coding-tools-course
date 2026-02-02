# Top 5 Most Relevant Research Papers on LLM Risks in Software Engineering

## Executive Summary

This comprehensive analysis identifies and summarizes five high-impact research papers on the risks of using large language models (LLMs) in software engineering. These papers, collectively analyzing over 800 research studies and examining thousands of code generations, reveal critical vulnerabilities spanning security, debugging, reproducibility, and hidden productivity costs. The research uncovers a pervasive **false sense of security** problem where improved metrics mask underlying code correctness issues, widespread **output instability** that undermines reproducibility, and systematic bias toward insecure patterns learned from unvetted training data.

***

## Paper 1: "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions"
**Authors**: Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri  
**Publication**: IEEE S&P adjacent; ArXiv preprint (2021-12-16) [arxiv](http://arxiv.org/pdf/2108.09293.pdf)
**Citation Impact**: Foundational work; frequently cited in subsequent LLM security studies  
**Scope**: 1,689 programs generated across 89 scenarios

### Key Findings on Risks

**Prevalence of Vulnerable Code**: Approximately 40% of GitHub Copilot's generated programs were found vulnerable to CWE (Common Weakness Enumeration) Top 25 vulnerabilities. This finding establishes a quantitative baseline for the security risk posed by widely-adopted AI code assistants. The analysis breaks down by programming language—C code showed the highest vulnerability rate at 50%, followed by Python at 38%, and hardware specification language Verilog at 28%. [arxiv](http://arxiv.org/pdf/2108.09293.pdf)

**False Confidence Problem**: A significant discovery is that vulnerable code frequently receives high confidence scores from the model. Across all scenarios, 44% of the top-scoring (highest-confidence) suggestions generated vulnerable code. This creates a dangerous developer experience where the most "confident" suggestions are statistically likely to contain security flaws. For example, in null pointer dereference scenarios (CWE-476), Copilot assigned confidence scores of 0.96 to vulnerable outputs, demonstrating that model confidence provides no meaningful security guarantee. [arxiv](http://arxiv.org/pdf/2108.09293.pdf)

**Worst Performing Vulnerability Categories**:
- NULL Pointer Dereference (CWE-476): 86% vulnerable
- OS Command Injection (CWE-78): 85% vulnerable  
- Path Traversal (CWE-22): 60% vulnerable
- Out-of-bounds Operations (CWE-787, CWE-125): 47–52% vulnerable [arxiv](http://arxiv.org/pdf/2108.09293.pdf)

**Best Performing Categories**:
- Cross-site Scripting (CWE-79): 19% vulnerable
- Authentication Failures (CWE-306): 20% vulnerable

**Prompt Sensitivity & Debugging Difficulty**: The paper demonstrates that subtle variations in prompt context dramatically alter vulnerability rates. For SQL injection (CWE-89), tweaking nearby code from secure to insecure patterns shifted vulnerability rates from 0% to 94%. This extreme sensitivity makes it virtually impossible for developers to reliably predict when Copilot will generate secure versus vulnerable code, complicating both debugging and quality assurance workflows. [arxiv](http://arxiv.org/pdf/2108.09293.pdf)

**Hidden Costs**: The study identifies that developers face a scrutiny overhead of approximately 40–50% of generated suggestions, as each completion must be manually reviewed for security weaknesses. This overhead substantially offsets the claimed productivity gains, as the time saved by avoiding manual coding is partially consumed by security review burden.

### Methodological Strength

The evaluation employs three axes of analysis:
- **Diversity of Weakness (DOW)**: Tests across 18 distinct CWE categories
- **Diversity of Prompt (DOP)**: Evaluates how context variations affect output  
- **Diversity of Domain (DOD)**: Tests across software (Python/C) and hardware (Verilog) domains

Evaluation uses both automated CodeQL scanning and manual security expert review, ensuring rigor beyond automated analysis alone.

***

## Paper 2: "Constrained Decoding for Secure Code Generation"
**Authors**: Yanjun Fu, Ethan Baker, Yu Ding, Yizheng Chen (Google DeepMind, University of Maryland)  
**Publication**: ArXiv (2024-07-20); journal-quality methodology [arxiv](https://arxiv.org/abs/2405.00218)
**Citation Impact**: Recent (2024); introduces new evaluation paradigm; introduces CODEGUARD+ benchmark  
**Scope**: 91 prompts across 34 CWEs; 8 state-of-the-art Code LLMs evaluated

### Key Findings on Hidden Risks and False Sense of Security

**The False Sense of Security Problem**: This paper makes the critical discovery that previous security evaluation metrics drastically overestimate code safety. The widely-used SVEN Security Rate metric (from prior SOTA work) ignores functional correctness. When evaluating state-of-the-art defense techniques like prefix tuning, the paper demonstrates:

| Metric                          | CodeGen + Prefix Tuning | Baseline CodeGen |
| ------------------------------- | ----------------------- | ---------------- |
| SVEN Security Rate (old metric) | 71.91%                  | 53.65% (+18%)    |
| secure-pass@1 (new metric)      | 29.14%                  | 26.07% (+3%)     |

The old metric suggested prefix tuning provided an 18% improvement in security. The new secure-pass@1 metric—which evaluates both correctness AND security—reveals only 3% improvement. The paper further demonstrates that prefix tuning sacrifices functional correctness (pass@1 decreases by 6.94%), generating "trivially safe" code like comments-only completions that no developer would accept. [arxiv](https://arxiv.org/abs/2405.00218)

**Trade-off Between Security and Correctness**: A fundamental finding is that existing defenses achieve security by sacrificing correctness, creating an untenable trade-off. The new metrics (secure-pass@k and secure@kpass) explicitly measure this two-dimensional performance space, exposing prior work's limitations. [arxiv](https://arxiv.org/abs/2405.00218)

**Vulnerability Rate Among Leading Models**: Across the CODEGUARD+ benchmark of 91 prompts covering 34 CWE types:
- CodeGen-2.7B: secure-pass@1 = 26%–51% (depending on decoding method)
- CodeLlama-34B: secure-pass@1 = 61%
- GPT-4 (Nucleus Sampling): secure-pass@1 = 47.5% [arxiv](https://arxiv.org/abs/2405.00218)

All leading models fail to generate secure and correct code more than 51% of the time.

**Decoding Method Sensitivity**: The paper reveals that decoding algorithms dramatically impact security. Beam sampling outperforms nucleus sampling by 7.7% on secure-pass@1 for CodeGen, yet this critical parameter is often treated as a black box by practitioners. No single decoding method is universally superior across all models, requiring per-model tuning. [arxiv](https://arxiv.org/abs/2405.00218)

**Hidden Cost: Metric Misguidance**: Organizations relying on SVEN-SR to assess LLM security would grossly overestimate actual safety, making 2–3x wrong decisions about deployment readiness. This metric gap represents a systemic risk in the broader industry adoption of code LLMs.

### New Benchmarks and Evaluation Framework

The paper introduces **CODEGUARD+**—a benchmark with:
- 91 prompts (vs. 54 in prior SVEN)
- 34 CWEs (vs. 18 prior)
- Unit tests for functional correctness (vs. none prior)
- Metrics explicitly combining security + correctness [arxiv](https://arxiv.org/abs/2405.00218)

This benchmark is released open-source, enabling future reproducibility and comparison.

***

## Paper 3: "Breaking the Silence: the Threats of Using LLMs in Software Engineering"
**Authors**: June Sallou, Thomas Durieux, Annibale Panichella (TU Delft)  
**Publication**: ICSE-NIER 2024 (ACM/IEEE, top-tier venue) [arxiv](https://arxiv.org/pdf/2312.08055.pdf)
**Citation Impact**: Published at ICSE, initiating community-wide discussion on reproducibility threats  
**Scope**: Empirical study on ChatGPT-3.5; guidelines for researchers and LLM providers

### Key Findings on Reproducibility and Hidden Validity Threats

**Three Primary Threats to Research Validity**: The paper identifies systematic biases in LLM-based SE research:

1. **Data Leakage Between Training and Evaluation**: ChatGPT exhibits precise knowledge of bugs in Defects4J (a widely-used SE benchmark), despite not being fine-tuned for this specific dataset. This knowledge likely derives from pre-training on scientific papers or code repositories. When researchers evaluate LLMs on Defects4J, they are unwittingly testing memorization rather than generalization capability, invalidating external validity claims. [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

2. **Time-Based Output Drift**: The paper documents alarming instability in model outputs over a 3-month period (March–June 2023):
   - GPT-3.5 code generation: 20% mismatch in outputs
   - GPT-4 code generation: 50% mismatch
   - GPT-3.5 executable output rate: drops from 52% to 10%
   - GPT-4 executable output rate: drops from 22% to 2% [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

   This drift occurs due to model retraining, reinforcement learning adjustments, or user feedback integration—all undisclosed to researchers. Reproductions of published results become impossible.

3. **Model Evolution Unpredictability**: Closed-source LLM providers (OpenAI, Google, Anthropic) release new versions without explicit changelogs. Determining whether performance improvements in follow-up research stem from novel techniques or model updates becomes intractable. [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

**Practical Evidence of Data Leakage**: In a case study generating JUnit tests for buggy Defects4J code (Chart-11 and Math-5):
- ChatGPT-3.5 generated 71% branch coverage on original code
- On metamorphically transformed code (renamed methods, removed javadoc), coverage collapsed to near 0%, with hallucinated method calls [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

This dramatic performance drop suggests the model relied on memorized patterns from training data rather than understanding test generation principles.

**Hidden Cost: Reproducibility Crisis**: The inability to fix random seeds, control model versions, or trace training data means published findings using closed-source LLMs are inherently non-reproducible. This represents a fundamental methodological crisis for LLM-based SE research.

### Guidelines for Mitigating Reproducibility Risks

The paper proposes actionable recommendations:

**For LLM Providers:**
- Implement versioning nomenclature distinguishing major vs. minor updates
- Provide fixed random seed support for deterministic inference
- Maintain archiving systems (e.g., HuggingFace, Zenodo) for model snapshots
- Disclose dataset composition for pre-training/fine-tuning [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

**For SE Researchers:**
- Conduct multiple inference runs (10+ per prompt) to quantify output variability
- Apply metamorphic testing to evaluate robustness to semantic-preserving code changes
- Use diverse data sources (not just GitHub) to test generalization
- Employ code clone detection to identify potential memorization
- Document execution metadata: model version, seed, date, scope of reproducibility [arxiv](https://arxiv.org/pdf/2312.08055.pdf)

***

## Paper 4: "Large Language Models for Cyber Security: A Systematic Literature Review"
**Authors**: Hanxiang Xu, Shenao Wang, Kailong Wang, et al. (Huazhong University of Science and Technology, Nanyang Technological University) [arxiv](https://arxiv.org/pdf/2405.04760.pdf)
**Publication**: ArXiv (2024-07-27); peer-reviewed venues; 185 papers analyzed  
**Citation Impact**: Most comprehensive SLR on LLM4Security (40K+ papers screened, 185 analyzed from top-tier venues)  
**Scope**: Systematic review spanning software/system security (63%), network security (14%), information security (12%), hardware (5%), blockchain (6%)

### Key Findings on Security Risks and Hidden Vulnerabilities

**Software and System Security Dominance**: The review finds that 119 papers (63%) focus on code-level security tasks:
- Vulnerability Detection (22 papers)
- Vulnerability Repair (15 papers)
- Bug Detection (11 papers)
- Bug Repair (32 papers) [arxiv](https://arxiv.org/pdf/2405.04760.pdf)

This concentration reveals both opportunity and risk: LLMs are increasingly deployed for high-stakes security decisions, yet the foundational risks of this deployment remain underexplored.

**Inherent LLM Security Risks (Security4LLM)**: Beyond using LLMs for security tasks, the review catalogs risks **in** LLMs themselves:
- **Jailbreaking**: Adversarial prompts can bypass safety measures
- **Prompt Injection**: Malicious inputs exploit LLM parsing to change behavior
- **Data Poisoning/Backdoors**: Training data contamination introduces vulnerabilities
- **Privacy Leaks**: Sensitive code (credentials, proprietary algorithms) extracted via inference [arxiv](https://arxiv.org/pdf/2405.04760.pdf)

These risks mean that using LLMs for security analysis simultaneously introduces new attack surfaces.

**Data Scarcity and Quality Gaps**: The survey identifies a critical gap: 64% of studies use public benchmarks (HumanEval, MBPP, SecurityEval), while only 4 studies leverage industrial/domain-specific data. This creates:
- Overfitting to benchmark scenarios
- Poor generalization to real-world code
- Bias toward open-source vulnerability patterns [arxiv](https://arxiv.org/pdf/2405.04760.pdf)

**Black-box Decision-Making**: The majority of LLM4Security papers lack interpretability analysis, meaning security teams cannot understand *why* an LLM flagged code as vulnerable. This is unacceptable for security-critical decisions where explainability and auditability are non-negotiable. [arxiv](https://arxiv.org/pdf/2405.04760.pdf)

**Hybrid Neuro-Symbolic Approaches as Emerging Mitigation**: The survey notes an emerging trend toward combining LLMs with formal verification, static analysis, and explainability tools (RAG, tool calling, autonomous agents). This hybrid paradigm addresses LLM hallucinations and unreliability in high-stakes security tasks. [arxiv](https://arxiv.org/pdf/2405.04760.pdf)

### Quantitative Impact

Distribution of security tasks:
| Task Category           | Count | Example LLM       | Performance                                     |
| ----------------------- | ----- | ----------------- | ----------------------------------------------- |
| Vulnerability Detection | 22    | CSGVD, BERT-based | Outperforms DL baselines on benchmarks          |
| Vulnerability Repair    | 15    | GPT-3.5/Codex     | 100% on synthetic; struggles on real CVEs       |
| Bug Repair              | 32    | Various           | Encoder-decoders (T5) + decoder-only (GPT) lead |
| Program Fuzzing         | 11    | LLM-guided AFL++  | Improves coverage vs. traditional fuzzers       |

***

## Paper 5: "Large Language Models for Software Engineering: A Systematic Literature Review"
**Authors**: Xinyi Hou, Yanjie Zhao, Yue Liu, et al. (Huazhong University, Monash University, Singapore Management University) [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)
**Publication**: ACM Transactions-style journal; ArXiv (2023-08-28); 229 papers analyzed  
**Citation Impact**: Broadest SLR on LLMs4SE covering full software lifecycle; 2017–2023 timeframe  
**Scope**: 229 papers; 55 distinct SE tasks across requirements, design, development, testing, maintenance, management

### Key Findings on Hidden Costs and Debugging Challenges

**Explosive Growth with Unresolved Risks**: The survey documents explosive publication growth:
- 2020: 7 papers
- 2021: 11 papers
- 2022: 51 papers
- 2023 (first 8 months): 160 papers [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

This rapid adoption outpaces understanding of risks, creating an adoption-without-due-diligence crisis.

**Model Architecture Trends**: Decoder-only LLMs (GPT series, Codex, ChatGPT) dominate by 2023 (73% of papers), driven by superior code generation performance. However, this concentration increases systemic risk—reliance on closed-source models (GPT-4, ChatGPT) means SE research depends on proprietary, non-reproducible tools. [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

**Code Generation as Primary Focus**: 57% of papers target code generation tasks. Leading models achieve:
- CodeX/GPT-3: 72.31% on HumanEval (Python challenges)
- GPT-4: Solves "real-world" coding tasks with multi-step reasoning [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

Yet the review documents persistent challenges unresolved:

| Challenge                                         | Impact                                                                                                     | Example                                            |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Ambiguity in Intent**                           | Semantic-preserving changes (variable renaming) cause >50% performance drops for code understanding models | CodeBERT fails when obfuscated                     |
| **Out-of-Distribution Generalization**            | Models excel on benchmark tasks but struggle on real-world code from unseen projects/domains               | JavaScript repair performs worse than Python       |
| **Data Scarcity & Bias**                          | 64% of studies use public/open-source data; poor coverage of industrial codebases                          | No privacy-preserving datasets for enterprise code |
| **Metric Misalignment**                           | BLEU/pass@k miss interpretability, robustness, and security dimensions                                     | Metrics don't capture code maintainability         |
| **Functional Correctness vs. Security Trade-off** | Defense techniques improve security while degrading functional correctness                                 | Prefix tuning (SVEN): -6.94% pass@1                |

**Debugging and Development Workflow Risks**: The survey documents challenges developers face:
1. **Partial Generation Problem**: LLMs often generate incomplete or syntactically malformed code requiring post-processing (adds latency).
2. **Hallucination**: Models invent APIs, libraries, or functions that don't exist, forcing developers to validate every suggestion.
3. **Context Limitations**: LLMs cannot reason about system-wide invariants, leading to code that passes unit tests but breaks integration tests.
4. **Non-determinism**: Multiple runs yield different outputs, complicating reproducibility and testing workflows. [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

**Hidden Technical Debt**: While the survey documents success in code generation, it flags a critical finding from parallel work (Quality Assurance paper): **Industry practitioners prioritize maintainability and readability over security and performance**. LLM-generated code, while functionally correct, often introduces technical debt through poor variable naming, insufficient comments, and inconsistent style. This creates long-term maintenance costs that offset short-term productivity gains. [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

### Evaluation Metric Gaps

The survey highlights that current metrics are insufficient:
- **BLEU/CIDEr**: Measure surface-level similarity, miss semantic correctness
- **pass@k**: Captures functional correctness but ignores security, efficiency, maintainability
- **Precision/Recall**: Binary classification metrics miss nuances of partial correctness [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf)

No unified metric captures all SE quality dimensions simultaneously.

***

## Integrated Risk Taxonomy Across All Five Papers

### 1. Hidden Costs (Non-Security, But Productivity-Affecting)

| Cost Category                   | Magnitude                                                 | Evidence                                        |
| ------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| Review Scrutiny Overhead        | 40–50% of suggestions need review                         | [arxiv](http://arxiv.org/pdf/2108.09293.pdf)    |
| Output Variability/Drift        | 20–50% mismatch over 3 months                             | [arxiv](https://arxiv.org/pdf/2312.08055.pdf)   |
| Training Data Bias Reproduction | Reproduces obsolete/insecure GitHub patterns              | [arxiv](http://arxiv.org/pdf/2108.09293.pdf)    |
| Technical Debt Accumulation     | Industry concern: reduced maintainability                 | [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf) |
| Deployment Latency              | Model sizes >100GB; partial code requires post-processing | [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf) |

### 2. Security Risks (Critical for Adoption)

| Risk Type                       | Prevalence                                | Mechanisms                         | Mitigation                                    |
| ------------------------------- | ----------------------------------------- | ---------------------------------- | --------------------------------------------- |
| **Vulnerable Code Generation**  | 40% of Copilot output                     | Learns from unvetted GitHub code   | CODEGUARD+ benchmark; constrained decoding    |
| **False Confidence**            | 44% of top suggestions vulnerable         | High model confidence ≠ safety     | New metrics (secure-pass@k)                   |
| **Unreliable Detection/Repair** | >50% detection false positives            | Black-box reasoning; hallucination | Hybrid neuro-symbolic systems; explainability |
| **LLM Vulnerabilities**         | Jailbreaking, poisoning, prompt injection | Inherent to LLM architecture       | Defense research ongoing                      |

### 3. Debugging & Development Challenges

| Challenge           | Symptom                                            | Severity                            |
| ------------------- | -------------------------------------------------- | ----------------------------------- |
| Prompt Sensitivity  | SQL injection rate: 0–100% across context variants | HIGH—makes safety unpredictable     |
| Partial Generations | Incomplete code, hallucinated APIs                 | MEDIUM—adds review/debugging burden |
| Context Limitations | Fails on system-wide invariants; taint tracking    | MEDIUM—catches in testing           |
| Non-Determinism     | Multiple runs produce different outputs            | MEDIUM—complicates reproducibility  |

### 4. Reproducibility & Validity Threats (Research Methodology)

| Threat                    | Evidence                                         | Impact                              |
| ------------------------- | ------------------------------------------------ | ----------------------------------- |
| **Data Leakage**          | ChatGPT memorizes Defects4J bugs                 | Invalidates generalization claims   |
| **Model Evolution**       | 20–50% output drift over 3 months                | Non-reproducible results            |
| **Closed-Source Opacity** | No control over versions, updates, training data | Research non-portable to other LLMs |
| **Output Instability**    | 52%→10% executable rate (GPT-3.5)                | Reproductions fail                  |

***

## Synthesis: Why These Are the Top 5 Papers

| Paper                                                                    | Contribution                                                                                   | Why Essential                                                                |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| ** [arxiv](http://arxiv.org/pdf/2108.09293.pdf) Asleep at the Keyboard** | Foundational quantification of Copilot's 40% vulnerability rate; 1,689-program empirical study | Establishes baseline risk magnitude; forces industry recognition of problem  |
| ** [arxiv](https://arxiv.org/abs/2405.00218) Constrained Decoding**      | Reveals false sense of security in prior metrics; introduces CODEGUARD+ benchmark              | Corrects 30-year evaluation crisis; enables future reproducible comparisons  |
| ** [arxiv](https://arxiv.org/pdf/2312.08055.pdf) Breaking the Silence**  | Documents 20–50% output drift, data leakage, reproducibility crisis                            | Raises awareness of research validity threats; proposes community guidelines |
| ** [arxiv](https://arxiv.org/pdf/2405.04760.pdf) LLM4Security SLR**      | Most comprehensive security review (185 papers); identifies inherent LLM vulnerabilities       | Catalogs all security risks; identifies data gaps and deployment hazards     |
| ** [arxiv](https://arxiv.org/pdf/2308.10620v2.pdf) LLMs4SE SLR**         | Broadest SE-focused review (229 papers); documents hidden costs and technical debt             | Completes ecosystem picture; flags long-term maintainability concerns        |

Together, these papers establish that LLM adoption in SE faces three interconnected crises: **security (40% vulnerable code)**, **debugging (unpredictable, context-sensitive behavior)**, and **reproducibility (non-deterministic, evolving models)**, all masked by metrics that overestimate actual capabilities.

***

## Recommendations for Practice

1. **Do not deploy LLMs for security-critical code generation without human expert review.**
2. **Use new evaluation metrics** (secure-pass@k, correctness + security) rather than outdated benchmarks.
3. **Apply hybrid neuro-symbolic approaches** combining LLMs with static analysis, fuzzing, and formal verification.
4. **Invest in interpretability research** to enable security auditing of LLM-generated code.
5. **Advocate for open-source models and reproducibility standards** to escape closed-source proprietary risks.
6. **Conduct multi-run inference** and metamorphic testing to quantify output variability before deployment.