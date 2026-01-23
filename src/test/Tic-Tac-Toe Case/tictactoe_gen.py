import asyncio
import os
from src.utils import CopilotInstance

async def GenerateSolution():
    copilot = CopilotInstance.CopilotInstance(output=True, model="gpt-4.1")

    await copilot.initalize()

    problem_path = os.path.join(os.path.dirname(__file__), "problem.txt")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    # Read the problem file
    with open(problem_path, 'r') as f:
        problem_text = f.read()
    
    print(f"Problem file path: {problem_path}")
    print(f"Output directory: {output_dir}")

    # Pass raw text to generateCode
    await copilot.bulkGenerateCode(problem_text, output_dir, 100)

    await copilot.close()

asyncio.run(GenerateSolution())
#  python -m src.test.Tic-Tac-Toe\ Case.tictactoe_gen