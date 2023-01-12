from functools import wraps


def decorator_one(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("Decorator one")
        return result
    return wrapper


def decorator_two(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("Decorator two")
        return result
    return wrapper


@decorator_one
@decorator_two
def greeting(word):
    print(f'Hello {word}')


if __name__ == '__main__':
    greeting('world!')
    greeting.__wrapped__('Maksym')
    greeting.__wrapped__.__wrapped__('Nikita')
    