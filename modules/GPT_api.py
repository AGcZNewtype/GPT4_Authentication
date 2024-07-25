from openai import OpenAI
import os

# Function to generate a response from GPT based on the given PDF text
def GPT_generation(pdf_text):
    # Set the API key
    c_key = 'sk-proj-q4BSmJAdKjBDAhm6xtBST3BlbkFJxey686dvUm4P0MMb8l91'

    # Connect to the OpenAI API
    client = OpenAI(api_key=c_key)

    # Load the instruction text from a file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    instruction_path = os.path.join(base_dir, '../instruction.txt')
    with open(instruction_path, 'r') as instruction_file:
        instructions = instruction_file.read()

    # Create a session with the API
    client = OpenAI(api_key=c_key)

    # Complete the session with the given text and instructions
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": pdf_text}
        ]
    )

    # Return the generated result
    return response.choices[0].message.content


