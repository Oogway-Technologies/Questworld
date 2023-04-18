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
--data '{
    "memories": [
        "Bruce witnessing his parents'\'' murder in Crime Alley, fueling his desire for justice",
        "Bruce met and trained with various mentors around the world, honing his skills in martial arts, detective work, and other disciplines",
        "As a masked vigilante, he encounters different kind of bad people, in particular a sociopath person dresses like a clown"
    ]
}'
```

You should receive an output that is similar to the following:

```JSON
{
    "metadata": {
        "metrics": {
            "num_requests": {
                "type": "COUNT",
                "value": 1
            },
            "time_duration": {
                "type": "RATE",
                "value": 7.39660120010376
            }
        }
    },
    "summary": "Name: Bruce (age: 25)\nInnate traits: intelligent, idealist, realist\nBruce is a skilled and disciplined individual who has trained extensively in various areas, including martial arts and detective work. He is driven by a desire for justice, stemming from the traumatic experience of witnessing his parents' murder in Crime Alley. As a vigilante, he faces dangerous criminals, including a particularly disturbing sociopath who dresses like a clown."
}
```
