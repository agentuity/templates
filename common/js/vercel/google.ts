import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { google } from '@ai-sdk/google';
import { streamText } from 'ai';

export const welcome = () => {
  return {
    welcome:
      "Welcome to the Vercel AI SDK with Google AI Agent! I can help you build AI-powered applications using Vercel's AI SDK with Gemini models.",
    prompts: [
      {
        data: 'How do I implement streaming responses with Gemini models?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the best practices for prompt engineering with Gemini?',
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
      model: google('gemini-2.0-flash'),
      system:
        'You are a helpful assistant that provides concise and accurate information.',
      prompt: (await req.data.text()) ?? 'Hello, Gemini',
    });

    return resp.stream(result.textStream);
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
