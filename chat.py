import random
import json

import pandas as pd
import duckdb
import openai
import time 
import os

from openai import OpenAI
import duckdb

bot_name = "Vegan-punk"

path = "./data/titanic"
files = [x for x in os.listdir(path = path) if ".csv" in x]
data = pd.concat((pd.read_csv(path +"/" + f) for f in files), ignore_index=True)
data.columns = [c.strip().replace(" ", "_").lower() for c in data.columns]


prompt_template = """

Given the following SQL table, your job is to write queries given a user’s request, giving only code, no explanantion, and ending the query with a semicolon. \n

CREATE TABLE {} ({}) \n

Write a SQL query that returns - {}
"""

def sql_prompt_generator(table_name, col_names, query):
    prompt = prompt_template.format(table_name, col_names, query)
    return prompt
table = "data"
col_names = str(list(data.columns)).replace('[', '').replace(']', '')
query = "How many passengers were there?"

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
openai_api_models = pd.DataFrame(client.models.list().data)


def get_response(msg):
    
    try:
        # msg = "How many passengers were there?"
        prompt = sql_prompt_generator(table_name = table, col_names = col_names, query = msg)
        model="gpt-4-1106-preview"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        response_text = response.choices[0].message.content
        startidtoken = "```sql"
        endidtoken = ";"
        sqlkey_select_loc = response_text.find(startidtoken)+len(startidtoken)
        sqlkey_semicolon_loc = response_text.find(endidtoken)
        query = response_text[sqlkey_select_loc:sqlkey_semicolon_loc]
    except Exception as e:
        print(e)
        return prompt
    
    return query


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

