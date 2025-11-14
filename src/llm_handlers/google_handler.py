from google import genai

class GoogleHandler:
    def __init__(self,model_name):
        self.client = genai.Client()
        self.model_name = model_name

    def generate_document(self, prompt):
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        return response['text'] if 'text' in response else None

    def generate_exercise_list(self, subject, specifications):
        prompt = f"Create an exercise list for {subject} with the following specifications: {specifications}"
        return self.generate_document(prompt)

    def generate_powerpoint_slides(self, content):
        prompt = f"Create PowerPoint slides based on the following content: {content}"
        return self.generate_document(prompt)

    def generate_summary(self, text):
        prompt = f"Summarize the following text: {text}"
        return self.generate_document(prompt)