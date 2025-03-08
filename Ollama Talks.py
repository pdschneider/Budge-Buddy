# Import the csv module to handle reading and writing CSV files
import csv
# Import the os module for file system operations (e.g., creating directories, checking file existence)
import os
# Import the requests module to make HTTP requests to the Ollama API
import requests
# Import the string module to access string.punctuation for cleaning input
import string

# Define the path to the budget CSV file (specific to your system)
budget_file = "/media/phillip/Storage Drive/Personal/Code Projects/Python Files/LLM Budgeting Tool/budget.csv"

# Function to create the budget file with default entries if it doesn't exist
def create_budget_file():
    # Create the directory for the budget file if it doesn’t already exist
    os.makedirs(os.path.dirname(budget_file), exist_ok=True)
    # Check if the budget file doesn’t exist
    if not os.path.exists(budget_file):
        # Open the file in write mode, ensuring no extra newline characters
        with open(budget_file, 'w', newline='') as file:
            # Create a CSV writer object to write rows to the file
            writer = csv.writer(file)
            # Write the header row with column names "Category" and "Amount"
            writer.writerow(["Category", "Amount"])
            # Write a default entry for Groceries with an amount of 500
            writer.writerow(["Groceries", "500"])
            # Write a default entry for Restaurants with an amount of 100
            writer.writerow(["Restaurants", "100"])
            # Write a default entry for Mortgage with an amount of 1250
            writer.writerow(["Mortgage", "1250"])
            # Write a default entry for Internet with an amount of 100
            writer.writerow(["Internet", "100"])

# Function to read the budget from the CSV file into a dictionary
def read_budget():
    # Initialize an empty dictionary to store budget categories and amounts
    budget = {}
    # Check if the budget file exists before trying to read it
    if os.path.exists(budget_file):
        # Open the file in read mode
        with open(budget_file, 'r') as file:
            # Create a CSV reader object to read rows from the file
            reader = csv.reader(file)
            # Skip the header row ("Category", "Amount") to get to the data
            next(reader)
            # Loop through each remaining row in the CSV file
            for row in reader:
                # Clean the amount string by removing quotes and whitespace
                amount_str = row[1].strip(' "\t\n\r')
                # Convert the cleaned amount string to a float and store it in the dictionary with the category as the key
                budget[row[0]] = float(amount_str)
    # Return the budget dictionary (empty if the file doesn’t exist)
    return budget

# Function to update the budget by changing or adjusting an amount
def update_budget(category, amount_change=None, new_amount=None):
    # Load the current budget from the file into a dictionary
    budget = read_budget()
    # Capitalize the category name (e.g., "groceries" becomes "Groceries")
    category = category.title()
    # Check if a new amount is provided (used for "change" or "set" commands)
    if new_amount is not None:
        # Ensure new_amount is a number (integer or float)
        if not isinstance(new_amount, (int, float)):
            # Return an error message if new_amount isn’t a number
            return f"Error: new_amount must be a number, got {type(new_amount)}"
        # Prevent setting a negative amount
        if new_amount < 0:
            # Return a warning if the new amount is negative
            return f"Warning! Can’t set {category} to a negative amount!"
        # Update the budget dictionary with the new amount for the category
        budget[category] = float(new_amount)
    # Check if an amount change is provided (used for "add" or "subtract" commands)
    elif amount_change is not None:
        # Ensure amount_change is a number (integer or float)
        if not isinstance(amount_change, (int, float)):
            # Return an error message if amount_change isn’t a number
            return f"Error: amount_change must be a number, got {type(amount_change)}"
        # Check if the category already exists in the budget
        if category in budget:
            # Calculate the new amount by adding the change to the existing amount
            updated_amount = budget[category] + amount_change
            # Prevent the amount from going negative
            if updated_amount < 0:
                # Return a warning if the adjustment would result in a negative amount
                return f"Warning! Can’t adjust {category}—it’d go negative!"
            # Update the budget dictionary with the new amount
            budget[category] = float(updated_amount)
        else:
            # Prevent subtracting from a category that doesn’t exist
            if amount_change < 0:
                # Return a warning if trying to subtract from a non-existent category
                return f"Warning! Can’t subtract from {category}—it doesn’t exist yet!"
            # Add the new category with the amount_change as its starting amount
            budget[category] = float(amount_change)
    else:
        # Return an error if neither new_amount nor amount_change is provided
        return "Error: No amount specified!"
    # Open the budget file in write mode to save the updated budget
    with open(budget_file, 'w', newline='') as file:
        # Create a CSV writer object to write rows to the file
        writer = csv.writer(file)
        # Write the header row with column names "Category" and "Amount"
        writer.writerow(["Category", "Amount"])
        # Loop through each category and amount in the budget dictionary
        for cat, amt in budget.items():
            # Write the category and its amount as a row in the CSV file
            writer.writerow([cat, str(amt)])
    # Return a success message showing the updated amount for the category
    return f"Updated {category} to {budget[category]}"

