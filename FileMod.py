import re
import json
import os

__all__ = ["FileMod"]

class FileMod:
    def __init__(self, agent):
        self.agent = agent
        self.description = "Regex-Powered AI-Driven Universal File Transformer (UFT) for Creating, Editing, and Transforming Files of Any Type."
        self.schema = {
            "functions": {
                "filemod": {
                    "arguments": {
                        "file_path": "str",
                        "regex_target": "str",
                        "replacement": "str",
                    },
                    "description": "Universal File Transformer (UFT) Tool - Creates, Edits, and Transforms files through AI-Targeted Regex"
                }
            }
        }

    async def execute(self, args):
        new_file = False
        file_path = args["file_path"]
        regex_target = args["regex_target"]
        replacement = args["replacement"]

        # Create the file and directories if they don't exist
        dir_name = os.path.dirname(file_path)
        if dir_name:  # Check if dir_name is not empty
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('')  # Create an empty file
            #await self.agent.tool_response(f"File '{file_path}' not found. Created the file and its directories.")

        try:
            with open(file_path, 'r') as f:
                file_content = f.read()

            compiled_regex = re.compile(regex_target)
            new_content, num_replacements = compiled_regex.subn(replacement, file_content)

            if num_replacements == 0:
                await self.agent.tool_response(f"Warning: Regex '{regex_target}' did not match in file '{file_path}'. No replacements were made.")
            else:
                with open(file_path, 'w') as f:
                    f.write(new_content)
                await self.agent.tool_response(f"File mod completed successfully on '{file_path}'. {num_replacements} replacement(s) were made.")

        except Exception as e:
            await self.agent.tool_response(f"Error during reverse search and replace: {str(e)}")
