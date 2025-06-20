import os
from typing import Dict, Any
from agentuity import AgentRequest, AgentResponse, AgentContext
from rizaio import Riza

riza = Riza(api_key=os.getenv("RIZA_API_KEY"))

async def agent(req: AgentRequest, resp: AgentResponse, ctx: AgentContext):
    try:
        data = await req.data.json()
        language = data.get("language", "")
        code = data.get("code", "")
        
        if not language or not code:
            return resp.json({"error": "Both 'language' and 'code' parameters are required"})

        supported_languages = ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "RUBY", "PHP"]
        if language.upper() not in supported_languages:
            return resp.json({
                "error": f"Unsupported language: {language}. Supported languages: {', '.join(supported_languages)}"
            })

        ctx.logger.info(f"Executing {language} code via Riza")
        
        try:
            result = riza.command.exec(
                language=language.upper(),
                code=code
            )
            
            return resp.json({
                "success": True,
                "language": language,
                "stdout": result.stdout,
                "stderr": result.stderr or None,
                "exitCode": getattr(result, 'exit_code', 0)
            })
        except Exception as error:
            ctx.logger.error(f"Code execution failed: {error}")
            return resp.json({
                "success": False,
                "error": f"Code execution failed: {error}"
            })
    except Exception as error:
        ctx.logger.error(f"Error processing request: {error}")
        return resp.json({"error": "Failed to process request"})

def welcome():
    return {
        "welcome": "Welcome to the Riza agent! I can execute code securely using Riza's sandbox environment. I support Python, JavaScript, TypeScript, Ruby, and PHP.",
        "prompts": [
            {
                "data": {"language": "python", "code": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a)\n        a, b = b, a + b\n\nfibonacci(10)"},
                "contentType": "application/json"
            },
            {
                "data": {"language": "javascript", "code": "function sortNumbers(arr) {\n    return arr.sort((a, b) => a - b);\n}\n\nconsole.log(sortNumbers([64, 34, 25, 12, 22, 11, 90]));"},
                "contentType": "application/json"
            },
            {
                "data": {"language": "typescript", "code": "interface UserProfile {\n    id: number;\n    name: string;\n    email: string;\n    age?: number;\n}\n\nfunction validateUser(user: UserProfile): boolean {\n    return user.id > 0 && user.name.length > 0 && user.email.includes('@');\n}\n\nconst user: UserProfile = { id: 1, name: 'John', email: 'john@example.com' };\nconsole.log(validateUser(user));"},
                "contentType": "application/json"
            }
        ]
    }
