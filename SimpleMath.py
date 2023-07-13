import ast
import math
import re
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,        # TODO: this requires more parsing to avoid float pow'ing
    #ast.BitXor: op.xor,
    #ast.USub: op.neg,
    #ast.Mod: op.mod
}

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        return 0

class SimpleMath:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("FLOAT", { "default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1 }),
                "b": ("FLOAT", { "default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1 }),
                "operation": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", )

    FUNCTION = "do_math"

    CATEGORY = "utils"

    def do_math(self, a, b, operation):
        # TODO: check if it can be done with a one-liner
        operation = re.sub(r'\b[aA]\b', str(a), operation)
        operation = re.sub(r'\b[bB]\b', str(b), operation)

        result = eval_(ast.parse(operation, mode='eval').body)

        if math.isnan(result):
            result = 0.0

        return (round(result), result, )

NODE_CLASS_MAPPINGS = {
    "SimpleMath": SimpleMath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleMath": "Math op"
}
