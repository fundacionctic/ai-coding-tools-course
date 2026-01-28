# MCP Overview

## Core Architecture

* **MCP Client** connects to **MCP Server**.
* **MCP Server** contains tools, resources, and prompts as internal components.

## Problem Solved

* Traditional approach requires developers to manually author tool schemas and functions for each service integration (e.g., GitHub API tools).
* Maintenance burden increases for complex services with many features.

## MCP Solution

* Shifts tool definition and execution from the developer's server to a dedicated MCP server.
* MCP server acts as the interface to external services, wrapping functionality into pre-built tools.

## Key Benefits

* Eliminates need for developers to write or maintain tool schemas and function implementations.
* Tool creation is outsourced; the MCP server authors and packages tools.

## Common Questions

* **Who authors MCP servers?** Anyone, but often service providers create official implementations.
* **Difference from direct API calls?** Saves developer time by providing pre-built tool schemas/functions.
* **Relationship to tool use?** MCP focuses on who creates tools; tool use is complementary.

## Core Value

* Reduces developer burden by outsourcing tool creation to MCP server implementations instead of requiring custom tool development for each service integration.

---

# Transport & Communication

## Transport Agnostic

* Client/server can communicate via multiple protocols (stdin/stdout, HTTP, WebSockets, etc.).
* Common setup: both on the same machine using stdin/stdout.

## Communication

* Message exchange defined by MCP spec. Key message types:

  * **List tools request/result:** client asks server for available tools; server responds with tool list.
  * **Call tool request/result:** client asks server to run tool with arguments; server returns execution result.

## Typical Flow

```
User query 
  → Server asks MCP client for tools 
  → MCP client sends list tools request to MCP server 
  → Server gets tool list 
  → Server sends query + tools to Claude 
  → Claude requests tool execution 
  → Server asks MCP client to run tool 
  → MCP client sends call tool request to MCP server 
  → MCP server executes tool (e.g., GitHub API call) 
  → Results flow back through chain 
  → Claude formulates final response 
  → User gets answer
```

* **MCP Client:** acts as intermediary, does not execute tools itself, just facilitates communication.

---

# Project Structure & Setup

* **Project Structure:** Custom MCP client connects to custom MCP server (both built in same project).
* **Document System:** Fake documents stored in memory only (no persistence).
* **Server Tools:**

  1. `read_doc_contents` – reads document content.
  2. `edit_document` – updates document content.
* **Real-world Context:** Normally projects implement either client OR server; this project does both for learning.

### Setup Requirements

1. Download `CLI_project.zip`
2. Extract files
3. Configure `.env` with API key
4. Install dependencies

### Running Project

* With UV: `uv run main.py`
* Without UV: `python main.py`

### Verification

* Chat prompt appears and responds to basic queries (e.g., "what's one plus one").

---

# Tool Definitions

* **Syntax:** `@mcp.tool` decorator + function with typed parameters + Field descriptions.
* **Document Storage:** In-memory dictionary with `doc_id` keys and `content` values.
* **Tool Examples:**

  1. **read_doc_contents**

     * Parameter: `doc_id` (str)
     * Returns document content
     * Raises `ValueError` if document not found
  2. **edit_document**

     * Parameters: `doc_id`, `old_string`, `new_string`
     * Performs find/replace operation
     * Validates document existence

### MCP Python SDK Benefits

* Auto-generates JSON schemas from decorated functions.
* Single-line server creation.
* Eliminates manual schema writing.

### Parameter Definition

* Use `Field()` with description for tool arguments (import from `pydantic`).

### Error Handling

* Validate document existence before operations; raise `ValueError` for missing documents.

### Implementation Pattern

1. Decorator
2. Function definition
3. Parameter typing
4. Validation
5. Core logic

---

# Access & Interface

### Running MCP Server

```bash
mcp dev [server_file.py]
```

* Opens server on port; visit provided localhost address.

### Interface

* **Left Sidebar:** Connect button
* **Top Navigation:** Resources / Prompts / Tools sections
* **Tools Section:** Lists available tools; click to open right panel for manual testing

### Testing Process

1. Select tool
2. Input required parameters
3. Click **Run Tool**
4. Verify output / success message

### Key Features

* Live development testing
* Tool invocation simulation
* Parameter input fields
* Success/failure feedback

