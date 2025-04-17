import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { Agent, Memory } from '@mastra/core';
import { openai } from '@ai-sdk/openai';

const memory = new Memory();

const simpleWorkflow = {
  start: (input: string) => ({
    llm: {
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: input || 'Hello, who are you?' }
      ],
      model: openai('gpt-4o-mini'),
    },
    then: (response) => {
      return { result: response.content };
    }
  })
};

const mastraAgent = new Agent({
  name: '{{ .AgentName }}',
  instructions: 'You are a helpful assistant that provides concise and accurate information.',
  model: openai('gpt-4o-mini'),
  memory,
  workflow: { simpleWorkflow }
});

export default async function Agent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext,
) {
  try {
    const result = await mastraAgent.run('start', req.input || 'Hello, who are you?');
    ctx.logger.info('Workflow result:', result);
    
    return resp.text(result.result);
  } catch (error) {
    ctx.logger.error('Error running agent:', error);
    return resp.text('Sorry, there was an error processing your request.');
  }
}
