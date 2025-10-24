# Agentuity JavaScript/TypeScript Agent Development

This guide provides comprehensive instructions for developing AI agents using the Agentuity platform with JavaScript and TypeScript.

## 1. Agent Development Guidelines

- Prefer using the `agentuity agent create` command to create a new Agent
- Prefer loading types from the node modules package `@agentuity/sdk` in the node_modules folder
- The file should export a default function
- Prefer naming the default function Agent or the name of the Agent based on the context of the Agent description
- All code should be in TypeScript format
- Use the provided logger from the `AgentContext` interface such as `ctx.logger.info("my message: %s", "hello")`

### Example Agent File

```typescript
import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";

export default async function Agent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext,
) {
  return resp.json({ hello: "world" });
}
```

## 2. Core Interfaces

### AgentHandler

The main handler function type for an agent:

```typescript
type AgentHandler = (
  request: AgentRequest,
  response: AgentResponse,
  context: AgentContext,
) => Promise<AgentResponseType>;
```

### AgentRequest

The `AgentRequest` interface provides methods for accessing request data:

- `request.trigger`: Gets the trigger type of the request
- `request.metadata(key, defaultValue)`: Gets metadata associated with the request
- `request.get(key, defaultValue)`: Gets the metadata value of the request
- `request.data.contentType`: Gets the content type of the request payload
- `request.data.json(): Promise<Json>`: Gets the payload as a JSON object
- `request.data.text(): Promise<string>`: Gets the payload as a string
- `request.data.buffer(): Promise<ArrayBuffer>`: Gets the payload as a ArrayBuffer
- `request.data.binary(): Promise<ArrayBuffer>`: Gets the payload as a ArrayBuffer
- `request.data.object<T>: Promise<T>`: Gets the payload as a typed object

### AgentResponse

The `AgentResponse` interface provides methods for creating responses:

- `response.json(data, metadata)`: Creates a JSON response
- `response.text(data, metadata)`: Creates a text response
- `response.binary(data, metadata)`: Creates a binary response
- `response.html(data, metadata)`: Creates an HTML response
- `response.empty(metadata)`: Creates an empty response
- `response.handoff(agent, args?)`: Redirects to another agent within the same project

### AgentContext

The `AgentContext` interface provides access to various capabilities:

- `context.logger`: Logging functionality
- `context.kv`: Key-Value storage
- `context.vector`: Vector storage
- `context.getAgent(params)`: Gets a handle to a remote agent
- `context.tracer`: OpenTelemetry tracing

## 3. Storage APIs

### Key-Value Storage

Access through `context.kv`:

- `context.kv.get(name, key)`: Retrieves a value
- `context.kv.set(name, key, value, params)`: Stores a value with optional params (KeyValueStorageSetParams)
- `context.kv.delete(name, key)`: Deletes a value

### Vector Storage

Access through `context.vector`:

- `context.vector.upsert(name, ...documents)`: Inserts or updates vectors
- `context.vector.search(name, params)`: Searches for vectors
- `context.vector.delete(name, ...ids)`: Deletes vectors

## 4. Logging

Access through `context.logger`:

- `context.logger.debug(message, ...args)`: Logs a debug message
- `context.logger.info(message, ...args)`: Logs an informational message
- `context.logger.warn(message, ...args)`: Logs a warning message
- `context.logger.error(message, ...args)`: Logs an error message
- `context.logger.child(opts)`: Creates a child logger with additional context

## 5. Best Practices

- Use TypeScript for better type safety and IDE support
- Import types from `@agentuity/sdk`
- Use structured error handling with try/catch blocks
- Leverage the provided logger for consistent logging
- Use the storage APIs for persisting data
- Consider agent communication for complex workflows

## 6. How to use the documentation site, its APIs, etc.

The Agentuity documentation site provides API endpoints that AI agents can use to search and read documentation programmatically.

For the complete docs: https://agentuity.dev
The public repo markdown files are here: https://github.com/agentuity/docs/tree/main/content
For complete JS SDK documentation, visit: https://agentuity.dev/SDKs/javascript/api-reference

