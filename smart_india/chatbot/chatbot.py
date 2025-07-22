from transformers import pipeline

def get_career_advice(user_input):
    # For now, we'll use a simple text generation model.
    # In a real application, this would be a more sophisticated model
    # fine-tuned for career counseling.
    generator = pipeline('text-generation', model='distilgpt2')
    response = generator(user_input, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']
