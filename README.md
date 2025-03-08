# Budge-Buddy
This tool connects to a local LLM and reads/writes to a budget file.

This project is a tool that combines the features of Siri or Alexa with a locally run LLM. At its core, the script runs a local LLM (in this case Llama 3.2) via a program called Ollama within terminal. It also creates a new CSV type budget file with default entries and uses preset commands (example: "Add $50 to Groceries." or "Change Restaurants to $200") to actually write to the file itself.
The objective is to create the seed of a larger software vision that could be thought of as a true virtual assistant, like Siri + ChatGPT. It would be all totally local and private with the ability to modify your schedule, set reminders, change your budget, etc., as well as give you advice in a way that updates to new input retained as memories. So you could talk to the LLM about your plans for the month and it would give you a template budget (example: "Hey LLM, this month I'm traveling to Dubai so I need to budget for that. Can you give me an estimate on how much that would cost? Hint: a lot).
The actual code is written already (sorry, I wanted to make sure it worked before submitting the idea!) and what it does is just a start of what it could theoretically do, but here's the breakdown:

1. Imports the necessary modules (csv, os, requests, and string).
2. Creates a CSV type budget file if not already in the folder path with default categories and amounts.
3. Reads the budget file as a dictionary.
4. Writes to the budget file after parsing out a command it recognizes. It separates words in the sentence and checks for an integer or float for the amount and checks to see what the command is (add, subtract, change, or show) while giving errors if the amount goes below zero or is not a number. You have to be pretty specific with your wording.
5. Cleans up the data so that it is able to be written to the file (removes special characters and converts number amounts from strings into integers or floats).
6. Pulls the model (in this case llama 3.2 because it's small enough to run on somewhat older CPU's like mine, but you could very easily download any model you want with a couple clicks from the ollama website and run anything your PC can handle, just change the LLM's name in the script) and submits your input as a chat message, prompting a response. It uses ollama + docker engine (software that creates virtual containers) on the back end to function.


End result:

Output:
Budget Buddy ready! Talk to me here.
Tell me what to do: 

Input:
Add $100 to groceries.

Output:
Result: Updated Groceries to 600.0
Budget Buddy says: "Hey, just wanted to touch base with you about the grocery budget. I understand we've been looking at our expenses and making some adjustments. Would it be possible to add another $100 to that category? That way, we can still keep an eye on things but also make sure we're covering all our bases when it comes to food."


The major limitation of the tool is that the LLM itself can't actually "see" the files or write to them on its own. It runs two totally separate processes simultaneously through the script: the read/write to files (Siri lite) and the chat bot's response (ChatGPT lite). The chat bot does not store memories outside each chat session and it cannot give real time information or advise based on your CSV file's contents. Integrating those two would be a leap, but it is possible to use an interface called OpenWebUI run custom Python scripts. Theoretically, you could add the code I wrote to that interface and be able to run the same kind of thing outside of terminal. If you could store that file in a place accessible to the LLM in real time, it would start to function more as intended.
