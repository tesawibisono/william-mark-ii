import openai
# from openai import OpenAI
# import RPi.GPIO as GPIO
import gpiod
import subprocess


yellow_led = 22 #pinout led GPIO-22
green_led = 27 #pinout led GPIO-27
red_led = 17 #pinout led GPIO-27

# client = OpenAI()

with open('api_key.txt', 'r') as file:
    gpt_key = file.read().rstrip()


openai.api_key = gpt_key

# def get_gpt_response(prompt):
#     response = client.completions.create

def get_gpt_response(prompt):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens=300,
    )
    return response.choices[0].text.strip()

def execute_command(command):
    exec(command)

def create_and_run_python_file(filename, content):
    # Ensure the filename ends with .py
    if not filename.endswith('.py'):
        filename += '.py'
    
    # Write the content to the new Python file
    with open(filename, 'w') as file:
        file.write(content)
    
    print(f"{filename} has been created successfully.")
    
    # Run the newly created Python file
    result = subprocess.run(['python', filename], capture_output=True, text=True)
    
    # Print the output of the script
    print("Output from the new Python file:")
    print(result.stdout)
    
    # Print any errors
    if result.stderr:
        print("Errors:")
        print(result.stderr)

def main():
    while True:
        user_input = input("Tell me to do something: ")
        gpt_prompt = f"Generate Python code to control Raspberry Pi 5 using gpiod as the gpio library with gpiod.Chip('gpiochip4') and add other necessary library for this: {user_input}. ONLY GENERATE THE CODE. DON'T EXPLAIN WITHOUT ''#''"
        gpt_code = get_gpt_response(gpt_prompt)
        print(f"Generated code:\n{gpt_code}")
        
        # Clean up the GPT-generated code
        filtered_command = gpt_code.replace('```python', '').replace('```', '').strip()
        
        # Set the filename and content for the new Python file
        filename = "generated_script"
        content = f"{filtered_command}"
        
        # Create and run the new Python file
        create_and_run_python_file(filename, content)

if __name__ == '__main__':
    main()