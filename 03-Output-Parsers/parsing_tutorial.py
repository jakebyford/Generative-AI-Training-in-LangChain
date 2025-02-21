# parsing_tutorial.py

# Create environment
# python -m venv venv
# Windows:  source venv\Scripts\activate
# Mac:  source venv/bin/activate
# pip install langchain langchain_core pydantic langchain_openai

# SET API KEY
# export OPENAI_API_KEY="sk-proj---------------------------------------------"

# VIEW IF API KEY IS IN ENVIRONMENT
# echo $OPENAI_API_KEY

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
from datetime import datetime



"""
Introduction to Output Parsing in LangChain
-----------------------------------------

Output parsing is a crucial concept in LangChain that helps structure LLM responses
into formats that are easier to work with in your applications. Instead of dealing
with raw text, parsers help you convert LLM outputs into Python objects, lists,
or other structured formats.

Key Concepts:
1. Output Parsers: Tools that convert raw LLM output into structured formats
2. Format Instructions: Templates that tell the LLM how to format its response
3. Parsing Rules: Specific formatting requirements for different parser types

Common Parser Types in LangChain:
-------------------------------




##################################################################################################################


1. PydanticOutputParser
   - Uses Pydantic models to define structured output
   - Great for complex, nested data structures
   - Validates output against a schema
   Example:
"""

class Person(BaseModel):
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    interests: list[str] = Field(description="List of the person's interests or hobbies")
    occupation: str = Field(description="The person's job or occupation", default="Unknown")


parser = PydanticOutputParser(pydantic_object=Person)

