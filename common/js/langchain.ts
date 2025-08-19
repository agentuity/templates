import type { AgentContext, AgentRequest, AgentResponse } from '@agentuity/sdk';
import { ChatOpenAI } from '@langchain/openai';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';

export const welcome = () => {
  return {
    welcome:
      'Welcome to the LangChain TypeScript Agent! I can help you build LLM-powered applications with chains, agents, and memory capabilities.',
    prompts: [
      {
        data: 'How do I create LLM chains with LangChain?',
        contentType: 'text/plain',
      },
      {
        data: 'What are the key components of LangChain for building AI applications?',
        contentType: 'text/plain',
      },
    ],
  };
};

export default async function LangChainAgent(
  req: AgentRequest,
  resp: AgentResponse,
  ctx: AgentContext
) {
  try {
    const userMessage = (await req.data.text()) ?? 'Tell me about LangChain and its capabilities.';

    // Create a ChatOpenAI model
    const model = new ChatOpenAI({
      model: 'gpt-5-mini',
      temperature: 0,
    });

    // Create a prompt template
    const prompt = ChatPromptTemplate.fromTemplate(`
      You are an expert in LangChain, the TypeScript/JavaScript framework for building LLM-powered applications.
      You specialize in explaining chains, agents, memory management, prompt templates, output parsers, and 
      building production-ready AI applications. Provide detailed, practical information about LangChain development.
      
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
