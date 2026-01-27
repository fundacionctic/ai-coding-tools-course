# **The Sovereign Intelligence Architecture: Engineering Local, Privacy-First Large Language Model Ecosystems**

The landscape of artificial intelligence has transitioned from a period of experimental centralized adoption to a foundational era of sovereign computational autonomy. As of 2025 and 2026, the reliance on proprietary cloud-based Large Language Models (LLMs) has begun to yield to a sophisticated architecture of local deployments, driven by the intersecting needs for data governance, privacy preservation, and long-term cost efficiency.1 This paradigm shift, often referred to as the "Moon-landing moment" for private data, represents an evolution where intelligence is no longer a rented service but a controlled asset.3 For the modern enterprise, the decision to host intelligence locally is no longer merely a response to security fears but a strategic move to integrate AI into the core of the operational workflow without ceding control to third-party providers.1

## **The Open-Weight Model Landscape: From Dense Foundations to Reasoning MoEs**

The current state of open-weight models is characterized by a high degree of specialization and architectural innovation that challenges the dominance of closed-source giants. In 2026, the choice of a model is determined by its internal architecture—specifically whether it follows a dense, Mixture-of-Experts (MoE), or reasoning-first design—and how these structures align with local hardware constraints.5

### **Dense Architectures and the Efficiency Frontier**

Dense models, such as the Llama 4 Scout and Maverick variants, represent the traditional transformer architecture where every parameter is activated for every token generated.7 While these models are conceptually simpler and often easier to optimize for high-speed "streaming" applications, they face a physical limit in a local context due to their high VRAM-per-token cost. However, the 2026 generation of dense models has achieved significant performance gains through distilled knowledge from much larger "teacher" models. For instance, the DeepSeek-R1-Distill-Qwen3-8B demonstrates that a dense 8-billion parameter model can match the reasoning capabilities of 235-billion parameter models in specific mathematical domains, such as the AIME benchmarks.6 This efficiency makes dense models the preferred choice for edge devices and laptops where memory is at a premium.

### **Mixture-of-Experts (MoE): Scaling Without Computational Overload**

The Mixture-of-Experts (MoE) architecture has become the de facto standard for large-scale local intelligence in 2026\. Models like DeepSeek-V3 and Qwen3 utilize this sparse activation strategy to provide the benefits of a trillion-parameter model while only requiring the compute of a much smaller one.5 In an MoE system, the model is divided into many specialized "experts." A routing mechanism selects only a few experts (e.g., 2 to 8\) to process any given token.

This leads to a significant reduction in the Floating Point Operations (FLOPs) required per token. For example, the MiniMax-M1-80k model, which possesses 456 billion parameters, only activates 45.9 billion per token, resulting in a 75% savings in FLOPs compared to traditional dense architectures of similar scale.5 For the local engineer, this means that while a 671B model like DeepSeek-V3 requires a massive amount of storage space (disk and VRAM), its generation speed (tokens per second) is surprisingly high once loaded into memory.5

### **Reasoning-First Models and Internal Deliberation**

The most significant advancement in 2026 is the emergence of reasoning-first LLMs. These models, exemplified by DeepSeek-R1, GLM-4.7, and Kimi K2 Thinking, do not merely predict the next token in a sequence; they utilize internal deliberation loops, often encapsulated in \<think\> tags, to perform multi-step planning and self-correction.5 This "thinking mode" allows the model to deliberate before producing an output, which dramatically improves performance in complex tasks like automated theorem proving, software engineering, and strategic planning.5

| Model Family | Developer     | Architecture      | Key Strength          | Target Use Case     |
| :----------- | :------------ | :---------------- | :-------------------- | :------------------ |
| DeepSeek-R1  | deepseek-ai   | MoE \+ RL         | OpenAI-o1 parity      | Math/Code Reasoning |
| Qwen3-Next   | Alibaba Cloud | Sparse MoE        | 36T token training    | Multilingual Agents |
| Llama 4      | Meta          | Dense/Hybrid      | Massive Ecosystem     | General Assistant   |
| GLM-4.7      | Zhipu AI      | MoE               | Interleaved Reasoning | Agentic Coding      |
| Kimi K2      | Moonshot AI   | MoE (384 Experts) | Long Context (1M+)    | Research/Legal      |

5

Reasoning models achieve their performance through large-scale reinforcement learning (RL) rather than just supervised fine-tuning. A model like MiniMax-M2.1 autonomously patches codebases in Docker environments and only receives "rewards" when full test suites pass, ensuring that its reasoning is grounded in practical correctness rather than mere linguistic probability.5

## **Hardware Considerations for Running LLMs Locally**

The engineering of a local LLM ecosystem is fundamentally a memory-centric challenge. In 2026, the primary bottleneck for AI performance is not the processing power of the GPU (TFLOPS) but the memory bandwidth and capacity (VRAM).9 When intelligence is moved local, the "Memory Wall" dictates the upper limit of the model's complexity and the speed of its interaction.

### **Memory Needs and the VRAM Constraint**

Large Language Models must reside in memory for efficient inference. If a model's weights do not fit entirely in the Video Random Access Memory (VRAM) of a GPU, the system must "offload" layers to the system RAM or, worse, to a disk-based swap file. Offloading to system RAM typically results in a performance degradation from 40-60 tokens per second down to 1-2 tokens per second, a speed that is insufficient for real-time interaction.10

