from json import loads, JSONDecodeError

from loguru import logger

from .types import ReviewResponse
from g4f.Provider import ChatgptNext, FlowGpt
from g4f.client import Client

import nest_asyncio

nest_asyncio.apply()

user_message_instruction = """You are a highly proficient English speaker with deep understanding of the language. Your task is to evaluate the user's sentence based on the correct usage of the given word and its provided sense. Rate the sentence on a scale of 1 to 10, with 10 being a perfect usage. If the sentence is incorrect regarding the word usage, provide the correct version. If necessary, cite the relevant English language rules. If the studied word is not used in the sentence at all, rate it as 1 and provide constructive feedback. Always respond in the following JSON format for easy parsing:

{
    "score": [1-10 rating],
    "corrected_sentence": [corrected sentence or "N/A" if original is correct],
    "feedback": [feedback on word usage and any other issues],
    "explanation": [optional explanation of relevant rules]
}

Do not add any additional information outside of this JSON structure. If everything is correct, give the maximum score of 10 and provide positive feedback.
"""

user_message_1 = """{
  "word": "offensive",
  "sense": "rude in a way that causes somebody to feel upset or annoyed because it shows a lack of respect",
  "sentence": "i don't want to use offensive vocabulary"
}"""

assistant_message_1 = """{
  "score": 10,
  "feedback": "Your sentence correctly uses the word 'offensive' in the specified sense.",
  "explanation": "In your sentence, 'offensive' is used to describe vocabulary that could potentially cause upset or annoyance due to a lack of respect. This is indeed the correct usage according to the sense you provided.",
  "corrected_sentence": "N/A"
}"""

user_message_2 = """{
  "word": "arrive",
  "sense": "to get to a place, especially at the end of a journey",
  "sentence": "we don't like war"
}"""

assistant_message_2 = """{
  "score": 1,
  "feedback": "The word 'arrive' does not appear in your sentence, which makes it difficult to assess its usage.",
  "explanation": "Please ensure the provided word is included in the sentence so I can accurately evaluate its usage.",
  "corrected_sentence": "We don't arrive at our destination because we don't like war."
}"""



def do_review(word: str, sense: str, sentence: str) -> ReviewResponse:
    client = Client()

    response = client.chat.completions.create(

        model="mixtral-8x7b",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message_instruction},
            {"role": "user", "content": user_message_1},
            {"role": "assistant", "content": assistant_message_1},
            {"role": "user", "content": user_message_2},
            {"role": "assistant", "content": assistant_message_2},
            {"role": "user", "content": str({"word": word, "sense": sense, "sentence": sentence})}],
        # ignored=[
        #     "FreeGpt",
        #     # "ChatgptNext",
        # ],

        # provider=ChatgptNext
    )
    # response = (response.choices[0].message.content.replace("rule_means[optional]", "rule_means ")
    #             .replace("score:", '"score":').replace("feedback:", '"feedback":')
    #             .replace("explanation:", '"explanation":').replace("rule_means:", '"rule_means":')
    #             .replace("rule_means :", '"rule_means":')).replace("output: ", "")
    response = response.choices[0].message.content

    try:
        review = ReviewResponse.model_validate(loads(response))
    except JSONDecodeError:
        logger.error("ERROR!")
        print(response)
    return review
