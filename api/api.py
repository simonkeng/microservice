import hug
import requests

@hug.get('/greet/{user}', version=1)
def greet(user: str):
    return f"Hello {user}! Nice to meet you."


@hug.get('/return_data', version=1)
def return_data():

    data = '7849056728596798296'

    return f"{data}"
