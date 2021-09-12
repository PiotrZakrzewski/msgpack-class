import msgpack
import json
import pytest
from main import ExampleChild, encode_example, decode_example
from random import randint, choice, random
from string import ascii_letters, digits


def _rand_string(length):
    chars = ascii_letters + digits
    return "".join([choice(chars) for _ in range(length)])

def gen_test_obj(fields_no) -> ExampleChild:
    big_dict = {}
    for i in range(fields_no):
        big_dict[f"{i}_str"] = _rand_string(30)
        big_dict[f"{i}_int"] = randint(10000, 90000)
        big_dict[f"{i}_float"] = random()
        big_dict[f"{i}_bool"] = choice([True, False])
    return ExampleChild(
        randint(10000, 90000),
        _rand_string(30),
        big_dict,
        random(),
    )

single = gen_test_obj(1)
_100 = gen_test_obj(100)
_1k = gen_test_obj(1000)
_10k = gen_test_obj(10000)

@pytest.mark.parametrize("lib", ["msgpack", "json"])
@pytest.mark.parametrize("test_data", [single, _100, _1k, _10k], ids=["single", "100", "1k", "10k"])
def test_dumps(benchmark, lib, test_data):
    def serdes():
        if lib == "msgpack":
            msgpack.dumps(test_data, default=encode_example)
        elif lib == "json":
            json.dumps(test_data.as_dict())
    benchmark(serdes)

@pytest.mark.parametrize("lib", ["msgpack", "json"])
@pytest.mark.parametrize("test_data", [single, _100, _1k, _10k], ids=["single", "100", "1k", "10k"])
def test_loads(benchmark, lib, test_data):
    if lib == "msgpack":
        encoded = msgpack.dumps(test_data, default=encode_example)
        def serdes():
            msgpack.loads(encoded, object_hook=decode_example)
    elif lib == "json":
        encoded = json.dumps(test_data.as_dict())
        def serdes():
            json.loads(encoded)
    benchmark(serdes)