With that in mind, here are some helpful things you can do to find the right doc information:

**Base URL:** `https://agentuity.dev`

### Quick Reference

```bash
# Set base URL once per session
BASE="https://agentuity.dev"

# Ask a question (AI-powered with RAG)
curl -sG "$BASE/api/rag-search" --data-urlencode "query=How do I create an agent?"

# Search documentation (keyword search)
curl -sG "$BASE/api/search" --data-urlencode "query=environment variables"

# Read full page content
curl -sG "$BASE/api/page-content" --data-urlencode "path=Introduction/getting-started"
```

### API Endpoints

#### 1. RAG Search (Recommended for Questions)

**Use when:** You have a natural-language question and want an AI-generated answer with supporting documentation.

```bash
curl -sG "https://agentuity.dev/api/rag-search" \
  --data-urlencode "query=How do I use KV?"
```

**Response Format:**

```json
[
  {
    "id": "ai-answer-...",
    "url": "#ai-answer",
    "title": "AI Answer",
    "content": "AI-generated answer to your question...",
    "type": "ai-answer"
  },
  {
    "id": "doc-...",
    "url": "/getting-started/installation",
    "title": "Installation Guide",
    "content": "Brief snippet of the document...",
    "type": "document"
  }
]
```

**Workflow:**

1. Get the `ai-answer` item for a quick response
2. Extract `document` items for supporting documentation
3. Use the `url` field to read full page content (see Page Content API)

#### 2. Keyword Search (Deterministic)

**Use when:** You need exact keyword matches or when RAG is unavailable.

```bash
curl -sG "https://agentuity.dev/api/search" \
  --data-urlencode "query=agent create"
```

**Response Format:**

```json
[
  {
    "id": "/guide/agents",
    "type": "page",
    "content": "Creating Agents",
    "url": "/guide/agents"
  },
  {
    "id": "/guide/agents-12",
    "type": "text",
    "content": "Use the CLI to create a new agent...",
    "url": "/guide/agents#create"
  }
]
```

#### 3. Page Content (Full Markdown)

**Use when:** You need the complete markdown content of a specific documentation page.

```bash
curl -sG "https://agentuity.dev/api/page-content" \
  --data-urlencode "path=getting-started/quickstart"
```

**Path Format:**

- Remove leading slash: `/getting-started/quickstart` → `getting-started/quickstart`
- Remove trailing slashes
- Remove URL fragments: `guide/install#linux` → `guide/install`
- For index pages, use just the folder name: `getting-started` resolves to `getting-started/index.mdx`

**Convert URL to Path (one-liner):**

```bash
PATH="$(echo "$URL" | sed -E 's#^/##; s#/+$##; s/#.*$//')"
```

**Response Format:**

```json
{
  "content": "# Quickstart\n\nFull markdown content here...",
  "title": "Quickstart Guide",
  "description": "Get started quickly with Agentuity",
  "path": "getting-started/quickstart"
}
```

**Path Validation:**

- Paths cannot contain `..`, `\`, or start with `/`
- Returns 404 if page not found

### When to Use Which API

| Scenario                | Recommended API                            | Reason                                |
| ----------------------- | ------------------------------------------ | ------------------------------------- |
| "How do I..." questions | `/api/rag-search`                          | AI-generated answer + supporting docs |
| Exact term search       | `/api/search`                              | Fast, deterministic keyword matching  |
| Reading specific page   | `/api/page-content`                        | Full markdown with proper formatting  |
| Error message lookup    | `/api/search`                              | Exact text matching                   |
| Multi-step tutorials    | `/api/rag-search` then `/api/page-content` | Get overview, then deep dive          |

### Best Practices

1. **Start with RAG for questions:** It provides both answers and relevant documentation links
2. **Use keyword search for known terms:** When you know exactly what you're looking for
3. **Fetch full content for citations:** Always read the complete page when citing documentation
4. **Cache results:** Avoid repeated API calls for the same content
5. **Handle fallbacks:** If RAG fails, fall back to keyword search
