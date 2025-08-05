from transformers import pipeline

class HuggingFaceHandler:
    def __init__(self, model_name="gpt-2"):
        self.model_name = model_name
        self.generator = pipeline("text-generation", model=self.model_name)

    def generate_text(self, prompt, max_length=150):
        response = self.generator(prompt, max_length=max_length, num_return_sequences=1)
        return response[0]['generated_text']

    def generate_exercise_list(self, subject, num_exercises=5):
        prompt = f"Create a list of {num_exercises} exercises for the subject: {subject}."
        return self.generate_text(prompt)

    def generate_powerpoint_slides(self, topic, num_slides=5):
        prompt = f"Create an outline for {num_slides} PowerPoint slides on the topic: {topic}."
        return self.generate_text(prompt)

    def generate_summary(self, text):
        prompt = f"Summarize the following text: {text}"
        return self.generate_text(prompt)