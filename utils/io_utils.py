import json
import yaml
from colorama import Fore
from pathlib import Path


def open_file(filepath, print_error: bool = True):
    if filepath is None:
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except Exception as e:
        if print_error:
            print(e)
        return None


def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)
    except Exception as e:
        return None


def load_template(module_folder: str, filename: str, load_json: bool = True, templates_folder: str = 'templates'):
    path_to_data = Path(__file__).parent.parent / \
        module_folder / templates_folder
    try:
        for file in path_to_data.iterdir():
            if file.is_file() and str(file.name) == filename:
                with open(file, "r") as infile:
                    if load_json:
                        # Read dictionary from file
                        data = json.load(infile)
                        return data
                    else:
                        # Read text from file
                        data = infile.read()
                        return data
    except Exception as e:
        print(e)
    return None


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def clean_input(prompt: str = ""):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("You interrupted Auto-GPT")
        print("Quitting...")
        exit(0)


def validate_yaml_file(file: str):
    try:
        with open(file, encoding="utf-8") as fp:
            yaml.load(fp.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        return (False, f"The file {Fore.CYAN}`{file}`{Fore.RESET} wasn't found")
    except yaml.YAMLError as e:
        return (
            False,
            f"There was an issue while trying to read with your AI Settings file: {e}",
        )

    return (True, f"Successfully validated {Fore.CYAN}`{file}`{Fore.RESET}!")
