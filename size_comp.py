import json
import msgpack
from test_benchmark import single, _100, _1k, _10k
from main import encode_example

test_data = [single, _100, _1k, _10k]

for i, data in enumerate(test_data):
    with open(f"msgpack_{i}.bin", "wb") as outf:
        msgpack.dump(data, outf, default=encode_example)
    with open(f"json_{i}.json", "w") as outf:
        json.dump(data.as_dict(), outf)
