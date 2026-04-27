import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class K8sAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        # Configure Gemini
        print("[*] Configuring Gemini API...")
        genai.configure(api_key=self.api_key)

        # Use a working model
        print(f"[*] Initializing model: gemini-flash-latest")
        self.model = genai.GenerativeModel("gemini-flash-latest")

        # Start chat session
        self.chat = self.model.start_chat(history=[])

        # System prompt
        self.system_prompt = """
        You are an expert Kubernetes administrator.
        When asked a question, respond ONLY with the exact kubectl command.
        Do not include markdown, backticks, or explanation.
        """

        # Initialize context
        print("[*] AI ready!")

    def generate_command(self, user_query: str) -> str:
        # If it's the first message, prepend the instructions
        if not self.chat.history:
            full_query = f"{self.system_prompt}\n\nUser Request: {user_query}"
        else:
            full_query = f"User Request: {user_query}"
            
        response = self.chat.send_message(full_query)
        return response.text.strip()

    def summarize_output(self, user_query: str, command: str, terminal_output: str) -> str:
        prompt = f"""
        User asked: {user_query}
        Command executed: {command}

        Output:
        {terminal_output}

        Provide a short summary.
        """
        response = self.chat.send_message(prompt)
        return response.text.strip()

    def execute_with_autofix(self, command: str, max_retries: int = 3):
        current_command = command

        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    current_command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                return current_command, result.stdout, True

            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() or e.stdout.strip()

                if attempt < max_retries - 1:
                    print(f"\nError: {error_msg}")
                    print("Asking AI for fix...")

                    fix_prompt = f"""
                    The command failed.

                    Command: {current_command}
                    Error: {error_msg}

                    Return ONLY corrected kubectl command.
                    """

                    response = self.chat.send_message(fix_prompt)
                    current_command = response.text.strip()
                    print(f"New command: {current_command}")

                else:
                    return current_command, error_msg, False

        return current_command, "Unknown error", False