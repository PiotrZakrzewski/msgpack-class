import msgpack
import json
from main import Example, ExampleChild, encode_example, decode_example

def test_serdes():
    ex1 = Example(1, 'bla', {'a':2})
    ex2 = ExampleChild(1, 'bla', {'a':2}, 3.14)
    payload = {"ex1": ex1, "ex2": ex2}
    encoded = msgpack.dumps(payload, default=encode_example)
    decoded = msgpack.loads(encoded, object_hook=decode_example)
    assert payload["ex1"].param1 == decoded["ex1"].param1
    assert payload["ex1"].param2 == decoded["ex1"].param2
    assert payload["ex1"].param3 == decoded["ex1"].param3

    assert payload["ex2"].param1 == decoded["ex2"].param1
    assert payload["ex2"].param2 == decoded["ex2"].param2
    assert payload["ex2"].param3 == decoded["ex2"].param3
    assert payload["ex2"].param4 == decoded["ex2"].param4


def test_json():
    ex2 = ExampleChild(1, 'bla', {'a':2}, 3.14)
    encoded = json.dumps(ex2.as_dict())
    decoded = json.loads(encoded)

    assert ex2.param1 == decoded["param1"]
    assert ex2.param2 == decoded["param2"]
    assert ex2.param3 == decoded["param3"]
    assert ex2.param4 == decoded["param4"]
