from .types import ReviewResponse
from g4f.Provider import ChatgptNext
from g4f.client import Client
from json import loads

import nest_asyncio
nest_asyncio.apply()


def build_prompt(word: str, sense: str, sentence: str) -> str:
    message = """
I'm native english speaker with excellent english knowledge. My task is to evaluate the user's sentence based on its usage of the given word and its sense. Rate the sentence on a scale of 1 to 10. If the sentence is incorrect, provide the correct version. If necessary, cite the relevant English language rules. If the studied word is not used in the sentence, rate 1 score and provide feedback. Always respond in the same format for easy parsing. Don’t try to make mistakes out of thin air, if everything is fine, just give the maximum score and praise.

Example:

input: {
 word: "Umbrella",
 sense: "A portable cover used for protection from rain or sun.",
 sentence: "I always bring umbrella with me when it raining"
}

output: {
 score: 7,
 feedback: "The sentence is grammatically incorrect. The correct sentence should be: 'I always bring an umbrella with me when it is raining.'",
 explanation: "In English, we usually use an article (a, an, the) before a singular, countable noun. Also, the verb 'to be' is needed before 'raining'.",
 rule_means[optional]: "Articles are used before nouns and depend on whether the noun is countable or uncountable, and whether it is specific or not. The verb 'to be' is used to describe the state of being."
}
"""
    data = str({"word": word, "sense": sense, "sentence": sentence})
    return f"""{message}
Current input: 
{data}
"""


def do_review(word: str, sense: str, sentence: str) -> ReviewResponse:
    prompt = build_prompt(word, sense, sentence)
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt}],
        ignored=[
            "FreeGpt",
            # "ChatgptNext",
        ],
        provider=ChatgptNext
    )

    response = (response.choices[0].message.content.replace("rule_means[optional]", "rule_means ")
                .replace("score:",'"score":').replace("feedback:", '"feedback":')
                .replace("explanation:", '"explanation":').replace("rule_means:", '"rule_means":')
                .replace("rule_means :", '"rule_means":'))
    return ReviewResponse.model_validate(loads(response))