# Create the prompt template
prompt = PromptTemplate(
    template="""Please extract structured information about this person. Include their name, age, interests, and occupation if mentioned.
    
Text to analyze: {query}

{format_instructions}

Remember to:
- Extract the name and age accurately
- List any mentioned interests or hobbies
- Include occupation if stated, otherwise mark as "Unknown"
""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Set up the LLM and create the chain
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Run the chain
human_prompt = """
Hi there! I'm Jake, a 30-year-old data scientist based in New Jersey. 
I'm really passionate about Generative AI and machine learning. In my free time, 
I enjoy baseball and playing chess. I've been working in tech for about 5 years now.
"""

result = chain.invoke({"query": human_prompt})
print(result)  # Will output structured Person object
print(type(result)) # Will output object type

##################################################################################################################
"""
2. CommaSeparatedListOutputParser (CSV)
   - Splits output into a list using commas
   - Simple but effective for basic list operations
   - Ideal for generating CSV-like outputs for spreadsheets or database
   Example:
"""

list_parser = CommaSeparatedListOutputParser()

# Get the format instructions from the parser
format_instructions = list_parser.get_format_instructions()

# Create a prompt template
prompt = PromptTemplate(
    template="Generate a list of {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)

# Initialize the LLM
llm = ChatOpenAI(temperature=0.5)

# Create the chain
chain = prompt | llm | list_parser

# Example 1: Generating a list of fruits
result = chain.invoke({"subject": "tropical fruits"})
print(result)

# Example 2: Generating a list of programming languages
result = chain.invoke({"subject": "popular programming languages in 2024"})
print(result)

##################################################################################################################
"""
3. StructuredOutputParser
   - Defines custom response schemas
   - More flexible than Pydantic for simple cases
   Example:
"""

response_schemas = [
    ResponseSchema(name="color", description="The primary color"),
    ResponseSchema(name="mood", description="The mood it evokes")
]
structured_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = structured_parser.get_format_instructions()

prompt = PromptTemplate(
    template="""Analyze the following item and extract its color and the mood it evokes.

Item: {item}

{format_instructions}
""",
    input_variables=["item"],
    partial_variables={"format_instructions": format_instructions}
)

# Initialize the LLM
llm = ChatOpenAI(temperature=0)

# Create the chain
chain = prompt | llm | structured_parser

# Example 1: Analyzing a sunset
result = chain.invoke({
    "item": "A vibrant sunset over the ocean"
})
print(result)
# Output: {"color": "orange", "mood": "peaceful"}

# Example 2: Analyzing a stormy sky
result = chain.invoke({
    "item": "Dark storm clouds gathering overhead"
})
print(result)
# Output: {"color": "dark gray", "mood": "ominous"}

##################################################################################################################
"""
4. Advanced StructuredOutputParser
   - Handling Multiple Types of Data
   - Example with mixed data types:
"""


# Define the schemas
# This helps capture the data
mixed_schemas = [
    ResponseSchema(name="name", description="The name of the item"),
    ResponseSchema(name="year", description="The year of creation (integer)"),
    ResponseSchema(name="categories", description="List of relevant categories"),
    ResponseSchema(name="rating", description="Numerical rating from 1-5 (float)"),
    ResponseSchema(name="description", description="Brief text description")
]

# Create parser
mixed_parser = StructuredOutputParser.from_response_schemas(mixed_schemas)

# Get format instructions
format_instructions = mixed_parser.get_format_instructions()

# Create prompt template
prompt = PromptTemplate(
    template="""Please analyze the following item and provide a structured review.

Item to analyze: {item}

Provide the following information:
1. The item's name
2. The year it was created
3. Categories it belongs to
4. A rating from 1-5 (can use decimals)
5. A brief description (2-3 sentences)

{format_instructions}

Be specific and accurate with the details.""",
    input_variables=["item"],
    partial_variables={"format_instructions": format_instructions}
)

# Set up LLM and chain
llm = ChatOpenAI(temperature=0.2)  # Lower temperature for more consistent output
chain = prompt | llm | mixed_parser

# Example usage
test_item = """
The iPhone 14 Pro is Apple's flagship smartphone released in late 2022. It features 
a 48MP camera, the A16 Bionic chip, and the innovative Dynamic Island. The phone 
comes with iOS 16 and is available in various colors including Deep Purple and Gold.
"""

result = chain.invoke({"item": test_item})
print(result)

##################################################################################################################
"""
5. DatetimeOutputParser
   - Helps extract and standardize date and time information.
   Example:
"""

# Initialize parser
datetime_parser = DatetimeOutputParser()

print(datetime_parser.get_format_instructions())

# Create prompt template
prompt = PromptTemplate(
    template="""Answer the users question:
    Text: {text}

    {format_instructions}
    """,
    input_variables=["text"],
    partial_variables={"format_instructions": datetime_parser.get_format_instructions()}
)

# Create chain
chain = prompt | llm | datetime_parser

# Example usage
result = chain.invoke({
    "text": "When was Bitcoin founded?"
})
print(result)  # Returns a datetime object



##################################################################################################################
"""
6. JsonOutputParser
   - JSON is one of the most versatile data formats for APIs and storage.
   Example:
"""

# Define the data structure
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

# Initialize the model
model = ChatOpenAI(temperature=0)

# Create a JSON parser with the defined schema
json_parser = JsonOutputParser(pydantic_object=Joke)

# Define a prompt template
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": json_parser.get_format_instructions()},
)

# Combine prompt, model, and parser into a chain
chain = prompt | model | json_parser

# Generate a joke
joke_query = "Tell me a joke."
result = chain.invoke({"query": joke_query})
print(result)



"""
Using Parsers with Prompts:
-------------------------

1. Get format instructions from parser:
   format_instructions = parser.get_format_instructions()

2. Include instructions in your prompt:
   prompt = PromptTemplate(
       template="Answer query:\n{query}\n{format_instructions}",
       input_variables=["query"],
       partial_variables={"format_instructions": format_instructions}
   )

3. Create a chain:
   chain = prompt | llm | parser

Best Practices:
-------------
1. Always validate parser output
2. Use appropriate parser for your use case
3. Include clear format instructions
4. Handle parsing errors gracefully
5. Test with various inputs

Now that you understand the basics, try the exercises below!
"""