import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { streamText } from "ai";
import { groq } from "@ai-sdk/groq";

export const welcome = () => {
	return {
		welcome:
			"Welcome to the Vercel AI SDK with Groq + LLAMA Agent! I can help you build AI-powered applications using Vercel's AI SDK with Groq powered models.",
		prompts: [
			{
				data: "What is Groq so fast in AI Inference?",
				contentType: "text/plain",
			},
			{
				data: "What are the best practices for prompt engineering with LLAMA?",
				contentType: "text/plain",
			},
		],
	};
};

export default async function Agent(
	req: AgentRequest,
	resp: AgentResponse,
	ctx: AgentContext,
) {
	const result = streamText({
		model: groq("llama-3.3-70b-versatile"),
		prompt:
			(await req.data.text()) ??
			"Why do Vercel and Groq work so well together?",
	});
	return resp.stream(result.textStream, "text/markdown");
}
