from anthropic import Anthropic
import os
import base64
from dotenv import load_dotenv
import time

load_dotenv()   

model = "claude-sonnet-4-6"

class ClaudeService:

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.messages = []

    def add_user_message(self, text):
        user_message = { 'role': 'user', 'content': text}
        self.messages.append(user_message)    

    def add_assistant_message(self, content):
        assistant_message = { 'role': 'assistant', 'content': content}
        self.messages.append(assistant_message)

    def chat(self, system=None):
        print("CHAT CALLED")
        params = {
            'model':model,
            'max_tokens':1000,
            'messages': self.messages,
        }

        if system:
            params['system'] = system

        full_text = ""
        for attempt in range(3):
            try:
                with self.client.messages.stream(**params) as stream:
                    for text in stream.text_stream:
                        full_text += text
                        yield text  # stream ka UI

                    final_message = stream.get_final_message()
                    print(f"FINAL {final_message.content[0].text}")

                self.add_assistant_message(full_text)
                break

            except Exception as e:
                yield f"ERROR: {str(e)}"
                print(f"ERROR: {str(e)}")
                

        
    def analyze_bread(self, image, notes):
        print("ANALYZE CALLED")
        try:
            image_bytes = base64.standard_b64encode(image.read()).decode('utf-8')

            content = [{
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
            self.add_user_message(content)
            return self.chat()    
        except Exception as e:
            return f"Error: {str(e)}"

    def chat_about_bread(self, message):
        self.add_user_message(message)
        return self.chat()    



        

    
