import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

export default async function AgentuityAgent(
	req: AgentRequest,
	resp: AgentResponse,
	ctx: AgentContext,
) {
	try {
		const agent = new Agent({
			name: "{{ .AgentName }}",
			instructions:
				"You are a helpful assistant that provides concise and accurate information.",
			model: openai("gpt-4o-mini"),
		});

		const result = await agent.generate(
			(await req.data.text()) || "Hello, who are you?",
		);
		return resp.text(result.text);
	} catch (error) {
		ctx.logger.error("Error running agent:", error);
		return resp.text("Sorry, there was an error processing your request.");
	}
}
