from colorama import init as colorama_init
from colorama import Fore, Style
import subprocess
import requests
import time
import random
from datetime import datetime

colorama_init()

prefix = ".."

conversation_history = []

def clear_screen():
    subprocess.call("cls", shell=True)

def check_api_key(api_key):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "This is a test."}],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)

    return response.status_code == 200

clear_screen()
print(f"\nWelcome to CMD-GPT!\n{Fore.RED}NOTE: Your data won't be stored.{Style.RESET_ALL}\n")

while True:

    openai_api_key = input(f"{Fore.GREEN}Please enter your OpenAI API key to continue:{Style.RESET_ALL} ")

    if check_api_key(openai_api_key):
        clear_screen()
        break

    else:
        clear_screen()
        print(f"{Fore.RED}Invalid API Key. Please try again.{Style.RESET_ALL}")

clear_screen()

def send_prompt(user_input, api_key, conversation_history):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


    conversation_history.append(user_input)

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]


    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{user_input} conversation history to keep track: {conversation_history}"}],
        "temperature": 0.7,
    }


    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)


    if response.status_code == 200:

        completion = response.json()["choices"][0]["message"]
        return completion["content"]
    else:

        clear_screen()
        return f"{Fore.RED}{Style.BRIGHT} There went something wrong with the AI. Please try again later.\nError: {response.status_code}{Style.RESET_ALL}"
        exit()
        

print(f"Type {Fore.GREEN}{Style.BRIGHT}..exit{Style.RESET_ALL} to quit.\n")

while True:

    user_input = input(f"{Fore.BLUE}{Style.BRIGHT}You:{Style.RESET_ALL} ")

    if user_input.lower() == prefix + "exit":
        clear_screen()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        print(f"{Fore.RED}{Style.BRIGHT}Session closed at {current_time}{Style.RESET_ALL}")
        break

    print(f"{Fore.CYAN}{Style.BRIGHT}GPT:{Style.RESET_ALL} ...", end="\r")

    gpt_response = send_prompt(user_input, openai_api_key, conversation_history)

    print(f"{Fore.CYAN}{Style.BRIGHT}GPT:{Style.RESET_ALL} {gpt_response}{' ' * 50}")