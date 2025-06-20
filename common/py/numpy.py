from agentuity import AgentRequest, AgentResponse, AgentContext
import numpy as np

def welcome():
    return {
        "welcome": "Welcome to the NumPy Python Agent! I can help you with numerical computations and array operations using NumPy.",
        "prompts": [
            {
                "data": "Create a random array and calculate its statistics",
                "contentType": "text/plain"
            },
            {
                "data": "Perform matrix multiplication with two arrays",
                "contentType": "text/plain"
            },
            {
                "data": "Generate a sine wave using NumPy",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_input = await request.data.text() or "demo"
        
        if "random" in user_input.lower() or "statistics" in user_input.lower() or user_input == "demo":
            arr = np.random.rand(10, 5)
            stats = {
                "shape": arr.shape,
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr))
            }
            
            result = f"Generated random array with shape {stats['shape']}\n"
            result += f"Statistics:\n"
            result += f"  Mean: {stats['mean']:.4f}\n"
            result += f"  Standard Deviation: {stats['std']:.4f}\n"
            result += f"  Min: {stats['min']:.4f}\n"
            result += f"  Max: {stats['max']:.4f}\n"
            result += f"\nFirst few values:\n{arr[:3, :3]}"
            
        elif "matrix" in user_input.lower() or "multiplication" in user_input.lower():
            a = np.random.rand(3, 4)
            b = np.random.rand(4, 2)
            c = np.dot(a, b)
            
            result = f"Matrix A (3x4):\n{a}\n\n"
            result += f"Matrix B (4x2):\n{b}\n\n"
            result += f"Result C = A × B (3x2):\n{c}"
            
        elif "sine" in user_input.lower() or "wave" in user_input.lower():
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x)
            
            result = f"Generated sine wave with {len(x)} points\n"
            result += f"X range: {x[0]:.2f} to {x[-1]:.2f}\n"
            result += f"Y range: {np.min(y):.2f} to {np.max(y):.2f}\n"
            result += f"Sample points (x, y):\n"
            for i in range(0, len(x), 20):
                result += f"  ({x[i]:.2f}, {y[i]:.4f})\n"
                
        else:
            arr = np.array([1, 2, 3, 4, 5])
            squared = np.square(arr)
            sum_val = np.sum(arr)
            
            result = f"NumPy demonstration:\n"
            result += f"Original array: {arr}\n"
            result += f"Squared array: {squared}\n"
            result += f"Sum: {sum_val}\n"
            result += f"Mean: {np.mean(arr):.2f}\n"
            result += f"\nTry asking about 'random statistics', 'matrix multiplication', or 'sine wave'!"

        return response.text(result)
        
    except Exception as e:
        context.logger.error(f"Error running NumPy agent: {e}")
        return response.text("Sorry, there was an error processing your NumPy request.")
