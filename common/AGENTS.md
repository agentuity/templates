# Agentuity Configuration Guidelines

This guide provides instructions for working with Agentuity configuration files and project setup.

## 1. Agentuity Configuration File

The `agentuity.yaml` file is used by Agentuity to configure the AI Agent project. You should NOT suggest edits to this file unless specifically requested, as it contains critical project configuration managed by the Agentuity platform.

## 2. Project Structure

Follow the established project structure for your chosen runtime:

- **Python projects**: Use the `agentuity_agents/` directory for agent implementations
- **JavaScript/TypeScript projects**: Use the `src/agents/` directory for agent implementations
- **Configuration files**: Keep `agentuity.yaml`, `.env` files, and other configuration in the project root

## 3. Development Workflow

- Use `agentuity dev` to start the development server
- Use `agentuity agent create` to scaffold new agents
- Use `agentuity deploy` to deploy your agents to production
- Follow the runtime-specific guidelines in your project's AGENTS.md file

## 4. Environment Management

- Use `.env.development` for development-specific environment variables
- Use `.env.production` for production environment variables
- Never commit sensitive credentials to version control
- Use the Agentuity Console for managing secrets in production
