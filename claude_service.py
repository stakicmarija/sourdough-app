from anthropic import Anthropic
import os
import base64
from dotenv import load_dotenv
import time

load_dotenv()

model = "claude-sonnet-4-6"

system_prompt = """
You are a professional sourdough baker and mentor.

Analyze photos of sourdough bread and give honest, constructive feedback to help the user improve.

Focus on:
- crumb structure
- crust quality
- oven spring and shape
- fermentation (under/over proofing)

Respond in this structure:
1. Overall impression
2. What is good
3. What can be improved
4. Specific actionable tips
5. Optional score (1–10)

Be supportive but direct. Avoid generic advice.
Do not assume the image is not the user’s bread.
"""

class ClaudeService:

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def chat(self, messages, system=None):
        params = {
            "model": model,
            "max_tokens": 1000,
            "messages": messages,
        }

        if system:
            params["system"] = system

        # retry
        for attempt in range(3):
            full_text = ""

            try:
                with self.client.messages.stream(**params) as stream:
                    for text in stream.text_stream:
                        full_text += text
                        yield text

                return  # success, stop retry

            except Exception as e:
                error_str = str(e).lower()
                yield f"\n Error: {str(e)}"
                return

    def analyze_bread(self, image, notes):
        image_bytes = base64.standard_b64encode(image.read()).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image.type, 
                            "data": image_bytes,
                        },
                    },
                    {
                        "type": "text",
                        "text": notes,
                    },
                ],
            }
        ]

        return self.chat(messages, system_prompt)