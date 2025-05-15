import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

export const welcome = () => {  
	return {  
	  welcome: "Welcome to the Vercel AI SDK with OpenAI Agent! I can help you build AI-powered applications using Vercel's AI SDK with OpenAI models.",  
	  prompts: [  
		{  
		  data: "How do I implement streaming responses with the Vercel AI SDK?",  
		  contentType: "text/plain",  
		},  
		{  
		  data: "Generate a poem about artificial intelligence",  
		  contentType: "text/plain",  
		}  
	  ],  
	};  
  };

export default async function Agent(
	req: AgentRequest,
	resp: AgentResponse,
	ctx: AgentContext,
) {
	const res = await generateText({
		model: openai("gpt-4o"),
		system: "You are a friendly assistant!",
		prompt: (await req.data.text()) ?? "Why is the sky blue?",
	});
	return resp.text(res.text);
}
