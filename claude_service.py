from anthropic import Anthropic
import os
import base64
from dotenv import load_dotenv

load_dotenv()   

model = "claude-sonnet-4-0"

class ClaudeService:

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.messages = []

    def analyze_bread(self, image, notes):
        image_bytes = base64.standard_b64encode(image.read()).decode('utf-8')

        self.messages.append(
            {

                "role": "user",
                "content":[{
                    "type":"image",
                    "source":{
                        "type":"base64",
                        "media_type":"image/jpeg",
                        "data":image_bytes
                    }
                },
                {
                    "type":"text",
                    "text":notes
                }
                ]

            }
            
        )

        message = self.client.messages.create(
            model=model,
            messages=self.messages,
            max_tokens=2000
        )

        return message.content[0].text


    
