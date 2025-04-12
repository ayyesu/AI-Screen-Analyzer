import json
import requests

class GeminiAPI:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def query_gemini(self, text, is_code_related=False):
        try:
            api_key = self.config_manager.get('API', 'gemini_api_key')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

            # Choose a prompt based on whether this is code-related
            if is_code_related:
                prompt = (
                    "I'm going to share text from a screenshot that contains a coding question or code-related problem. "
                    "Please analyze it and provide a helpful, detailed response that includes:\n"
                    "1. A clear explanation of the problem or question\n"
                    "2. A complete solution with working code examples\n"
                    "3. An explanation of how the code works\n"
                    "4. If there are errors in the original code, identify and fix them\n\n"
                    f"Screenshot text:\n{text}"
                )
            else:
                prompt = f"Please analyze the following text extracted from a screenshot and provide a helpful response:\n\n{text}"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    # Extract the text from the response
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return "No response content found in the API result."
            else:
                error_msg = f"API Error: {response.status_code}"
                try:
                    error_details = response.json()
                    if "error" in error_details:
                        error_msg += f" - {error_details['error']['message']}"
                except:
                    error_msg += f" - {response.text}"
                return error_msg

        except Exception as e:
            return f"Error connecting to Gemini API: {str(e)}"
