import type { AgentRequest, AgentResponse, AgentContext } from "@agentuity/sdk";
import { Riza } from "@riza-io/api";

const riza = new Riza({
  apiKey: process.env.RIZA_API_KEY,
});

export default async function Agent(req: AgentRequest, resp: AgentResponse, ctx: AgentContext) {
  try {
    const { language, code } = await req.data.json() as { language: string; code: string };
    
    if (!language || !code) {
      return resp.json({ error: "Both 'language' and 'code' parameters are required" });
    }

    const supportedLanguages = ["python", "javascript", "typescript", "ruby", "php"];
    if (!supportedLanguages.includes(language.toLowerCase())) {
      return resp.json({ 
        error: `Unsupported language: ${language}. Supported languages: ${supportedLanguages.join(", ")}` 
      });
    }

    ctx.logger.info(`Executing ${language} code via Riza`);
    
    try {
      const result = await riza.command.exec({
        language: language.toLowerCase() as "python" | "javascript" | "typescript" | "ruby" | "php",
        code: code,
      });
      
      return resp.json({
        success: true,
        language: language,
        stdout: result.stdout,
        stderr: result.stderr || null,
        exitCode: result.exit_code || 0
      });
    } catch (error) {
      ctx.logger.error("Code execution failed: %s", error);
      return resp.json({ 
        success: false,
        error: `Code execution failed: ${error}` 
      });
    }
  } catch (error) {
    ctx.logger.error("Error processing request: %s", error);
    return resp.json({ error: "Failed to process request" });
  }
}

export function welcome() {
  return {
    welcome: "Welcome to the Riza agent! I can execute code securely using Riza's sandbox environment. I support Python, JavaScript, TypeScript, Ruby, and PHP.",
    prompts: [
      {
        data: { language: "python", code: "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a)\n        a, b = b, a + b\n\nfibonacci(10)" },
        contentType: "application/json"
      },
      {
        data: { language: "javascript", code: "function sortNumbers(arr) {\n    return arr.sort((a, b) => a - b);\n}\n\nconsole.log(sortNumbers([64, 34, 25, 12, 22, 11, 90]));" },
        contentType: "application/json"
      },
      {
        data: { language: "typescript", code: "interface UserProfile {\n    id: number;\n    name: string;\n    email: string;\n    age?: number;\n}\n\nfunction validateUser(user: UserProfile): boolean {\n    return user.id > 0 && user.name.length > 0 && user.email.includes('@');\n}\n\nconst user: UserProfile = { id: 1, name: 'John', email: 'john@example.com' };\nconsole.log(validateUser(user));" },
        contentType: "application/json"
      }
    ]
  };
}
