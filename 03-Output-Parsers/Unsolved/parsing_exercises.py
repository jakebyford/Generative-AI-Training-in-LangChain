# Create environment
# python -m venv venv

# Activate environment
# Windows:  source venv\Scripts\activate
# Mac:  source venv/bin/activate

# Install dependencies
# pip install langchain langchain_core pydantic langchain_openai

# SET OPENAI_API_KEY
# export OPENAI_API_KEY="sk-proj---------------------------------------------"

# VIEW TO SEE IF API KEY IS ALREADY IN ENVIRONMENT
# echo $OPENAI_API_KEY




"""
Exercise 1: Movie Review Parser
Parse a movie review into structured data using LangChain's Pydantic parser.
The goal is to extract title, rating, and main points from a review.
"""

from langchain.output_parsers import (
    PydanticOutputParser, 
    CommaSeparatedListOutputParser, 
    StructuredOutputParser, 
    ResponseSchema, 
    DatetimeOutputParser
)
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# TODO: Create a MovieReview Pydantic model with:
# - title (str): The movie title
# - rating (float): Rating out of 10
# - main_points (list[str]): Key points from the review
# ADD CODE HERE


# TODO: Create a PydanticOutputParser using your MovieReview model
# ADD CODE HERE

# Create the prompt template
prompt = PromptTemplate(
    template="Extract structured information from this movie review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": "ADD CODE HERE"}  # Add parser instructions
)

# Example usage
review_text = """
I just watched "The Matrix" and it blew my mind! This sci-fi masterpiece 
deserves a solid 9.5/10. The special effects were groundbreaking, 
the philosophical themes were deep, and the action sequences were incredible. 
However, some scenes in the latter half felt a bit drawn out.
"""

print("\n","#"*50, "Exercise 1", "#"*50)

# TODO: Set up the LLM and create the chain
# ADD CODE HERE

# TODO: Run the chain and parse the output
# ADD CODE HERE











# exercise2.py
"""
Exercise 2: Recipe Steps Parser
Parse cooking recipe steps into a list using LangChain's CommaSeparatedListOutputParser.
The goal is to extract clear, separated steps from a recipe description.
"""

# TODO: Create a CommaSeparatedListOutputParser
# ADD CODE HERE

# Create the prompt template
prompt = PromptTemplate(
    template="Convert this recipe description into clear, separated steps:\n{recipe}\n{format_instructions}",
    input_variables=["recipe"],
    partial_variables={"format_instructions": "ADD CODE HERE"}  # Add parser instructions
)

# Example usage
recipe_text = """
To make a basic omelette, crack three eggs into a bowl and whisk them well. 
Heat butter in a non-stick pan over medium heat. Pour the eggs into the pan, 
let them set slightly, add your fillings to one half, then fold the other 
half over. Cook until golden brown on the bottom.
"""

print("\n","#"*50, "Exercise 2", "#"*50)

# TODO: Set up the LLM and create the chain
# ADD CODE HERE

# TODO: Run the chain and parse the output
# ADD CODE HERE













"""
Exercise 3: Product Review Sentiment Parser
Parse product reviews to extract sentiment scores using LangChain's StructuredOutputParser.
The goal is to analyze sentiment across different aspects of a product review.
"""

# TODO: Create ResponseSchema objects for:
# - overall_rating (1-5 scale)
# - pros (text description of positive aspects)
# - cons (text description of negative aspects)
# - sentiment_score (float between -1 and 1)
# ADD CODE HERE

# TODO: Create a StructuredOutputParser using your response schemas
# ADD CODE HERE

# Create the prompt template
prompt = PromptTemplate(
    template="Analyze the sentiment of this product review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": "ADD CODE HERE"}  # Add parser instructions
)

# Example usage
review_text = """
I've been using this wireless keyboard for about a month now. The battery life is excellent - 
I've only had to charge it once. The keys have a nice tactile feel and it pairs easily with 
multiple devices. However, it's a bit heavier than I expected and the lack of backlighting 
makes it difficult to use in low light conditions. Overall, it's a good keyboard but has room 
for improvement.
"""

print("\n","#"*50, "Exercise 3", "#"*50)

# TODO: Set up the LLM and create the chain
# ADD CODE HERE

# TODO: Run the chain and parse the output
# ADD CODE HERE














"""
Exercise 4: Meeting Notes Parser using JsonOutputParser
Parse meeting notes into a structured JSON format using LangChain's JsonOutputParser.
The goal is to extract meeting details, action items, and decisions from unstructured notes.
"""


# TODO: Create a MeetingNotes Pydantic model with:
# - title (str): Meeting title
# - date (str): Meeting date
# - participants (list[str]): List of meeting attendees
# - action_items (list[dict]): List of action items with 'task', 'assignee', and 'deadline' fields
# - decisions (list[str]): List of decisions made
# ADD CODE HERE

# TODO: Create a JsonOutputParser using your MeetingNotes model
# ADD CODE HERE

# Create the prompt template
prompt = PromptTemplate(
    template="Extract structured meeting information from these notes:\n{notes}\n{format_instructions}",
    input_variables=["notes"],
    partial_variables={"format_instructions": "ADD CODE HERE"}  # Add parser instructions
)

# Example usage
notes_text = """
Project Falcon Weekly Sync - March 15, 2025

Attendees: Sarah Johnson, Mike Chen, Priya Patel, Alex Rodriguez

Discussion Points:
- Reviewed sprint progress, currently at 70% completion
- Database migration issues causing delays in the authentication module
- New design mockups received from UX team for mobile app

Action Items:
1. Mike to troubleshoot database migration issues by Wednesday
2. Priya to schedule a review meeting with UX team by Friday
3. Alex to update project documentation with new API endpoints by next Monday

Decisions:
- Approved one-week extension for Phase 2 deliverables
- Selected AWS Lambda for serverless implementation
- Postponed the analytics dashboard to Phase 3
"""

print("\n","#"*50, "Exercise 4", "#"*50)

# TODO: Set up the LLM and create the chain
# ADD CODE HERE

# TODO: Run the chain and parse the output
# ADD CODE HERE















"""
Exercise 5: Date Extraction Parser
Parse text to extract and normalize date references using LangChain's DatetimeOutputParser.
The goal is to convert various date formats and references into standardized datetime objects.
"""


# TODO: Create a DatetimeOutputParser
# ADD CODE HERE

# Create the prompt template
prompt = PromptTemplate(
    template="Extract the time mentioned in this text:\n{text}\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": "ADD CODE HERE"}  # Add parser instructions
)

# Example usage
sample_texts = [
    "Let's schedule our meeting for next Tuesday at 2pm.",
    "The product launch is set for June 15, 2025.",
    "The report is due on Vikas' desk at 8am Monday morning."
]

print("\n","#"*50, "Exercise 5", "#"*50)

# TODO: Set up the LLM and create the chain
# ADD CODE HERE

# TODO: Run the chain for each sample text
# ADD CODE HERE