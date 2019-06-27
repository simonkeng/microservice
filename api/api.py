import hug

@hug.get('/greet/{user}', version=1)
def greet(user: str):
    return f"Hello {user}! Nice to meet you."
