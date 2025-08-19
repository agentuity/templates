import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const welcome = () => {
  return {
    welcome:
      'Welcome to the VoltAgent TypeScript Agent! I can help you build scalable AI agents with workflow orchestration and multi-agent systems.',
    prompts: [
      {
        data: 'How do I create multi-agent workflows with VoltAgent?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the key features of VoltAgent for building AI agents?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function Agent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  try {
    const userMessage = (await req.data.text()) ?? 'Tell me about VoltAgent and its capabilities.';

    // Use AI SDK directly to demonstrate VoltAgent concepts
    // In a real VoltAgent application, you would use the VoltAgent framework
    // with proper agent orchestration, workflows, and tool integration
    const result = await generateText({
      model: openai('gpt-5-mini'),
      system: 'You are an expert in VoltAgent, a TypeScript framework for building and orchestrating AI agents. You help users understand workflow orchestration, multi-agent systems, tool integration, memory management, observability, and building scalable AI applications. Provide detailed, practical information about VoltAgent development including code examples when appropriate.',
      prompt: userMessage,
    });

    return resp.text(result.text);
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
