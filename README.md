# Virtual_Assistant-for-Windows-based-PCs
This is a Virtual Assistant designed for windows based Computers.
Designed to replace Microsoft's retired Cortana.
# Currently supported features (More to come soon)
• Get the latest news headlines
• Remind you of birthdays and meetings.
• Get random jokes and advice
• Play videos, TV shows, or movies on YouTube 
• Send WhatsApp messages and Emails
• Open Desktop applications
• Get trending movies
• Search on Google
• Get the Weather report
• Retrieve IP Address
• Providing information or facts from Wikipedia. 
• Searching a flight
• Switching between windows
• Taking Screenshot
• Word dictionary
• Computations on WolframAlpha API
# How the assistant Works
The following steps give a brief overview on how the assistant works:

The program continously listens for a user to say the wake word (currently set to "Assistant").
When a wake word is detected, the program uses speech recognition to determine what the user says.
The IntentClassifier class classifies the user's intent using the Support Vector Machine (SVM) algorithm that trains on a dataset containing sample user prompts along with their intent.
Based on the classified intent, the assistant executes the correct function.


