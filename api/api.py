import hug
import requests

@hug.get('/greet/{user}', version=1)
def greet(user: str):
    
    # api to access "web" container
    # r = requests.get('web:8000/cat')
    # print(r.status_code)
    
    return f"Hello {user}! Nice to meet you."
