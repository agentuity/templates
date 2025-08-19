# Agent Instructions for Agentuity Templates

## Commands
- `npm run lint` - Run Biome linter with error-on-warnings flag
- `npm run format` - Auto-format code with Biome
- `npm test` - Currently not configured (returns error message)

## Architecture
This is a templates repository for the Agentuity Cloud Platform. It contains:
- Runtime-specific template definitions (`bunjs/`, `nodejs/`, `python-uv/`)
- Shared template files in `common/` (JavaScript/TypeScript in `js/`, Python in `py/`)
- Schema validation via JSON schemas (`templates.schema.json`, `runtimes.schema.json`, `rules.schema.json`)
- Runtime definitions in `runtimes.yaml` supporting Bun, Node.js, and Python+uv
- Template structure uses YAML with templating variables like `{{ .AgentName | safe_filename }}`

## Code Style
- Use Biome for linting and formatting
- 2-space indentation, single quotes, trailing commas (ES5), always semicolons
- Files to ignore: `.agentuity/**`
- Follow existing patterns in template files
- YAML files must include schema reference at top: `# yaml-language-server: $schema=...`
- Template filenames support Go template syntax with `safe_filename` filter

## Conventions
- Templates stored per runtime: `{runtime}/templates.yaml`
- Common files in `common/{js,py}/` for reusable template code
- Use clear naming and detailed descriptions in templates
- Test templates locally with `agentuity new --templates-dir=/path/to/templates`

## Framework Implementation Process
When adding new AI agent frameworks to the templates:

### 1. Research Phase
- Research the framework's SDK installation and basic API usage
- Identify correct package names and version requirements
- Find official examples and documentation for basic agent creation
- Check for Python vs JavaScript/TypeScript support

### 2. Template Implementation
- Add new template entry to appropriate `{runtime}/templates.yaml`
- Include proper package installation via `uv add` (Python) or `bun add` (JS)
- Create template file in `common/{js,py}/` directory
- Follow existing patterns: `welcome()` function and async `run()` function
- Use proper error handling and logging via `context.logger.error()`

### 3. Template Testing Process
- Create test project: `agentuity new test-project "Description" AgentName "Agent desc" --dir /path/to/test --runtime {runtime} --template "Framework Name" --templates-dir /path/to/templates --force --auth none`
- Run dev server in background: `agentuity dev > /tmp/framework.log 2>&1 &`
- Wait for server startup and extract port: `grep "Starting server on port" /tmp/framework.log`
- Get agent ID from agentuity.yaml: `grep "id:" /path/to/test/agentuity.yaml` or read the agents section
- Test with curl: `curl -X POST http://127.0.0.1:{port}/{agent_id} -H "Content-Type: text/plain" -d "test message"`
- Verify no errors and appropriate responses
- Clean up: `kill $(pgrep -f "agentuity dev")` and `rm -rf /path/to/test`

### 4. Common Issues & Solutions
- **API Version Changes**: Framework APIs change between versions, check migration guides
- **Interactive Input**: Avoid agents that require interactive user input (use direct message APIs)
- **Async/Await**: Most modern frameworks use async patterns, ensure proper `await` usage
- **Resource Cleanup**: Always close model clients and connections properly
- **Template vs Project Files**: Remember template changes only affect new projects, existing projects need manual updates
- **Port Conflicts**: When testing, agentuity may choose different ports due to conflicts - extract actual port from logs
- **Response Types**: Use `resp.text()` for strings, `resp.json()` for objects, handle arrays appropriately
- **Import Conflicts**: In TypeScript, use import aliases (e.g., `Agent as PraisonAgent`) to avoid function name conflicts

### 5. Successfully Implemented Frameworks
- **OpenAI Swarm**: Multi-agent orchestration with agent handoffs (`git+https://github.com/openai/swarm.git`)
- **Microsoft AutoGen**: Collaborative AI workflows (`autogen-agentchat`, `autogen-ext[openai]`)
- **Haystack**: RAG and semantic search applications (`haystack-ai`, `sentence-transformers`)
- **AWS Strands**: Model-driven AI agents with tool integration (`strands-agents`, `strands-agents-tools`)
- **VoltAgent**: TypeScript framework for workflow orchestration and multi-agent systems (`@voltagent/core`, `@voltagent/vercel-ai`)
- **Praison AI**: Production-ready multi-AI agent systems with self-reflection (`praisonaiagents`)
- **LangGraph**: Stateful AI agents with graph-based workflows and human-in-the-loop controls (`langgraph`, `langchain-openai`, `langchain-core`)
- **LangChain**: LLM-powered applications with chains, agents, and memory (`@langchain/core`, `@langchain/openai`)

## Template Development Troubleshooting

### Getting Project Metadata
- **Agent ID**: Found in `agentuity.yaml` under the `agents` section: `agents[0].id`
- **Port Information**: Default port is 3500, but conflicts cause dynamic assignment
- **Project Structure**: TypeScript projects use `src/agents/`, Python projects use `agentuity_agents/`

### Debugging Failed Agents
- **Check Logs**: Use `tail -20 /tmp/framework.log` to see latest errors
- **TypeScript Errors**: Look for import conflicts, missing types, or wrong method signatures
- **Python Errors**: Check for missing dependencies, async/sync mismatches, or API changes
- **Port Issues**: Extract port from logs with `grep "Starting server on port\|Bun server started on port"`

### Response Handling Patterns
- **Text Responses**: Use `resp.text(string)` for simple string responses
- **JSON Responses**: Use `resp.json(object)` for complex objects or arrays
- **Array Results**: Extract text first: `results[0]` then use `resp.text()`
- **Fallback Responses**: Always provide meaningful fallback messages

### Framework-Specific Debugging
- **Module Import Issues**: Use dynamic imports or aliases to avoid conflicts
- **Model Configuration**: Prefer OpenAI models for compatibility, avoid AWS/cloud-specific defaults
- **Authentication**: Use model providers that work without additional credentials setup
- **Async Operations**: Wrap synchronous framework calls with `asyncio.to_thread()` in Python
- **GPT-5 Compatibility**: Most frameworks support GPT-5, but AutoGen requires GPT-4 due to model validation
- **Model Updates**: Some frameworks haven't updated their model validation for newest models
