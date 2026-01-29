import asyncio
import os
import re
import time
import random
import string
from copilot import CopilotClient

"""
    This program uses the Copilot CLI to generate code snippets based on user-provided prompts.

    This makes it easily accessible for developers who have the Github and Copilot CLI installed and no API keys.

    Use cautiously if you are Copilot user paying per request.
"""


class CopilotInstance:
    def __init__(self, language = "Python", model: str = "gpt-5-mini", output: bool = False):
        self.AGENT_PROMPT = f"Please solve the following programming challenge using a unique solution. Your response must contain ONLY {language} code with no explanations, no markdown formatting, and no text before or after the code."
        self.output = output
        self.model = model

    async def initalize(self):
        self.client = CopilotClient()
        await self.client.start()
        self.session = await self.client.create_session({
            "model": self.model,
            "on_permission_request": self._deny_all_permissions,
            "systemMessage": {
                "content": "You are a code generator. Each request is independent - you have no memory of previous conversations. Respond only with code."
            }
        })

    async def _deny_all_permissions(self, request: dict) -> dict:
        """Deny all permission requests - Copilot cannot access any files."""
        permission_type = request.get('type', 'unknown')
        print(f"Denied permission request: {permission_type}")
        return {"result": "denied"}

    async def test(self, prompt:str = "What is 2 + 2?"):
        response =  await self.session.send_and_wait({"prompt": prompt})
        print(response.data.content)

    async def generateCode(self, problem_text: str, output_path: str):
        """
        Generate code from raw problem text.
        
        Args:
            problem_text: The problem description as raw text.
            output_path: Where to save the generated code.
        """
        await self._recycleSession()

        # Add a unique identifier to bust any caching
        cache_buster = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Send prompt with problem text directly (no attachments)
        response = await self.session.send_and_wait({
            "prompt": f"[Request ID: {cache_buster}]\n\n{self.AGENT_PROMPT}\n\n{problem_text}"
        })

        if self.output:
            print("Writing response to file...")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            # Extract code from markdown code blocks if present
            code = self._extract_code(response.data.content)
            f.write(code)
        print(f"Response written to {output_path}")

        return response

    def _extract_code(self, content: str) -> str:
        """Extract code from markdown code blocks, handling various formats."""
        # Try to find code between ```python and ``` or just ``` and ```
        pattern = r'```(?:python)?\s*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            # Return the first (or largest) code block
            return max(matches, key=len).strip()
        
        # If no code blocks found, return content as-is (stripped)
        return content.strip()

    async def bulkGenerateCode(self, problem_text: str, output_dir: str, count: int = 0):
        """
        Generate multiple code solutions from the same problem text.
        
        Args:
            problem_text: The problem description as raw text.
            output_dir: Directory to save all generated code files.
            count: Number of solutions to generate.
        """
        i = 0
        while i < count:
            start_time = time.time()

            await self.generateCode(problem_text, os.path.join(output_dir, f"output-{i}.py"))
            i += 1

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Iteration {i} took {elapsed_time:.2f} seconds")

    async def _recycleSession(self):
        """Fully destroy the current session and create a fresh one with no history."""
        try:
            await self.session.abort()
        except Exception:
            pass
        
        try:
            await self.session.destroy()
        except Exception:
            pass
        
        # Delete the old session reference
        del self.session
        
        # Create a completely fresh session with no conversation history
        self.session = await self.client.create_session({
            "model": self.model,
            "on_permission_request": self._deny_all_permissions,
            "systemMessage": {
                "content": "You are a code generator. Each request is independent - you have no memory of previous conversations. Respond only with code."
            }
        })

    async def close(self):
        await self.client.stop()
