# QuestWorld Setup

## Why QuestWorld?

Some lore about QuestWorld can be found here: https://jonnyquest.fandom.com/wiki/Questworld

TL;DR

Questworld, also written QuestWorld, is the highly intricate virtual reality computer system created by Dr. Benton Quest. Jonny, Hadji, and Jessie primarily use it for creating and playing virtual reality games. Dr. Jeremiah Surd tries to take control of it to dominate cyberspace.
It operates with an artificial intelligence named Iris.

## How do I start?

Follow these steps:

- Create a virtual environmet for Python 3.10 (use pyenv if you want to switch between Python versions: https://github.com/pyenv/pyenv)
- Install the requirements in requirements.txt
- Download en_core_web_md SpaCy model:

```BASH
python -m spacy download en_core_web_md
```

- create an .env file following the env_example file (use your OpenAI credentials)

## How do I run the app?

You can choose to run the stand-alone app or the server.

To run the app stand-alone use

```BASH
python app.py
```

To run the server use

```BASH
python app.py --run_server true --service_type <service>
```

where 'service' is the type of service you want to run, for example 'demo'.

## How do I send requests to the server?

You can use Postman to send request to the server with a raw JSON type payload or use curl:

```BASH
curl --location 'http://127.0.0.1:6000/' \
--header 'Content-Type: application/json' \
--data '{
    "objective": "Write an essay on the character Joel from the last of us video game."
}'
```

### Example with agent

Run the following

```BASH
python app.py --run_server true --service_type agents
```

and send the following request:

```BASH
curl --location 'http://127.0.0.1:6000/' \
--header 'Content-Type: application/json' \
--data '<agents_content>'
```

where agents_content is the JSON content you can find under

```BASH
projects/llm/agents/examples/agents.json
```

You should see the conversation on the screen similar to the following:

```
Arthur Arthur pauses briefly before continuing with the attempted robbery.
Bruce said "Stop right there, Arthur. You're not getting away with this."
Arthur said "Oh, Bruce. You always were such a stickler for the rules. But I'm afraid I have to go through with this. It's nothing personal, you understand. Just business."
Bruce said "Arthur, there are no excuses for breaking the law. You know that. And I won't let you get away with it. Turn yourself in now, and I'll make sure the consequences aren't as severe as they could be."
Arthur said "Oh Bruce, you always were such a goody two-shoes. But you know I can't turn myself in now. I have too much on the line. I appreciate your concern, but I have to do what I have to do."
Bruce said "Arthur, I understand that you may feel like you have no other choice, but there is always another way. You don't have to resort to crime to get what you want. Think about the consequences and make the right decision. Turn yourself in now and let's work together to find a solution that doesn't involve breaking the law."
```
