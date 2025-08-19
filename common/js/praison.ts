import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { Agent as PraisonAIAgent, PraisonAIAgents } from 'praisonai';

export const welcome = () => {
  return {
    welcome:
      'Welcome to the Praison AI TypeScript Agent! I can help you build production-ready multi-AI agent systems with self-reflection capabilities.',
    prompts: [
      {
        data: 'How do I create multi-agent systems with Praison AI?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the self-reflection capabilities of Praison AI agents?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function PraisonAgent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  try {
    const userMessage =
      (await req.data.text()) ??
      'Tell me about Praison AI and how it helps build multi-agent systems.';

    // Create a Praison AI agent with expertise in the framework
    const agent = new PraisonAIAgent({
      name: 'PraisonExpert',
      instructions: `You are an expert in Praison AI, a production-ready framework for creating multi-AI agent systems. 
      You specialize in explaining self-reflection capabilities, multi-agent coordination, CrewAI and AG2 integration, 
      low-code solutions, and building complex LLM systems. Provide detailed, practical information about Praison AI 
      development including code examples when appropriate.`,
      verbose: false,
    });

    // Initialize PraisonAIAgents with the single agent
    const praisonAI = new PraisonAIAgents({
      agents: [agent],
      tasks: [userMessage],
      verbose: false,
    });

    // Start the agent and get results
    const results = await praisonAI.start();

    // Extract the response text from the results array
    if (Array.isArray(results) && results.length > 0 && results[0]) {
      // Praison AI returns an array with the response as the first element
      return resp.text(results[0]);
    }
    if (typeof results === 'string') {
      return resp.text(results);
    }
    if (results && typeof results === 'object') {
      // Return as JSON if it's an object
      return resp.json(results);
    }
    return resp.text(
      "I'd be happy to help you with Praison AI multi-agent systems! Could you please provide more details about what you'd like to know?"
    );
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