# Function to clean an amount string by removing non-numeric characters
def clean_amount(amount_str):
    # Create a list of characters that are digits or a decimal point from the input string
    digits_and_decimal = [c for c in amount_str if c.isdigit() or c == '.']
    # Initialize an empty string to build the cleaned amount
    cleaned = ''
    # Track whether a decimal point has been added to avoid multiple decimals
    has_decimal = False
    # Loop through each character in the filtered list
    for c in digits_and_decimal:
        # Add the decimal point only if it’s the first one encountered
        if c == '.' and not has_decimal:
            # Append the decimal point to the cleaned string
            cleaned += c
            # Mark that a decimal has been added
            has_decimal = True
        # Add digits to the cleaned string
        elif c.isdigit():
            # Append the digit to the cleaned string
            cleaned += c
    # Check if the cleaned string is empty (no valid number found)
    if not cleaned:
        # Raise an error if no valid number was extracted
        raise ValueError("No valid number found")
    # Return the cleaned string with ".0" appended if no decimal is present, otherwise return as is
    return cleaned if '.' in cleaned else cleaned + '.0'

# Function to parse the user’s command and determine the action to take
def parse_command(command):
    # Convert the command to lowercase and remove leading/trailing spaces
    command = command.lower().strip()
    # Split the command into individual words
    parts = command.split()
    # Check if the command includes "add" and "to" (e.g., "add $50 to groceries")
    if "add" in parts and "to" in parts:
        try:
            # Find the index of "add" in the command
            add_index = parts.index("add")
            # Find the index of "to" in the command
            to_index = parts.index("to")
            # Extract the raw amount string (e.g., "$50") after "add"
            amount_str_raw = parts[add_index + 1]
            # Clean the raw amount string to get a valid number
            amount_str = clean_amount(amount_str_raw)
            # Convert the cleaned amount string to a float
            amount = float(amount_str)
            # Extract the category words after "to"
            category_parts = parts[to_index + 1:]
            # Join the category words, remove trailing punctuation, and capitalize
            category = ' '.join(category_parts).rstrip(string.punctuation).title()
            # Call update_budget to add the amount to the category
            return update_budget(category, amount_change=amount)
        except ValueError as e:
            # Return an error if the amount couldn’t be parsed
            return f"Invalid amount: {str(e)}. Please use a number like '$50' or '50'."
        except IndexError:
            # Return an error if the command format is incorrect
            return "Invalid add command format. Try 'Add $50 to groceries'."
    # Check if the command includes "subtract" or "remove" and "from" (e.g., "subtract $20 from restaurants")
    elif ("subtract" in parts or "remove" in parts) and "from" in parts:
        # Determine which verb is used ("subtract" or "remove")
        verb = "subtract" if "subtract" in parts else "remove"
        try:
            # Find the index of the verb in the command
            verb_index = parts.index(verb)
            # Find the index of "from" in the command
            from_index = parts.index("from")
            # Extract the raw amount string after the verb
            amount_str_raw = parts[verb_index + 1]
            # Clean the raw amount string to get a valid number
            amount_str = clean_amount(amount_str_raw)
            # Convert the cleaned amount string to a float
            amount = float(amount_str)
            # Extract the category words after "from"
            category_parts = parts[from_index + 1:]
            # Join the category words, remove trailing punctuation, and capitalize
            category = ' '.join(category_parts).rstrip(string.punctuation).title()
            # Call update_budget to subtract the amount from the category (negative amount_change)
            return update_budget(category, amount_change=-amount)
        except ValueError as e:
            # Return an error if the amount couldn’t be parsed
            return f"Invalid amount: {str(e)}. Please use a number like '$20' or '20'."
        except IndexError:
            # Return an error if the command format is incorrect
            return "Invalid subtract command format. Try 'Subtract $20 from restaurants'."
    # Check if the command includes "change" or "set" and "to" (e.g., "change groceries to $300")
    elif ("change" in parts or "set" in parts) and "to" in parts:
        # Determine which verb is used ("change" or "set")
        verb = "change" if "change" in parts else "set"
        try:
            # Find the index of the verb in the command
            verb_index = parts.index(verb)
            # Find the index of "to" in the command
            to_index = parts.index("to")
            # Extract the category words between the verb and "to"
            category_parts = parts[verb_index + 1:to_index]
            # Join the category words and capitalize them
            category = ' '.join(category_parts).title()
            # Extract the raw amount string after "to"
            amount_str_raw = parts[to_index + 1]
            # Clean the raw amount string to get a valid number
            amount_str = clean_amount(amount_str_raw)
            # Convert the cleaned amount string to a float
            amount = float(amount_str)
            # Call update_budget to set the category to the new amount
            return update_budget(category, new_amount=amount)
        except ValueError as e:
            # Return an error if the amount couldn’t be parsed
            return f"Invalid amount: {str(e)}. Please use a number like '$300' or '300'."
        except IndexError:
            # Return an error if the command format is incorrect
            return "Invalid change command format. Try 'Change groceries to $300'."
    # Check if the command includes "show" or "read" (e.g., "show budget")
    elif "show" in parts or "read" in parts:
        # Return the current budget dictionary as a string
        return str(read_budget())
    # Return an error if the command doesn’t match any known pattern
    return "Unknown command. Try 'Add $50 to groceries', 'Subtract $20 from restaurants', 'Change mortgage to $1300', or 'Show budget'."

