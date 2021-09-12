import msgpack
import json
import pytest
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

single = [gen_test_obj()]
_100 = [gen_test_obj() for _ in range(100)]
_1k = [gen_test_obj() for _ in range(10000)]
_10k = [gen_test_obj() for _ in range(1000*10)]

@pytest.mark.parametrize("lib", ["msgpack", "json"])
@pytest.mark.parametrize("test_data", [single, _100, _1k, _10k], ids=["single", "100", "1k", "10k"])
def test_dumps(benchmark, lib, test_data):
    def serdes():
        if lib == "msgpack":
            msgpack.dumps(test_data, default=encode_example)
        elif lib == "json":
            data = [d.as_dict() for d in test_data]
            json.dumps(data)
    benchmark(serdes)

@pytest.mark.parametrize("lib", ["msgpack", "json"])
@pytest.mark.parametrize("test_data", [single, _100, _1k, _10k], ids=["single", "100", "1k", "10k"])
def test_loads(benchmark, lib, test_data):
    if lib == "msgpack":
        encoded = msgpack.dumps(test_data, default=encode_example)
        def serdes():
            msgpack.loads(encoded, object_hook=decode_example)
    elif lib == "json":
        data = [d.as_dict() for d in test_data]
        encoded = json.dumps(data)
        def serdes():
            json.loads(encoded)
    benchmark(serdes)
