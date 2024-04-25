import click
# Function to load JSON data from a file
PROMPTS = {
    'email_contractor': {
        'input_variables': [
            'contractor_name',
            'project_details',
            'discount_justification'
        ]
    },
    'linkedin_from_tweet': {
        'input_variables': ['tweet']
    },
    'markdown_resume_builder': {
        'input_variables': ['sample_resume', 'candidate_information']
    },
    'job_fit': {
        'input_variables': ['job_post', 'candidate_description']
    },
    'code_analysis': {
        'input_variables': ['job_post', 'candidate_description']
    }
}

# Function to prompt for input based on the keys in the JSON file
def prompt_for_input(input_variables):
    responses = {}
    for variable in input_variables:
        responses[variable] = click.prompt(f"Please enter your {variable}")
    return responses

# Main CLI function
@click.command()
@click.argument('prompt_filename')
def main(prompt_filename):
    # Retrieve the input variables from the PROMPTS dictionary
    prompt_data = PROMPTS.get(prompt_filename)

    # Extract the input variables from the JSON data
    task = click.prompt("Please enter your task")
    input_variables = click.prompt("Please enter your input variables (comma-separated)", value_proc=lambda x: x.split(','))
    output_variables = click.prompt("Please enter your output variables (comma-separated)", value_proc=lambda x: x.split(','))

    # Prompt the user for input and store the responses
    responses = prompt_for_input(input_variables)

    # Output the responses
    click.echo("\nYou have entered the following information:")
    click.echo(f"Task: {task}")
    click.echo(f"Input Variables: {', '.join(input_variables)}")
    click.echo(f"Output Variables: {', '.join(output_variables)}")
    for key, value in responses.items():
        click.echo(f"{key}: {value}")

# Entry point for the script
if __name__ == "__main__":
    main()