### Status

* Inspector in active development; UI may change, core functionality remains similar.

---

# MCP Client

* **Wrapper class** around client session for MCP server connection with resource cleanup.
* **Client Session:** Actual connection via MCP Python SDK, requires cleanup.
* **Client Purpose:** Exposes MCP server functionality to rest of codebase.

### Key Functions

```python
await client.list_tools()       # Returns result.tools
await client.call_tool(name, input)  # Executes tool on server
```

### Implementation Flow

1. Application requests tool list for Claude
2. Client retrieves server’s available tools
3. Claude selects tool & provides parameters
4. Client executes tool on server
5. Results returned to Claude

### Best Practices

* Wrap client session in larger class for resource management.

---

# Resources

* **Types:**

  * Direct/Static (e.g., `docs://documents`)
  * Templated (e.g., `documents/{doc_id}`)
* **Flow:**

  1. Client sends read resource request
  2. MCP server matches URI to function
  3. Server executes and returns result
  4. Client receives data via result message

### Implementation

* Use `@mcp.resource` decorator
* Define URI
* Set MIME type (e.g., `application/json`, `text/plain`)
* Templated URIs: parameters become function keyword args
* MCP Python SDK auto-serializes return values

### Client Parsing

* `read_resource` requests resource using:

```python
await self.session.read_resource(AnyUrl(uri))
```

* Parse result based on `mime_type`:

```python
if resource.mime_type == "application/json":
    return json.loads(resource.text)
else:
    return resource.text
```

---

# Prompts

* **Purpose:** Server-defined templates for AI instructions.
* **Implementation:**

```python
@prompt(name="format", description="rewrites document in markdown")
def format_document(doc_id: str) -> list[messages]:
    return [base.user_message(prompt_text)]
```

* **Workflow:** User types `/format` → selects document → server returns prompt → client sends to Claude.

### Key Features

* Encapsulates domain expertise in server-defined prompts
* Allows reusable, parameterized AI instructions

---

# Tools, Resources, Prompts Overview

| Type      | Trigger | Purpose                  |
| --------- | ------- | ------------------------ |
| Tools     | Model   | Claude decides execution |
| Resources | App     | Fetch data into app/UI   |
| Prompts   | User    | Predefined workflows     |

---

# Roots Feature

* **Problem:** Claude cannot locate files without full paths.
* **Solution:** Add 3 tools to MCP server:

  1. ConvertVideo
  2. ReadDirectory
  3. ListRoots
* **Root:** File/folder user grants permission for server access.
* **Benefits:**

  * Permission control
  * Autonomous file discovery
* **Limitation:** MCP SDK does not enforce roots; server developer must implement access checks.

---

# MCP Communication & Messaging

* **Format:** JSON messages between client and server
* **Categories:**

  * Request/Result pairs
  * Notifications (no response required)
* **Direction:**

  * Client messages → server
  * Server messages → client

### Stdio Transport

* Bidirectional via stdin/stdout
* Limitation: requires same machine

### HTTP Transport

* Restricted server-to-client messaging
* **Solution:** StreamableHTTP with SSE connections for server-to-client requests

### Session Flow (SSE)

1. Client sends `initialize_request`
2. Server responds with result + session ID
3. Client sends `initialized_notification`
4. Client optionally opens GET request for SSE streaming

---

# Flags Impacting Server Behavior

### Stateless HTTP

* Needed for horizontal scaling with multiple instances
* Effects: no session tracking, GET SSE disabled, sampling/progress/logs unavailable

### JSON Response

* Disables streaming intermediate messages
* POST returns only final result

---

# LLM Client Integration

* **Purpose:** Shifts LLM access from server to client
* **Benefits:** Reduces server complexity, removes API key requirements, prevents unauthorized token usage
* **Implementation:**

  * Server: `create_message()` function
  * Client: sampling callback handles LLM requests

---

# Tool Execution Callbacks

* **Server Side:**

  * Tool functions receive `context` object
  * `context.info()` logs messages
  * `context.report_progress()` updates progress

* **Client Side:**

  * Logging callback
  * Progress callback
  * Display handled by terminal or web UI

### Benefits

* Real-time feedback
* Prevents user confusion on long-running operations
* Optional for UX enhancement
