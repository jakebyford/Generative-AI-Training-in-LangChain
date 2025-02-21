# solutions.py
"""
Solutions for the LangChain Output Parser exercises
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





# Solution for Exercise 1: Movie Review Parser
class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie")
    rating: float = Field(description="Rating out of 10")
    main_points: list[str] = Field(description="Key points from the review")

# Create the parser
parser = PydanticOutputParser(pydantic_object=MovieReview)

#### Tip for writing queries
#### Print format instructions to see how this parser needs to be formatted.
# print(parser.get_format_instructions())

# Create the prompt template
prompt = PromptTemplate(
    template="Extract structured information from this movie review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain
review_text = """
I just watched "The Matrix" and it blew my mind! This sci-fi masterpiece 
deserves a solid 9.5/10. The special effects were groundbreaking, 
the philosophical themes were deep, and the action sequences were incredible. 
However, some scenes in the latter half felt a bit drawn out.
"""

result = chain.invoke({"review": review_text})
print("\n","#"*50, "Solution for Exercise 1", "#"*50)
print(result)  # Will output structured MovieReview object














# Solution for Exercise 2: Recipe Steps Parser

# Create the parser
parser = CommaSeparatedListOutputParser()

#### Tip for writing queries
#### Print format instructions to see how this parser needs to be formatted.
# print(parser.get_format_instructions())


# Create the prompt template
prompt = PromptTemplate(
    template="Convert this recipe description into clear, separated steps:\n{recipe}\n{format_instructions}",
    input_variables=["recipe"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain
recipe_text = """
To make a basic omelette, crack three eggs into a bowl and whisk them well. 
Heat butter in a non-stick pan over medium heat. Pour the eggs into the pan, 
let them set slightly, add your fillings to one half, then fold the other 
half over. Cook until golden brown on the bottom.
"""

result = chain.invoke({"recipe": recipe_text})
print("\n","#"*50, "Solution for Exercise 2", "#"*50)
print(result)  # Will output list of recipe steps











# Solution for Exercise 3: Product Review Sentiment Parser

# Create the response schemas
response_schemas = [
    ResponseSchema(name="overall_rating", description="Overall product rating on a scale of 1-5"),
    ResponseSchema(name="pros", description="Description of positive aspects of the product"),
    ResponseSchema(name="cons", description="Description of negative aspects of the product"),
    ResponseSchema(name="sentiment_score", description="Sentiment score between -1 (negative) and 1 (positive)")
]

# Create the parser
parser = StructuredOutputParser.from_response_schemas(response_schemas)

#### Tip for writing queries
#### Print format instructions to see how this parser needs to be formatted.
# print(parser.get_format_instructions())


# Create the prompt template
prompt = PromptTemplate(
    template="Analyze the sentiment of this product review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain
review_text = """
I've been using this wireless keyboard for about a month now. The battery life is excellent - 
I've only had to charge it once. The keys have a nice tactile feel and it pairs easily with 
multiple devices. However, it's a bit heavier than I expected and the lack of backlighting 
makes it difficult to use in low light conditions. Overall, it's a good keyboard but has room 
for improvement.
"""

result = chain.invoke({"review": review_text})
print("\n","#"*50, "Solution for Exercise 3", "#"*50)
print(result)  # Will output structured review analysis










# Solution for Exercise 4: Meeting Notes Parser using JsonOutputParser

# Create the Pydantic model
class ActionItem(BaseModel):
    task: str = Field(description="The task to be completed")
    assignee: str = Field(description="Person assigned to the task")
    deadline: str = Field(description="Deadline for the task completion")

class MeetingNotes(BaseModel):
    title: str = Field(description="Meeting title")
    date: str = Field(description="Meeting date")
    participants: list[str] = Field(description="List of meeting attendees")
    action_items: list[ActionItem] = Field(description="List of action items from the meeting")
    decisions: list[str] = Field(description="List of decisions made during the meeting")

# Create the parser
parser = JsonOutputParser(pydantic_object=MeetingNotes)

#### Tip for writing queries
#### Print format instructions to see how this parser needs to be formatted.
# print(parser.get_format_instructions())

# Create the prompt template
prompt = PromptTemplate(
    template="Extract structured meeting information from these notes:\n{notes}\n{format_instructions}",
    input_variables=["notes"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain
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

result = chain.invoke({"notes": notes_text})
print("\n","#"*50, "Solution for Exercise 4", "#"*50)
print(result)  # Will output structured meeting notes










# Solution for Exercise 5: Date Extraction Parser

# Create the parser
parser = DatetimeOutputParser()

#### Tip for writing queries
#### Print format instructions to see how this parser needs to be formatted.
# print(parser.get_format_instructions())

# Create the prompt template
prompt = PromptTemplate(
    template="Extract the time mentioned in this text:\n{text}\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain for each sample text
sample_texts = [
    "Let's schedule our meeting for next Tuesday at 2pm.",
    "The product launch is set for June 15, 2025.",
    "The report is due on Vikas' desk by 8am Monday morning."
]

print("\n","#"*50, "Solution for Exercise 5", "#"*50)

for text in sample_texts:
    result = chain.invoke({"text": text})
    print(f"Text: {text}")
    print(f"Extracted date: {result}")
    print(f"Date type: {type(result)}")
    print("---")