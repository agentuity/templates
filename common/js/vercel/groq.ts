import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { groq } from '@ai-sdk/groq';
import { streamText } from 'ai';

export const welcome = () => {
  return {
    welcome:
      "Welcome to the Vercel AI SDK with Groq and Llama! I can help you build AI-powered applications using Vercel's AI SDK with Groq powered models.",
    prompts: [
      {
        data: 'How do I implement streaming responses with Groq?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the best practices for prompt engineering with Llama?',
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
    const result = await streamText({
      model: groq('llama-3.1-8b-instant'),
      prompt: (await req.data.text()) ?? 'Hello, Groq',
    });

    return resp.stream(result.textStream, 'text/markdown');
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
