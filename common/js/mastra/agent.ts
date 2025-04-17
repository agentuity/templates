import { Agent, Memory } from '@mastra/core';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const simpleWorkflow = {
  start: () => ({
    llm: {
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Hello, who are you?' }
      ],
      model: openai('gpt-4o-mini'),
    },
    then: (response) => {
      console.log('Agent response:', response.content);
      return { result: response.content };
    }
  })
};

const memory = new Memory();

const agent = new Agent({
  name: '{{ .AgentName }}',
  instructions: 'You are a helpful assistant that provides concise and accurate information.',
  model: openai('gpt-4o-mini'),
  memory,
  workflow: { simpleWorkflow }
});

async function runAgent() {
  try {
    const result = await agent.run('start');
    console.log('Workflow result:', result);
    return result;
  } catch (error) {
    console.error('Error running agent:', error);
    throw error;
  }
}

export { agent, runAgent };
