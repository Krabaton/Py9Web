import logging

logging.basicConfig(
    format="%(asctime)s %(funcName)15s - %(message)s",
    level=logging.DEBUG,
    handlers=[logging.FileHandler("program.log"), logging.StreamHandler()],
)


def foo(num: int):
    result = num**2
    logging.debug(f"result: {result}")
    return result


if __name__ == "__main__":
    foo(13)