A standard rule of thumb for VRAM requirements is based on the parameter count and the quantization level. Using 4-bit quantization, which is the current industry standard for balancing quality and size, the required memory is roughly 0.7 to 0.8 gigabytes per billion parameters, plus an additional buffer for the KV-cache (the model's "short-term memory" of the current conversation).10

### **NVIDIA vs. Apple Silicon: Throughput vs. Capacity**

The hardware market in 2026 is split between NVIDIA’s discrete GPU dominance and Apple’s Unified Memory Architecture (UMA).

NVIDIA's newest flagship, the RTX 5090, features 32GB of GDDR7 memory with a bandwidth of approximately 1,792 GB/s.10 This represents a 77% improvement over the previous generation, making it the premier choice for high-speed inference on models up to 30 billion parameters. However, even the 5090 cannot fit a full 70B model uncompressed, necessitating multi-GPU setups or aggressive quantization for the largest open-weight models.10

Apple’s M4 and M5 Max/Ultra chips take a different approach through Unified Memory. In these systems, the CPU, GPU, and Neural Engine share a single pool of memory, which can be configured up to 512GB or more on high-end Mac Studio models.9 While the raw token generation speed (decode) on a Mac may trail a 5090 by 20-30%, the ability to load a 405B model or a 671B MoE model into a single machine without complex multi-GPU orchestration is a transformative advantage for sovereign deployments.9

### **Hardware Performance Tiers in 2026**

| Tier           | Hardware          | Memory        | Best For                | Price (Est.) |
| :------------- | :---------------- | :------------ | :---------------------- | :----------- |
| **Entry**      | RTX 4060 Ti       | 16GB VRAM     | 7B-8B Models            | $500         |
| **Mid**        | Used RTX 3090     | 24GB VRAM     | 14B-32B Models          | $700-$900    |
| **Flagship**   | RTX 5090          | 32GB VRAM     | 32B Models @ High Speed | $1,999       |
| **Pro**        | Mac Studio M4 Max | 128GB Unified | 70B Models              | $4,500+      |
| **Enterprise** | NVIDIA H100/H200  | 80GB VRAM     | Concurrent Production   | $25,000+     |

10

For technical managers, the choice involves a tradeoff between "model capacity" and "tokens per second." If the goal is to run the most intelligent models available (70B-405B) with long context windows, Apple Silicon or high-VRAM enterprise GPUs (RTX A6000) are the practical defaults. If the goal is low-latency, real-time responses for coding or chat using mid-sized models, NVIDIA consumer GPUs remain the efficiency leaders.9

## **Model Compression and Quantization Approaches**

Quantization is the process of reducing the mathematical precision of a model's weights—moving from 16-bit floating-point numbers (FP16) down to 4-bit or even 2-bit integers—to save memory and increase speed. In 2026, quantization is no longer a "lossy" compromise but a sophisticated optimization layer.16

### **GGUF: The Universal Local Format**

GGUF (GPT-Generated Unified Format) is the primary format for local LLMs, specifically designed for tools like Ollama and LM Studio. Its main advantage is its ability to run on both CPUs and GPUs through a feature called "layer offloading." If a user has a 24GB GPU but wants to run a model that requires 30GB, GGUF allows the first 20 layers to stay on the GPU while the remaining layers run on the slower CPU.12 This flexibility makes it the standard for heterogeneous hardware environments.

### **AWQ and EXL2: NVIDIA-Optimized Precision**

For those utilizing NVIDIA hardware, AWQ (Activation-aware Weight Quantization) and EXL2 (ExLlamaV2) offer superior performance. AWQ works by observing the "activation" patterns of a model—essentially identifying which neurons fire most frequently during thinking—and protecting those critical weights with higher precision while compressing the rest.16 This results in a 4-bit model that often retains 99% of the accuracy of the original 16-bit model. EXL2 takes this further by allowing "fractional" quantization, where an engineer can precisely target a bitrate (e.g., 4.25 bits per weight) to perfectly fill a specific GPU's VRAM.12

### **The Emergence of MXFP4**

The newest standard in 2026 is MXFP4, a format optimized for the latest generation of hardware like NVIDIA's Blackwell. It uses microscopic scaling factors to manage 4-bit data, allowing for massive throughput increases without the "blocking" artifacts seen in earlier 4-bit integer methods.18

The fundamental equation for determining the impact of quantization on memory usage is:

![][image1]  
Where the ![][image2] (typically 1.1 to 1.2) accounts for system memory, the KV-cache, and activation buffers.10 By applying this, a 70B parameter model at 4-bit precision (![][image3]) requires roughly 42GB of VRAM, which is why 48GB and 128GB systems have become the enterprise baseline for sovereign AI.10

## **Software Runtimes and Orchestration Layers**

The software runtime is the engine that executes the quantized model. In 2026, the ecosystem has matured into a multi-tiered landscape serving different needs from personal research to high-throughput production.20

### **Ollama and LM Studio: Accessibility and Developer Experience**

Ollama has emerged as the "Docker for AI," providing a simple command-line interface that manages model downloads, manifests, and local APIs.20 It is highly favored by developers because it packages the complex llama.cpp backend into a single executable that runs as a background service. LM Studio, on the other hand, provides the most polished graphical interface, allowing researchers and non-technical managers to "discover" models on Hugging Face and test them with visual parameter controls.20

### **vLLM: The Production Standard**

For enterprises needing to serve hundreds of concurrent users, vLLM is the primary choice. Its "V1" engine features always-on optimizations like prefix caching and continuous batching, which allows it to handle many requests simultaneously without the dramatic slowdowns seen in single-user runtimes.21 However, vLLM is largely optimized for Linux and NVIDIA GPUs, making it less portable than Ollama but significantly more powerful in a data center context.23

### **LocalAI and GPT4All: The Orchestration Hubs**

LocalAI acts as a "Universal API Hub," providing a single front door for multiple AI tasks—including text generation, image creation, and audio transcription—all through an OpenAI-compatible API.20 It can orchestrate different backends behind the scenes, such as routing a coding request to a vLLM instance while sending an image request to a local Stable Diffusion server. GPT4All remains the simplest option for privacy-first desktop use, specifically optimized for running on consumer-grade CPUs with a very small memory footprint.20

| Runtime       | Target Audience   | Deployment Scenario       | Key Strength         |
| :------------ | :---------------- | :------------------------ | :------------------- |
| **Ollama**    | Developers        | Local Workstations        | CLI UX / API Support |
| **vLLM**      | Enterprise Ops    | High-Concurrency Clusters | Maximum Throughput   |
| **LM Studio** | Researchers       | GUI-based Discovery       | Polish / Ease of Use |
| **LocalAI**   | System Architects | Multi-Model Orchestration | OpenAI API Parity    |
| **GPT4All**   | General Users     | CPU-only Hardware         | Lowest Footprint     |

20

## **Privacy-First System Configuration and Hardening**

Sovereign intelligence requires more than just local execution; it requires a defensive posture that assumes the system is a target. In 2026, attackers have moved from general phishing to systematic enumeration of local LLM endpoints, looking for misconfigured APIs to exfiltrate private data.24

### **Disabling Telemetry and "Phoning Home"**

Most modern software contains telemetry—data about usage patterns that is sent back to the developer. In a sovereign context, this is a vulnerability. Tools like "RemoveWindowsAI" are used to strip out integrated AI components from Windows systems that capture screenshots or local indices (like Windows Recall), ensuring that no background data collection occurs.25 Similarly, for containerized deployments, engineers must explicitly disable telemetry in Helm charts or configuration files, as seen in the "Okteto" or "Tabnine" air-gapped guides.26

### **Engineering Air-Gapped Systems**

An air-gapped system is physically or logically disconnected from the internet. To run an LLM in such an environment, an organization must build its own "Sovereign Supply Chain":

1. **Local Container Registry:** Instead of pulling images from Docker Hub, images are stored on an internal registry.26  
2. **Internal Model Storage:** Model weights (the "brain" of the AI) are hosted on private servers and scanned for integrity before being loaded into the production environment.26  
3. **Offline Licensing:** Enterprise tools like Tabnine or Sourcegraph Cody are configured with static license keys to avoid external validation pings.26

### **Network Isolation and Micro-Segmentation**

Even within a private network, AI servers should be isolated using a Zero Trust architecture. This involves:

* **VLAN Isolation:** Placing the AI cluster in a dedicated Virtual Local Area Network that cannot communicate with the rest of the corporate network without going through a firewall.28  
* **Default Deny Policies:** Firewalls should be configured to "drop" all traffic by default, only allowing specific ports (e.g., port 11434 for Ollama or 8080 for LocalAI) to communicate with authorized developer workstations.30  
* **MFA for SSH:** Any administrative access to the AI server must require multi-factor authentication, even if it is on a private, air-gapped segment.30

## **Private Retrieval-Augmented Generation (RAG) Architectures**

RAG is the mechanism that allows an LLM to "read" your private documents and answer questions based on them. In a sovereign architecture, the "Retrieval" must be as private as the "Generation".32

### **Local Embedding Models and Vector Databases**

The first step in RAG is converting text into numbers (embeddings). In 2026, open-weight embedding models like BGE-M3 or E5-Large have surpassed the performance of cloud-based APIs.34 These models run locally, ensuring that the "semantic meaning" of your documents never leaves your premises.

These embeddings are then stored in a vector database. For local or embedded use cases, Chroma and LanceDB offer a "zero-ops" experience where the database lives within the application.32 For enterprise-scale applications requiring billions of vectors, Qdrant or Milvus provide a dedicated service layer that can handle complex metadata filtering and hybrid searches (combining keyword and semantic matching).32

### **Practical Chunking and Workflow Logic**

The effectiveness of a RAG system depends on how documents are "chunked" or split before being stored.

* **Recursive Chunking:** This is the practical default for 2026\. It attempts to split documents at logical structural points—first by paragraphs, then sentences—to ensure that context is not lost by cutting a sentence in half.37  
* **Semantic Chunking:** A more advanced approach that uses an embedding model to find where the "topic" changes in a document, creating a break point only when a new concept is introduced.37  
* **Agentic Chunking:** This utilizes a small reasoning model to analyze a document's layout (recognizing tables, headers, and footnotes) to intelligently determine how a human would split the information.37

The RAG workflow follows a consistent path:

1. **Ingestion:** Documents are parsed and cleaned.  
2. **Chunking:** The text is split into manageable pieces (e.g., 512 tokens with 50-token overlap).37  
3. **Embedding:** Each chunk is converted into a vector using a local model like BGE-M3.34  
4. **Retrieval:** When a user asks a question, the system finds the most similar chunks in the vector database.40  
5. **Generation:** The retrieved text is fed into the local LLM as "context," and the model generates a response.40

## **Privacy-First Developer Workflows and Hardened Environments**

The daily workflow of a software engineer in 2026 is augmented by AI assistants that live directly in the IDE (Integrated Development Environment). To maintain sovereignty, these assistants must be decoupled from the cloud.41

### **Local IDE Assistants: Continue and RooCode**

Continue and RooCode (formerly Roo Cline) are the leading open-source alternatives to GitHub Copilot.

* **Continue** focuses on a seamless, native-like experience, providing autocomplete and chat. It is highly flexible, allowing a developer to connect it to an Ollama instance running on the same machine.42  
* **RooCode** is designed for autonomy. It functions as an "agentic" environment where the AI can plan multi-file changes, run terminal commands, and fix its own errors. It uses "Model Context Protocol" (MCP) to switch between local and remote models as needed.41

These tools enable a "BYO Model" strategy, where the code never leaves the developer's laptop, yet they still benefit from the state-of-the-art reasoning of models like DeepSeek Coder.21

### **Hardened Operating Systems for AI Isolation**

For high-security environments, the host operating system itself must be hardened to isolate AI workloads from potential compromise.45

* **Qubes OS:** Known as the "world's most secure OS," Qubes uses compartmentalization to run different activities in separate virtual machines. A developer can have an "offline-ai" qube that has exclusive access to the GPU via passthrough, while their networking is handled by a separate "sys-net" qube.45  
* **Talos Linux:** For those running AI on Kubernetes, Talos is an immutable, API-driven Linux distribution. It has no SSH and no shell, meaning that if a container is compromised, there is no underlying OS for an attacker to "pivot" to.46  
* **Ubuntu LTS with Hardening:** For more traditional environments, Ubuntu LTS 24.04 provides automated hardening through the "Ubuntu Security Guide" (USG), which applies CIS benchmarks and enables AppArmor for process-level isolation of the LLM runtime.47

### **Zero Trust Workload Isolation**

Implementing Zero Trust for local AI means that even the LLM itself is not "trusted."

* **Sandboxing:** Running LLM-generated code in microVMs like Firecracker or userspace kernels like gVisor to prevent a rogue AI-generated script from accessing the host's filesystem.54  
* **Micro-segmentation:** Using firewalls (UFW or iptables) to ensure the LLM server cannot "call home" or scan the internal network.28  
* **Continuous Auditing:** Using tools like auditd to monitor every file access made by the LLM runtime.30

## **Strategic Synthesis: Operational Resilience and Long-Term Value**

The shift to the Sovereign Intelligence Architecture is ultimately a strategic decision centered on resilience, compliance, and the total cost of ownership (TCO).

### **Operational Resilience and Independence**

By hosting intelligence locally, enterprises eliminate "vendor lock-in" and the risk of API outages. If a cloud provider changes their pricing model or "lobotomizes" a model through a safety update, the local sovereign system remains unchanged.13 Furthermore, ownership of the model weights allows for specialized fine-tuning on proprietary data that would be too sensitive to upload to a public cloud.4

### **The New Economics of AI: TCO Analysis**

While cloud-based AI appears cheaper in the short term due to its lack of upfront hardware costs, high-volume users find that local deployments are significantly more cost-effective over a 2-3 year horizon.13

| Cost Component   | Cloud API (Enterprise)      | Local Sovereign (Workstation) |
| :--------------- | :-------------------------- | :---------------------------- |
| **Setup Cost**   | $0                          | $4,000 \- $8,000              |
| **Token Cost**   | $15 \- $30 / million tokens | $0                            |
| **Privacy Risk** | Third-party handling        | Zero egress                   |
| **Scaling**      | Pay-as-you-go (Unlimited)   | Hardware-capped               |
| **Electricity**  | N/A                         | $0.10 \- $0.30 / kWh          |
| **Maintenance**  | Included                    | Requires MLOps effort         |

13

For an organization processing 50 million tokens per month (a common workload for a medium-sized development team), the annual cloud cost can exceed $12,000. A high-end workstation with an RTX 5090 or a Mac Studio pays for itself in less than nine months, with the only ongoing costs being electricity and minimal maintenance.13

### **Regulatory Compliance and the Future Outlook**

Regulations like California’s SB 243 and AB 489 are beginning to mandate clear AI disclosures and "doctor-level" accuracy for health-related bots.59 Sovereign deployments allow enterprises to audit their own models and enforce internal guardrails that are strictly tailored to these legal requirements, rather than relying on the generic safety filters of a cloud provider.26

As we look toward the remainder of the decade, the ability to engineer and maintain a local intelligence ecosystem will be a defining capability for the modern technical team. Sovereignty is not just about keeping data in-house; it is about the freedom to innovate at the speed of local hardware, without the constraints of third-party APIs or the risks of privacy erosion. The Sovereign Intelligence Architecture is the new foundation for a secure, resilient, and autonomous digital future.

#### **Works cited**

1. 2026 Predictions: The Architecture, Governance, and AI Trends Every Enterprise Must Prepare For \- Cloudera, accessed on January 27, 2026, [https://www.cloudera.com/blog/business/2026-predictions-the-architecture-governance-and-ai-trends-every-enterprise-must-prepare-for.html](https://www.cloudera.com/blog/business/2026-predictions-the-architecture-governance-and-ai-trends-every-enterprise-must-prepare-for.html)  
2. How agentic, physical and sovereign AI are rewriting the rules of enterprise innovation, accessed on January 27, 2026, [https://www.weforum.org/stories/2026/01/how-agentic-physical-and-sovereign-ai-are-rewriting-the-rules-of-enterprise-innovation/](https://www.weforum.org/stories/2026/01/how-agentic-physical-and-sovereign-ai-are-rewriting-the-rules-of-enterprise-innovation/)  
3. AI & Data Predictions for 2026: Trends & Opportunities \- EDB, accessed on January 27, 2026, [https://www.enterprisedb.com/resources/26-predictions](https://www.enterprisedb.com/resources/26-predictions)  
4. Enterprise AI in 2026: Sovereign, agentic, edge and AI factories ..., accessed on January 27, 2026, [https://www.spectrocloud.com/blog/enterprise-ai-2026-trends](https://www.spectrocloud.com/blog/enterprise-ai-2026-trends)  
5. Ultimate Guide \- The Best Open Source LLMs for Reasoning in 2026 \- SiliconFlow, accessed on January 27, 2026, [https://www.siliconflow.com/articles/en/best-open-source-LLMs-for-reasoning](https://www.siliconflow.com/articles/en/best-open-source-LLMs-for-reasoning)  
6. Top 10 Open-source Reasoning Models in 2026 \- Clarifai, accessed on January 27, 2026, [https://www.clarifai.com/blog/top-10-open-source-reasoning-models-in-2026](https://www.clarifai.com/blog/top-10-open-source-reasoning-models-in-2026)  
7. Top LLMs and AI Trends for 2026 | Clarifai Industry Guide, accessed on January 27, 2026, [https://www.clarifai.com/blog/llms-and-ai-trends](https://www.clarifai.com/blog/llms-and-ai-trends)  
8. Top LLMs To Use in 2026: Our Best Picks \- Splunk, accessed on January 27, 2026, [https://www.splunk.com/en\_us/blog/learn/llms-best-to-use.html](https://www.splunk.com/en_us/blog/learn/llms-best-to-use.html)  
9. I Almost Bought an RTX 5090\. Then Apple's Unified Memory Changed My Mind, accessed on January 27, 2026, [https://ksingh7.medium.com/i-almost-bought-an-rtx-5090-then-apples-unified-memory-changed-my-mind-83eb964e930b](https://ksingh7.medium.com/i-almost-bought-an-rtx-5090-then-apples-unified-memory-changed-my-mind-83eb964e930b)  
10. The Complete Guide to Running LLMs Locally: Hardware, Software ..., accessed on January 27, 2026, [https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/](https://www.ikangai.com/the-complete-guide-to-running-llms-locally-hardware-software-and-performance-essentials/)  
11. The 2026 Local LLM Hardware Guide: Surviving the RAM Crisis | by James Rien \- Medium, accessed on January 27, 2026, [https://medium.com/@jameshugo598/the-2026-local-llm-hardware-guide-surviving-the-ram-crisis-fa67e8c95804](https://medium.com/@jameshugo598/the-2026-local-llm-hardware-guide-surviving-the-ram-crisis-fa67e8c95804)  
12. AWQ vs GPTQ vs GGUF: AI Quantization Comparison (2025) \- Local AI Master, accessed on January 27, 2026, [https://localaimaster.com/blog/quantization-explained](https://localaimaster.com/blog/quantization-explained)  
13. On-Prem LLMs vs Cloud APIs: When to Run Models Locally | Unified AI Hub, accessed on January 27, 2026, [https://www.unifiedaihub.com/blog/on-premise-llms-vs-cloud-apis-when-to-run-your-ai-models-on-premise](https://www.unifiedaihub.com/blog/on-premise-llms-vs-cloud-apis-when-to-run-your-ai-models-on-premise)  
14. Using a high-end MacBook Pro or a beefy RTX 5090 laptop (with 24 GB of RAM) for inference. : r/LocalLLM \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/LocalLLM/comments/1qnpti6/using\_a\_highend\_macbook\_pro\_or\_a\_beefy\_rtx\_5090/](https://www.reddit.com/r/LocalLLM/comments/1qnpti6/using_a_highend_macbook_pro_or_a_beefy_rtx_5090/)  
15. Need to upgrade my 5yo Legion: RTX 5090 (24GB) Laptop or MacBook M4/M5 Max (64GB+) for AI engineering? : r/LocalLLaMA \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1qf8qoz/need\_to\_upgrade\_my\_5yo\_legion\_rtx\_5090\_24gb/](https://www.reddit.com/r/LocalLLaMA/comments/1qf8qoz/need_to_upgrade_my_5yo_legion_rtx_5090_24gb/)  
16. Understanding LLM Weight Quantization: GPTQ, AWQ, and GGUF: Make BIG models fit in a small space | by Abhishek Kumar Srivastava \- Medium, accessed on January 27, 2026, [https://medium.com/@abhi-84/understanding-llm-weight-quantization-gptq-awq-and-gguf-make-big-models-fit-in-a-small-space-518bb204cae4](https://medium.com/@abhi-84/understanding-llm-weight-quantization-gptq-awq-and-gguf-make-big-models-fit-in-a-small-space-518bb204cae4)  
17. Which Quantization Method Is Best for You?: GGUF, GPTQ, or AWQ... | E2E Networks, accessed on January 27, 2026, [https://www.e2enetworks.com/blog/which-quantization-method-is-best-for-you-gguf-gptq-or-awq](https://www.e2enetworks.com/blog/which-quantization-method-is-best-for-you-gguf-gptq-or-awq)  
18. Visualizing Quantization Types : r/LocalLLaMA \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1opeu1w/visualizing\_quantization\_types/](https://www.reddit.com/r/LocalLLaMA/comments/1opeu1w/visualizing_quantization_types/)  
19. Benchmarks for Quantized Models? (for users locally running Q8/Q6/Q2 precision) \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/LocalLLaMA/comments/1pyrjke/benchmarks\_for\_quantized\_models\_for\_users\_locally/](https://www.reddit.com/r/LocalLLaMA/comments/1pyrjke/benchmarks_for_quantized_models_for_users_locally/)  
20. Top 5 Local LLM Tools and Models in 2026 \- Pinggy, accessed on January 27, 2026, [https://pinggy.io/blog/top\_5\_local\_llm\_tools\_and\_models/](https://pinggy.io/blog/top_5_local_llm_tools_and_models/)  
21. The Complete Guide to Ollama Alternatives: 8 Best Local LLM Tools for 2026, accessed on January 27, 2026, [https://localllm.in/blog/complete-guide-ollama-alternatives](https://localllm.in/blog/complete-guide-ollama-alternatives)  
22. Top 10 Local AI Tools for Enterprise (2026) | On-Premise AI Comparison, accessed on January 27, 2026, [https://iternal.ai/best-local-ai-tools-enterprise](https://iternal.ai/best-local-ai-tools-enterprise)  
23. vLLM vs Ollama vs LMStudio? : r/LocalLLM \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/LocalLLM/comments/1n1cmq6/vllm\_vs\_ollama\_vs\_lmstudio/](https://www.reddit.com/r/LocalLLM/comments/1n1cmq6/vllm_vs_ollama_vs_lmstudio/)  
24. AI Deployments Targeted in 91,000+ Attack Sessions | eSecurity Planet, accessed on January 27, 2026, [https://www.esecurityplanet.com/threats/ai-deployments-targeted-in-91000-attack-sessions/](https://www.esecurityplanet.com/threats/ai-deployments-targeted-in-91000-attack-sessions/)  
25. RemoveWindowsAI: Complete AI Feature Removal for Windows Privacy, Control, and Defensive Hardening \- Cyberwarzone, accessed on January 27, 2026, [https://cyberwarzone.com/2026/01/04/removewindowsai-complete-ai-feature-removal-for-windows-privacy-control-and-defensive-hardening/](https://cyberwarzone.com/2026/01/04/removewindowsai-complete-ai-feature-removal-for-windows-privacy-control-and-defensive-hardening/)  
26. Enterprise AI Code Assistants for Air-Gapped Environments ..., accessed on January 27, 2026, [https://intuitionlabs.ai/articles/enterprise-ai-code-assistants-air-gapped-environments](https://intuitionlabs.ai/articles/enterprise-ai-code-assistants-air-gapped-environments)  
27. Air-Gapped Networks | Okteto Documentation, accessed on January 27, 2026, [https://www.okteto.com/docs/self-hosted/manage/air-gapped/](https://www.okteto.com/docs/self-hosted/manage/air-gapped/)  
28. Network Isolation: How It Works, Methods, And Strategies \- Nile Secure, accessed on January 27, 2026, [https://nilesecure.com/network-design/network-isolation](https://nilesecure.com/network-design/network-isolation)  
29. What is an Air Gap? Benefits and Best Practices \- SentinelOne, accessed on January 27, 2026, [https://www.sentinelone.com/cybersecurity-101/cybersecurity/what-is-an-air-gap/](https://www.sentinelone.com/cybersecurity-101/cybersecurity/what-is-an-air-gap/)  
30. Implementing Zero Trust Architecture in Enterprise Linux: A Security Guide \- TuxCare, accessed on January 27, 2026, [https://tuxcare.com/blog/implementing-zero-trust-architecture-in-enterprise-linux-a-security-guide/](https://tuxcare.com/blog/implementing-zero-trust-architecture-in-enterprise-linux-a-security-guide/)  
31. Current best practices for isolating VLANs? : r/Ubiquiti \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/Ubiquiti/comments/1gev7g7/current\_best\_practices\_for\_isolating\_vlans/](https://www.reddit.com/r/Ubiquiti/comments/1gev7g7/current_best_practices_for_isolating_vlans/)  
32. The 7 Best Vector Databases in 2026 \- DataCamp, accessed on January 27, 2026, [https://www.datacamp.com/blog/the-top-5-vector-databases](https://www.datacamp.com/blog/the-top-5-vector-databases)  
33. Qdrant vs LanceDB | Vector Database Comparison \- Zilliz, accessed on January 27, 2026, [https://zilliz.com/comparison/qdrant-vs-lancedb](https://zilliz.com/comparison/qdrant-vs-lancedb)  
34. 5 Best Embedding Models for RAG: How to Choose the Right One \- GreenNode, accessed on January 27, 2026, [https://greennode.ai/blog/best-embedding-models-for-rag](https://greennode.ai/blog/best-embedding-models-for-rag)  
35. Best Vector Databases in 2025: A Complete Comparison Guide \- Firecrawl, accessed on January 27, 2026, [https://www.firecrawl.dev/blog/best-vector-databases-2025](https://www.firecrawl.dev/blog/best-vector-databases-2025)  
36. Best 17 Vector Databases for 2026 \[Top Picks\] \- lakeFS, accessed on January 27, 2026, [https://lakefs.io/blog/best-vector-databases/](https://lakefs.io/blog/best-vector-databases/)  
37. Implement RAG chunking strategies with LangChain and watsonx.ai \- IBM, accessed on January 27, 2026, [https://www.ibm.com/think/tutorials/chunking-strategies-for-rag-with-langchain-watsonx-ai](https://www.ibm.com/think/tutorials/chunking-strategies-for-rag-with-langchain-watsonx-ai)  
38. Chunking Strategies to Improve Your RAG Performance \- Weaviate, accessed on January 27, 2026, [https://weaviate.io/blog/chunking-strategies-for-rag](https://weaviate.io/blog/chunking-strategies-for-rag)  
39. Chunking Strategies for AI and RAG Applications \- DataCamp, accessed on January 27, 2026, [https://www.datacamp.com/blog/chunking-strategies](https://www.datacamp.com/blog/chunking-strategies)  
40. The Ultimate Guide to Chunking Strategies for RAG Applications with Databricks \- Medium, accessed on January 27, 2026, [https://medium.com/@debusinha2009/the-ultimate-guide-to-chunking-strategies-for-rag-applications-with-databricks-e495be6c0788](https://medium.com/@debusinha2009/the-ultimate-guide-to-chunking-strategies-for-rag-applications-with-databricks-e495be6c0788)  
41. Cline vs Roo Code vs Cursor | Better Stack Community, accessed on January 27, 2026, [https://betterstack.com/community/comparisons/cline-vs-roo-code-vs-cursor/](https://betterstack.com/community/comparisons/cline-vs-roo-code-vs-cursor/)  
42. Agentic AI Comparison: Continue vs Roo Code, accessed on January 27, 2026, [https://aiagentstore.ai/compare-ai-agents/continue-vs-roo-code](https://aiagentstore.ai/compare-ai-agents/continue-vs-roo-code)  
43. Continue vs. Roo Code Comparison \- SourceForge, accessed on January 27, 2026, [https://sourceforge.net/software/compare/Continue-vs-Roo-Code/](https://sourceforge.net/software/compare/Continue-vs-Roo-Code/)  
44. The Top 13 AI Coding Assistants to Use in 2026 | DataCamp, accessed on January 27, 2026, [https://www.datacamp.com/blog/best-ai-coding-assistants](https://www.datacamp.com/blog/best-ai-coding-assistants)  
45. Qubes OS: A reasonably secure operating system | Qubes OS, accessed on January 27, 2026, [https://www.qubes-os.org/](https://www.qubes-os.org/)  
46. Talos Linux security with Andrey Smirnov, accessed on January 27, 2026, [https://opensourcesecurity.io/2025/2025-09-talos-andrey-smirnov/](https://opensourcesecurity.io/2025/2025-09-talos-andrey-smirnov/)  
47. A guide to Infrastructure Hardening \- Ubuntu, accessed on January 27, 2026, [https://ubuntu.com/engage/a-guide-to-infrastructure-hardening](https://ubuntu.com/engage/a-guide-to-infrastructure-hardening)  
48. Step-by-step nvidia GPU passthrough for cuda/vulkan compute applications, accessed on January 27, 2026, [https://forum.qubes-os.org/t/step-by-step-nvidia-gpu-passthrough-for-cuda-vulkan-compute-applications/36813](https://forum.qubes-os.org/t/step-by-step-nvidia-gpu-passthrough-for-cuda-vulkan-compute-applications/36813)  
49. LLMs in Qubes (and GPU passthrough) \- Reddit, accessed on January 27, 2026, [https://www.reddit.com/r/Qubes/comments/1q36jtw/llms\_in\_qubes\_and\_gpu\_passthrough/](https://www.reddit.com/r/Qubes/comments/1q36jtw/llms_in_qubes_and_gpu_passthrough/)  
50. Talos Security Checklist \- Sidero Documentation \- What is Talos Linux?, accessed on January 27, 2026, [https://docs.siderolabs.com/talos/v1.11/security/talos-security-checklist](https://docs.siderolabs.com/talos/v1.11/security/talos-security-checklist)  
51. Security standards \- Ubuntu, accessed on January 27, 2026, [https://ubuntu.com/security/security-standards](https://ubuntu.com/security/security-standards)  
52. AppArmor \- Ubuntu Server documentation, accessed on January 27, 2026, [https://documentation.ubuntu.com/server/how-to/security/apparmor/](https://documentation.ubuntu.com/server/how-to/security/apparmor/)  
53. How to Set Up AppArmor Profiles on Ubuntu \- OneUptime, accessed on January 27, 2026, [https://oneuptime.com/blog/post/2026-01-07-ubuntu-apparmor-profiles/view](https://oneuptime.com/blog/post/2026-01-07-ubuntu-apparmor-profiles/view)  
54. A field guide to sandboxes for AI \- Luis Cardoso, accessed on January 27, 2026, [https://www.luiscardoso.dev/blog/sandboxes-for-ai](https://www.luiscardoso.dev/blog/sandboxes-for-ai)  
55. The Complete Guide to Sandboxing Autonomous Agents: Tools, Frameworks, and Safety Essentials \- IKANGAI, accessed on January 27, 2026, [https://www.ikangai.com/the-complete-guide-to-sandboxing-autonomous-agents-tools-frameworks-and-safety-essentials/](https://www.ikangai.com/the-complete-guide-to-sandboxing-autonomous-agents-tools-frameworks-and-safety-essentials/)  
56. Cloud LLM vs Local LLM: Which AI Deployment is Best for Your Business? \- Cantech, accessed on January 27, 2026, [https://www.cantech.in/blog/cloud-llm-vs-local-llm/](https://www.cantech.in/blog/cloud-llm-vs-local-llm/)  
57. Local LLM: When Running AI In-House Becomes the Smarter Choice \- Neil Sahota, accessed on January 27, 2026, [https://www.neilsahota.com/local-llm-when-running-ai-in-house-becomes-the-smarter-choice/](https://www.neilsahota.com/local-llm-when-running-ai-in-house-becomes-the-smarter-choice/)  
58. Complete LLM Pricing Comparison 2026: We Analyzed 60+ Models So You Don't Have To, accessed on January 27, 2026, [https://www.cloudidr.com/blog/llm-pricing-comparison-2026](https://www.cloudidr.com/blog/llm-pricing-comparison-2026)  
59. AI Guardrails Will Stop Being Optional in 2026 \- StateTech Magazine, accessed on January 27, 2026, [https://statetechmagazine.com/article/2026/01/ai-guardrails-will-stop-being-optional-2026](https://statetechmagazine.com/article/2026/01/ai-guardrails-will-stop-being-optional-2026)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAXCAYAAADAxotdAAAE90lEQVR4Xu2ZeainYxTHj11kzb6NJSJki7LOJUuIkuzLhJClyF78MwmNJGuIuFnGTvbdINv4Q8qadSz5R8kuWb8f533vfX7n3X9xr7neT32b+zvv/pzznHOeZ8x6enp65ieWjoaeqcOS0hPR+H9gb+lqabq0ubSptIm0cabFxk+1daWTpQvNr5tseLeHpWnxQAlHSKcG28LSiDRTOkhaZuDoxIMPUBd2NH9/tFc49jcXSH9W6Fdpzey8naVPpVOkXaRnpTuzY5PFLPP33CgeKOFxaZXk9wLSzdJN5t92tPSJtE1yzkSwm3Sd+bP5ljMHD9dyiXSLdJh0mfS79LS0eHrSPdIj0rXSVdIV0uXSR9K52TkLSV9IZ2S/YXnpe2lGYptIcMQP1s7Bq0uPBtsx0vXBRlZ6V1ok2P9N9pcONHdSFwePSG/YYF+B37jHxYnNXpIWTA1iO+nJxL6v+YVbjp3hvGgeMU2sEw0BHEAQtYXU/Lx5BLdx8NnS4cF2g/RUsC1rfr8Vgz2yknlNr4LssFY0NrCtdXPweebnMzFzdspsTMYx9kl/mEfEa9JqiY3pz4XRUQ9Kv5jXsjrukA6OxoytpTnSEvFADZSVQ6WzrJ2DX7WiQyg1ebTnKY00TelpguxBcJR15UyKUSsGVBNdHcy4zZX2S2wEHvf4LLEVGLVi2r3N/MJVg/3uzL5ysEcWlR6w4kczUC9IKwR7HVtI92Z/t3Ew51NrI2SNz82vf186R3o5s7dhV+k581mfg3N51vGJrS1dHVwGJYZ7UGZL2Ur60twhKSwvyhxJk9U0wDmk1YfMu1nAuaT4pnSYQqZgtufZpY2DL5V2j8aM9cz7CO6BRq040+ugQSJAcTLOpeE5YeCM9vwTDqbcfmc140EqjY0H0IHy8LQLhdzBGwR7FbmTzzd/GVJKF2j6jkp+NzmYuv569m9kOfMAY0C5z0/m96IZKzu/CoIHJ5PlTgrHupA7mHcZhuPMg5UVTilrSL9Zca0It5o/PKYvOnDsdNRtIbX9KJ0WDzSAE6n5KU0O3tO8ESuDQLso+b2+9Ir5/Q5J7E2QVajb75kHzbDkDqYh7ArLPDIvdbmSI80fULaBMcvKB5JOG2fRNbZhB/M6R4olOGYMHq7lRPN1+Dzp40zfmr8XtZRGKjJb2iwazYP5Dxtf4+eQaklxlTUsgHPvMk/L0807+7Qmd2FYB7Mx9aa0YWKjgSzAYpsHsDMSGTE/tkewE7X3BVsVuXPzmstakyYtr8nDcKWVBx4sZT4jyyDjsCkQHQz32/j6v47UuTk4eY4NtyOWO5hmrwwyTGxGeX+yR/odjOvc5PcY1EQeQKMVoSYRJSyXcqi7P5un3CZ4+bJumZdhkFjkDwNrQN65bJaSHdKNmQgDw8ZAmn3WNs8SNF91MB63S8fGA+ZrUe7d1ckEB9/CEjDC+1A+P0xsZIq3pbekZ8wDizF+x8ZXGQOwruMBVR/Hwn2edKN5/eRhbWvVNVZdn5gJ7KCVrSmrYA3MTts35in1ayvOVjr/dC0fYRZzDfeZaZ6WCeLS/dwAtZ0AqmJ7a99w8ewPpK/MSw7fQ5Cxx57D2ODMdLlHIOCvMvF/BQWmmbf9deAMZuMBVlwT/5fAsY9FYwnMXtI7AUM33CXIeiaR0624qdIzhaAWddmw6JmPYLkwGo09UwcW/WUrgZ6eqcVfZxALk/etqF4AAAAASUVORK5CYII=>