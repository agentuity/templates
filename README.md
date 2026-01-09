<div align="center">
    <img src="https://raw.githubusercontent.com/agentuity/templates/main/.github/Agentuity.png" alt="Agentuity" width="100"/> <br/>
    <strong>Build Agents, Not Infrastructure</strong> <br/>
<br />
<a href="https://github.com/agentuity/sdk-js/blob/main/README.md"><img alt="License" src="https://badgen.now.sh/badge/license/Apache-2.0"></a>
<a href="https://discord.gg/agentuity"><img alt="Join the community on Discord" src="https://img.shields.io/discord/1332974865371758646.svg?style=flat"></a>
</div>
</div>

# Agentuity Project Templates

> [!WARNING]
> This repo has now been deprecated in favor of the new opensource [SDK mono repo](https://github.com/agentuity/sdk) and will be archived soon.


These are templates for Agentuity projects. They are designed to help you get started with building your own Agents using the Agentuity Cloud Platform.

These templates are automatically available when using the `agentuity new` command from the [Agentuity CLI](https://github.com/agentuity/cli).

## Creating Templates

Templates define the structure and dependencies for new Agentuity agent projects. This guide explains how to create and contribute templates to this repository.

### Template Structure

Templates are defined in YAML files located in runtime-specific directories:
- `nodejs/templates.yaml` - Templates for Node.js runtime
- `bunjs/templates.yaml` - Templates for Bun.js runtime
- `python-uv/templates.yaml` - Templates for Python with uv runtime

Each template file must include a schema reference at the top:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/agentuity/templates/main/templates.schema.json
```

### Template Definition

A template is defined as a YAML object with the following required fields:

```yaml
- name: "Template Name"
  description: "A detailed description of what this template provides"
  steps:
    # List of steps to execute when this template is selected
    # ...
```

#### Required Fields

- `name`: A descriptive name for the template
- `description`: A detailed explanation of what the template provides
- `steps`: An array of steps to execute when the template is selected

#### Optional Fields

- `skip_agent_step`: Boolean flag to skip the agent step for this template (defaults to false)

### Template Steps

Steps define the actions to be performed when a template is selected. Each step must be one of the following types:

#### 1. Package Installation

Installs dependencies using the appropriate package manager:

```yaml
- command: npm  # or bun, uv depending on runtime
  args:
    - install  # or add for bun, add for uv
    - --no-fund  # optional flags
    - --no-audit  # optional flags
    - package-name  # package to install
    - another-package  # additional packages
```

#### 2. File Creation

Creates a new file from a template or source file:

```yaml
# Using a source file
- action: create_file
  filename: "src/agents/{{ .AgentName | safe_filename }}/index.ts"
  from: "common/js/openai.ts"

# Using a template file
- action: create_file
  filename: "agents/{{ .AgentName | safe_filename }}/agent.py"
  template: "common/py/crewai/agent.py"
```

The `filename` supports template variables:
- `{{ .AgentName }}` - The name of the agent provided by the user
- `{{ .AgentName | safe_filename }}` - The agent name sanitized for use in filenames

#### 3. Directory Copying

Copies an entire directory:

```yaml
- action: copy_dir
  from: "common/py/crewai/config"
  to: "agents/{{ .AgentName | safe_filename }}/config"
```

#### 4. Repository Cloning

Clones a GitHub repository:

```yaml
- action: clone_repo
  repo: "agentuity/agent-react-miami-concierge-template"
  to: "optional/target/directory"  # Optional, defaults to project directory
  branch: "main"  # Optional, defaults to the default branch
```

### Template Files

Template files are stored in the `common` directory:
- `common/js/` - JavaScript/TypeScript template files
- `common/py/` - Python template files

These files contain the actual code that will be used in the new agent projects.

### Example Templates

#### JavaScript/TypeScript Example

```yaml
- name: "OpenAI SDK for TypeScript"
  description: "Official TypeScript library for OpenAI"
  steps:
    - command: npm
      args:
        - install
        - --no-fund
        - --no-audit
        - openai
    - action: create_file
      filename: "src/agents/{{ .AgentName | safe_filename }}/index.ts"
      from: "common/js/openai.ts"
```

#### Python Example

```yaml
- name: "LangChain"
  description: "LangChain Python SDK with OpenAI"
  steps:
    - command: uv
      args:
        - add
        - --quiet
        - langchain
        - langchain-openai
        - langchain-community
    - action: create_file
      filename: "agents/{{ .AgentName | safe_filename }}/agent.py"
      from: "common/py/langchain/openai.py"
```

#### Complex Example with Multiple Steps

```yaml
- name: "CrewAI"
  description: "CrewAI Python SDK"
  steps:
    - command: uv
      args:
        - add
        - --quiet
        - crewai
    - action: create_file
      filename: "agents/{{ .AgentName | safe_filename }}/agent.py"
      template: "common/py/crewai/agent.py"
    - action: create_file
      filename: "agents/{{ .AgentName | safe_filename }}/crew.py"
      template: "common/py/crewai/crew.py"
    - action: copy_dir
      from: "common/py/crewai/config"
      to: "agents/{{ .AgentName | safe_filename }}/config"
```

### Testing Templates Locally

To test your templates locally, use the Agentuity CLI with the flag to override the templates directory:

```bash
agentuity new --templates-dir=/path/to/your/templates
```

This allows you to test your templates before submitting a pull request.

### Best Practices

1. **Clear Naming**: Use descriptive names for templates that indicate their purpose
2. **Detailed Descriptions**: Provide comprehensive descriptions to help users understand what the template offers
3. **Minimal Dependencies**: Only include necessary dependencies in your template
4. **Consistent Structure**: Follow the existing patterns for file organization
5. **Schema Validation**: Ensure your template conforms to the schema defined in `templates.schema.json`
6. **Test Thoroughly**: Test your template with the CLI before submitting

## Pull Requests

We welcome pull requests! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

See the [LICENSE](LICENSE.md) file for details.
