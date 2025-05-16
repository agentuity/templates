import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { GoogleGenAI } from "@google/genai";

// Get your API key here: https://aistudio.google.com/apikey
const google = new GoogleGenAI({ apiKey: process.env.GOOGLE_API_KEY! });

export const welcome = () => {
  return {
    welcome:
      "Welcome to the Google AI TypeScript Agent! I can help you interact with Gemini models for natural language tasks.",
    prompts: [
      {
        data: "Write a creative story about a journey through time",
        contentType: "text/plain",
      },
      {
        data: "Explain quantum computing to a high school student",
        contentType: "text/plain",
      },
    ],
  };
};

export default async function Agent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  const message = await google.models.generateContent({
    model: "gemini-2.0-flash",
    contents: (await req.data.text()) ?? "Explain how AI works in a few words",
  });

  return resp.text(message.text ?? "");
}
