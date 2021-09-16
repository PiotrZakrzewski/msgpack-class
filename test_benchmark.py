import msgpack
import json
import pytest
from main import ExampleChild, encode_example, decode_example
from random import randint, choice, random
from string import ascii_letters, digits
import pickle


def _rand_string(length):
    chars = ascii_letters + digits
    return "".join([choice(chars) for _ in range(length)])

def gen_test_obj(fields_no) -> ExampleChild:
    big_dict = {"big_array":[]}
    for i in range(fields_no):
        big_dict["big_array"].append(randint(10000, 90000))
        rand_elem = {}
        rand_elem["str"] = _rand_string(30)
        rand_elem["int_tuple"] = (randint(10000, 90000), randint(10000, 90000))
        rand_elem["float"] = random()
        rand_elem["bool"] = choice([True, False])
        big_dict[str(i)] = rand_elem
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

@pytest.mark.parametrize("lib", ["msgpack", "json", "pickle4", "pickle5"])
@pytest.mark.parametrize("test_data", [single, _100, _1k, _10k], ids=["single", "100", "1k", "10k"])
def test_dumps(benchmark, lib, test_data):
    def serdes():
        if lib == "msgpack":
            msgpack.dumps(test_data, default=encode_example)
        elif lib == "json":
            json.dumps(test_data.as_dict())
        elif lib == "pickle4":
            pickle.dumps(test_data, protocol=4)
        elif lib == "pickle5":
            pickle.dumps(test_data, protocol=5)
    benchmark(serdes)

@pytest.mark.parametrize("lib", ["msgpack", "json", "pickle4", "pickle5"])
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
    elif lib == "pickle4":
        encoded = pickle.dumps(test_data, protocol=4)
        def serdes():
            pickle.loads(encoded)
    elif lib == "pickle5":
        encoded = pickle.dumps(test_data, protocol=5)
        def serdes():
            pickle.loads(encoded)
    benchmark(serdes)
