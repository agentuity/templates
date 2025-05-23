import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { GoogleGenAI } from '@google/genai';

// Get your API key here: https://aistudio.google.com/apikey
if (!process.env.GOOGLE_API_KEY) {
  console.error('Missing the GOOGLE_API_KEY environment variable');

  process.exit(1);
}

const google = new GoogleGenAI({ apiKey: process.env.GOOGLE_API_KEY });

export const welcome = () => {
  return {
    welcome:
      'Welcome to the Google AI TypeScript Agent! I can help you build AI-powered applications using Gemini models.',
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
  ctx: AgentContext,
) {
  try {
    const result = await google.models.generateContent({
      model: 'gemini-2.0-flash',
      contents: (await req.data.text()) ?? 'Hello, Gemini',
    });

    return resp.text(result.text ?? 'Something went wrong');
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
