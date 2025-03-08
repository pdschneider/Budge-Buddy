# Budget Buddy

by Phillip Schneider

Budget Buddy is a tool that combines the features of Siri or Alexa with a locally run LLM. At its core, the script runs a local LLM (in this case Llama 3.2) via a program called Ollama within terminal. It also creates a new CSV type budget file with default entries and uses preset commands (example: "Add $50 to Groceries." or "Change Restaurants to $200") to actually write to the file itself.

The objective is to create the seed of a larger software vision that could be thought of as a true virtual assistant, like Siri + ChatGPT. It would be all totally local and private with the ability to modify your schedule, set reminders, change your budget, etc., as well as give you advice in a way that updates to new input retained as memories. So you could talk to the LLM about your plans for the month and it would give you a template budget (example: "Hey LLM, this month I'm traveling to Dubai so I need to budget for that. Can you give me an estimate on how much that would cost? Hint: a lot).

Here's the breakdown:

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

It uses several if/else statements, variables, and read/write abilities within a small handful of functions to do all this.
The major limitation of the tool is that the LLM itself can't actually "see" the files or write to them on its own. It runs two totally separate processes simultaneously through the script: the read/write to files (Siri lite) and the chat bot's response (ChatGPT lite). The chat bot does not store memories outside each chat session and it cannot give real time information or advise based on your CSV file's contents. Integrating those two would be a leap, but it is possible to use an interface called OpenWebUI to run the LLM through custom Python scripts. Theoretically, you could add the code I wrote to that interface and be able to run the same kind of thing outside of terminal. If you could store that file in a place accessible to the LLM in real time, it would start to function more as intended. I'm going to keep messing with this outside of the class, but I wanted to submit what I have now.

There were lots of new things I had to learn to create this, like how to get the actual LLM to be pulled by a Python script in VSCode, and it took me several days of nonstop trial and error. Even just getting docker engine to work probably ran me 5+ hours over a couple of days.

As far as errors go, at first I tried "tricking" the LLM to write to the file for me, but the LLM was so chatty that I couldn't pin down any exact input that would work. So, I had to pivot to making it do two separate things at once: the LLM's dialogue and the file writing. Then, I kept getting errors because the amounts kept turning into strings, so I had to force the script to change them into floats. Then, I was having problems with characters like the $ and . in the sentence, so I had to make the script strip those before parcing out the commands. 

I ended up dealing with code I had no idea I would end up with when I came up with the idea, but it was pretty ambitious from the start. It uses dictionaries rather than lists so that it can link together categories & amounts more easily, nested if statements for error correction, the csv module so that it can read and write to csv files, the requests module so that it can interact with the LLM, the os module to give it access to the file directory, and the string module so it can parce out and clean up what you write in a way that it understands to convert your input to a functioning read/write. It also creates a payload dictionary for the LLM which tell it which model to use and gives it a prompt to give friendly responses to budget questions.  If it doesn't return the correct status code, it throws an error and asks if Ollama is running via the "try: except" error handling method. It also uses for loops to scan through the CSV file's contents as well as to scan for special characters that it needs to scrub from user input as well as one while loop that keeps the program running (the first case I've seen of an infinite loop that is actually required for something). Almost all of this was new to me, so I learned quite a bit. Also, f strings make things WAY easier.
