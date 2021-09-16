from typing import List
from schema_pb2 import Example as ExampleProto, ExampleChild as ExampleChildProto
class Example:
    def __init__(self, param1:int, param2:str, param3:List[float], param4: List['ExampleChild']) -> None:
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4

    def as_dict(self) -> dict:
        return {
            "param1": self.param1,
            "param2": self.param2,
            "param3": self.param3,
            "param4": [child.as_dict() for child in self.param4],
        }

class ExampleChild:
    def __init__(self, param1:int, param2:str, param3: List[float]) -> None:
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def as_dict(self) -> dict:
        return {
            "param1": self.param1,
            "param2": self.param2,
            "param3": self.param3,
        }

def encode_example(obj):
    if isinstance(obj, ExampleChild):
        return {"__ExampleChild__": True, "fields": obj.as_dict() }
    if isinstance(obj, Example):
        return {"__Example__": True, "fields": obj.as_dict() }
    return obj

def decode_example(obj):
    if "__ExampleChild__" in obj:
        return ExampleChild(**obj["fields"])
    if "__Example__" in obj:
        return Example(**obj["fields"])
    return obj

def encode_example_proto(example: Example):
    ex_proto = ExampleProto()
    ex_proto.param1 = example.param1
    ex_proto.param2 = example.param2
    ex_proto.param3.extend(example.param3)
    ex_proto.param4.extend([_child_to_proto(c) for c in example.param4])
    return ex_proto.SerializeToString()

def _child_to_proto(example_child: ExampleChild) -> ExampleChildProto:
    ex_proto = ExampleChildProto()
    ex_proto.param1 = example_child.param1
    ex_proto.param2 = example_child.param2
    ex_proto.param3.extend(example_child.param3)
    return ex_proto

def decode_example_proto(encoded:bytes) -> Example:
    ex_proto = ExampleProto()
    ex_proto.ParseFromString(encoded)
    return Example(ex_proto.param1, ex_proto.param2, ex_proto.param3, ex_proto.param4)

