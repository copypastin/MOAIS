import asyncio
import os
from src.utils import CopilotInstance

async def GenerateSolution():
    copilot = CopilotInstance.CopilotInstance(output=True)

    await copilot.initalize()

    problem_path = os.path.join(os.path.dirname(__file__), "problem.txt")
    output_path = os.path.join(os.path.dirname(__file__), "output/sample_output.py")
    print(f"Problem file path: {problem_path}")
    print(f"Output file path: {output_path}")

    # await copilot.generateCode(problem_path, output_path)
    await copilot.bulkGenerateCode([problem_path], os.path.dirname(output_path), 100)


    await copilot.close()

asyncio.run(GenerateSolution())
#  python -m src.test.Tic-Tac-Toe\ Case.tictactoe_gen