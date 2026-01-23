import asyncio
import os
import time
from copilot import CopilotClient

"""
    This program uses the Copilot CLI to generate code snippets based on user-provided prompts.

    This makes it easily accessible for developers who have the Github and Copilot CLI installed and no API keys.

    Use cautiously if you are Copilot user paying per request.
"""


class CopilotInstance:
    def __init__(self, language = "Python", output: bool = False):
        self.AGENT_PROMPT = f"Please solve the following prgramming challenge. Your response must be 100% {language} code."
        self.output = output

    async def initalize(self, model: str = "gpt-4.1"):
        self.client = CopilotClient()
        await self.client.start()
        self.session = await self.client.create_session({"model": model})

    async def test(self, prompt:str = "What is 2 + 2?"):
        response =  await self.session.send_and_wait({"prompt": prompt})
        print(response.data.content)

    async def generateCode(self, documents: str | list[str], output_path: str):
        response = ""

        await self._recycleSession()

        # Convert to list of attachment objects
        if isinstance(documents, str, ):
            documents = [documents]
        
        attachments = [{"type": "file", "path": doc} for doc in documents]

        response = await self.session.send_and_wait({
            "prompt": self.AGENT_PROMPT, 
            "attachments": attachments
        })

        if self.output:
            print("Writing response to file...")


        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            # Remove the "```" from the start and end of the response
            f.write((response.data.content)[9:-3])
        print(f"Response written to {output_path}")

        return response

    async def bulkGenerateCode(self, documents: list[str], output_dir: str, count: int = 0):

        i = 0
        while i < count:
            start_time = time.time()

            await self._recycleSession()
            await asyncio.gather(*[self.generateCode(documents, os.path.join(output_dir, f"output-{i}.py"))])
            i += 1

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Iteration {i} took {elapsed_time:.2f} seconds")

    async def _recycleSession(self):
        await self.session.abort()
        self.session = await self.client.create_session({"model": "gpt-4.1"})

    async def close(self):
        await self.client.stop()
