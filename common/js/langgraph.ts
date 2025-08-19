import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { ChatOpenAI } from '@langchain/openai';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';

export const welcome = () => {
  return {
    welcome:
      'Welcome to the LangGraph TypeScript Agent! I can help you build stateful AI agents with graph-based workflows and human-in-the-loop controls.',
    prompts: [
      {
        data: 'How do I create stateful agents with LangGraph workflows?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the advantages of using graph-based agent architectures?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function LangGraphAgent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  try {
    const userMessage =
      (await req.data.text()) ??
      'Tell me about LangGraph and its capabilities.';

    // Create a ChatOpenAI model
    const model = new ChatOpenAI({
      model: 'gpt-5-mini',
      temperature: 0,
    });

    // Create a prompt template
    const prompt = ChatPromptTemplate.fromTemplate(`
      You are an expert in LangGraph, the TypeScript framework for building stateful AI agents with graph-based workflows.
      You specialize in explaining StateGraph architecture, node and edge definitions, tool integration, human-in-the-loop controls,
      persistence, and ReAct patterns. Provide detailed, practical information about LangGraph development including code examples.
      
      Human: {input}
      Assistant:`);

    // Create an output parser
    const outputParser = new StringOutputParser();

    // Create a chain
    const chain = prompt.pipe(model).pipe(outputParser);

    // Invoke the chain with the user message
    const result = await chain.invoke({
      input: userMessage,
    });

    return resp.text(result);
  } catch (error) {
    ctx.logger.error('Error running agent:', error);

    return resp.text('Sorry, there was an error processing your request.');
  }
}
