import msgpack
from main import ExampleChild, encode_example, decode_example
from random import randint, choice, random
from string import ascii_letters, digits


def _rand_string(length):
    chars = ascii_letters + digits
    return "".join([choice(chars) for _ in range(length)])

def gen_test_obj() -> ExampleChild:
    return ExampleChild(
        randint(10000, 90000),
        _rand_string(30),
        {"a":randint(10000, 90000), "b":_rand_string(30)},
        random(),
    )

test_data_single = [gen_test_obj()]
test_data_multiple = [gen_test_obj() for _ in range(1000)]

def test_benchmark_single(benchmark):
    def serdes():
        encoded = msgpack.dumps(test_data_single, default=encode_example)
        msgpack.loads(encoded, object_hook=decode_example)
    benchmark(serdes)

def test_benchmark_multiple(benchmark):
    def serdes():
        encoded = msgpack.dumps(test_data_multiple, default=encode_example)
        msgpack.loads(encoded, object_hook=decode_example)
    benchmark(serdes)
