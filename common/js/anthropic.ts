import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

export const welcome = () => {
  return {
    welcome:
      'Welcome to the Anthropic TypeScript Agent! I can help you build AI-powered applications using Claude models.',
    prompts: [
      {
        data: 'How do I implement streaming responses with Claude models?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the best practices for prompt engineering with Claude?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function Agent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext,
) {
  try {
    const result = await anthropic.messages.create({
      model: 'claude-3-7-sonnet-latest',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: (await req.data.text()) ?? 'Hello, Claude',
        },
      ],
    });

    return resp.text(result.content[0].text ?? 'Something went wrong');
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
