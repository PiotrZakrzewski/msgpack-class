from typing import List
import msgpack
import json
import pytest
from main import Example, ExampleChild, encode_example, decode_example, encode_example_proto, decode_example_proto
from random import randint, choice, random
from string import ascii_letters, digits
import pickle


def _rand_string(length=30):
    chars = ascii_letters + digits
    return "".join([choice(chars) for _ in range(length)])

def _rand_float_list(length) -> List[float]:
    return [random() for _ in range(length)]

def gen_test_obj(children_no: int) -> Example:
    children = [ExampleChild(randint(1000, 10000), _rand_string(), [random(), random()]) for _ in range(children_no)]
    return Example(randint(1000, 10000), _rand_string(), _rand_float_list(children_no), children)

single = gen_test_obj(1)
_100 = gen_test_obj(100)
_1k = gen_test_obj(1000)
_10k = gen_test_obj(10000)
_100k = gen_test_obj(100000)
test_sets = [single, _100, _1k, _10k, _100k]
test_set_labels = ["single", "100", "1k", "10k", "100k"]
libs = ["msgpack", "json", "pickle4", "pickle5", "proto"]

@pytest.mark.parametrize("lib", libs)
@pytest.mark.parametrize("test_data", test_sets, ids=test_set_labels)
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
        elif lib == "proto":
            encode_example_proto(test_data)
    benchmark(serdes)

@pytest.mark.parametrize("lib", libs)
@pytest.mark.parametrize("test_data", test_sets, ids=test_set_labels)
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
    elif lib == "proto":
        encoded = encode_example_proto(test_data)
        def serdes():
            decode_example_proto(encoded)
    benchmark(serdes)
