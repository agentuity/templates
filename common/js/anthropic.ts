import type { AgentRequest, AgentResponse, AgentContext } from '@agentuity/sdk';
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

export const welcome = () => {
  return {
    welcome:
      'Welcome to the Anthropic TypeScript Agent! I can help you interact with Claude models for natural language tasks.',
    prompts: [
      {
        data: 'Write a creative story about a journey through time',
        contentType: 'text/plain',
      },
      {
        data: 'Explain quantum computing to a high school student',
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
  const message = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-latest',
    max_tokens: 1024,
    messages: [
      { role: 'user', content: (await req.data.text()) ?? 'Hello, Claude' },
    ],
  });
  return resp.text(message.content[0].text);
}
