import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import OpenAI from "openai";

const client = new OpenAI();

export const welcome = () => {  
	return {  
	  welcome: "Welcome to the OpenAI TypeScript Agent! I can help you interact with OpenAI models.",  
	  prompts: [  
		{  
		  data: "Generate a creative story about space exploration",  
		  contentType: "text/plain",  
		},  
		{  
		  data: "How can I use the OpenAI API for text completion?",  
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
	const completion = await client.chat.completions.create({
		messages: [
			{
				role: "user",
				content: (await req.data.text()) ?? "Say this is a test",
			},
		],
		model: "gpt-4o",
	});
	const message = completion.choices[0]?.message;
	return resp.text(message?.content ?? "Something went wrong");
}
