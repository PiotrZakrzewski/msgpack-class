class Example:
    def __init__(self, param1:int, param2:str, param3:dict) -> None:
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def as_dict(self) -> dict:
        return {
            "param1": self.param1,
            "param2": self.param2,
            "param3": self.param3,
        }

class ExampleChild(Example):
    def __init__(self, param1: int, param2: str, param3: dict, param4:float) -> None:
        super().__init__(param1, param2, param3)
        self.param4 = param4

    def as_dict(self) -> dict:
        dict_rep = super().as_dict()
        dict_rep["param4"] = self.param4
        return dict_rep

def encode_example(obj):
    if isinstance(obj, ExampleChild):
        return {"__ExampleChild__": True, "fields":{
            "param1":obj.param1,
            "param2":obj.param2,
            "param3":obj.param3,
            "param4":obj.param4,
            }
        }
    if isinstance(obj, Example):
        return {"__Example__": True, "fields":{
            "param1":obj.param1,
            "param2":obj.param2,
            "param3":obj.param3,
            }
        }
    return obj

def decode_example(obj):
    if "__ExampleChild__" in obj:
        return ExampleChild(**obj["fields"])
    if "__Example__" in obj:
        return Example(**obj["fields"])
    return obj
