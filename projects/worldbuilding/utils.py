from langchain.prompts.chat import HumanMessagePromptTemplate


def get_goal_prompt():
    prompt = HumanMessagePromptTemplate.from_template(
        "You are {agent}. {agent_description}"
        + " You just woke up in {source_area} and went out to the {destination_area}."
        + " The following people live in the town: {people}."
        + " What is your goal for today? Be brief, and use at most 20 words and answer from your perspective."
    )
    return prompt


def get_plan_prompt():
    prompt = HumanMessagePromptTemplate.from_template(
        "You are {agent}. {agent_description}\n"
        + "You are planning to: {plan}\n"
        + "You are currently in {location} with the following description: {location_description}.\n"
        + "It is currently {time}:00.\n"
        + "The following people are in this area: {people}\n"
        + "You can interct with them."
        + "You know the following about people:\n{people_description}."
        + "What do you want to do next? Be brief, and use at most 20 words and answer from your perspective."
    )
    return prompt


def get_plan_prompt_clean():
    prompt = HumanMessagePromptTemplate.from_template(
        "Convert the following paragraph to first person past tense:"
        + "\n{paragraph}"
    )
    return prompt
