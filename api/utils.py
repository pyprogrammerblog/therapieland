import random, string


def random_string():
    return ''.join(
        random.choice(
            string.ascii_uppercase +
            string.ascii_lowercase +
            string.digits +
            "_"
        ) for _ in range(6))