# Function to query the Ollama API for a friendly response
def query_ollama(prompt):
    # Define the URL for the Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    # Create a payload dictionary with the model name, prompt, and stream setting
    payload = {
        "model": "llama3.2",
        "prompt": f"Provide a friendly, conversational response to this budget-related request: {prompt}",
        "stream": False
    }
    try:
        # Send a POST request to the Ollama API with the payload
        response = requests.post(url, json=payload)
        # Check if the response status code is 200 (success)
        if response.status_code == 200:
            # Extract and return the response text from the JSON data
            return response.json()["response"]
        # Return an error message if the API responded but not successfully
        return "Oh no! Ollama didn’t reply—check if it’s running!"
    except requests.ConnectionError:
        # Return an error message if the connection to the API failed
        return "Can’t reach Ollama—is Docker up?"

# Main function to run the program
def main():
    # Call the function to create the budget file if it doesn’t exist
    create_budget_file()
    # Print a welcome message to the user
    print("Budget Buddy ready! Talk to me here.")
    # Start an infinite loop to keep the program running
    while True:
        # Prompt the user for input and store their command
        user_input = input("Tell me what to do: ")
        # Parse the user’s command and get the result
        command_result = parse_command(user_input)
        # Query the Ollama API for a friendly response to the user’s input
        ollama_response = query_ollama(user_input)
        # Print the result of the parsed command
        print(f"Result: {command_result}")
        # Print the friendly response from Ollama
        print(f"Budget Buddy says: {ollama_response}")

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Call the main function to start the program
    main()