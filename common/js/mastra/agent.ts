import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { openai } from '@ai-sdk/openai';
import { Agent } from '@mastra/core/agent';

export const welcome = () => {
  return {
    welcome:
      'Welcome to the Mastra TypeScript Agent Framework! I can help you build sophisticated AI applications using the Mastra framework.',
    prompts: [
      {
        data: 'How do I create a multi-step agent workflow with Mastra?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the core components of the Mastra framework?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function AgentuityAgent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  try {
    const agent = new Agent({
      name: '{{ .AgentName }}',
      model: openai('gpt-5-mini'),
      instructions:
        'You are a helpful assistant that provides concise and accurate information.',
    });

    const result = await agent.generate(
      (await req.data.text()) || 'Hello, Mastra'
    );

    return resp.text(result.text ?? 'Something went wrong');
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
