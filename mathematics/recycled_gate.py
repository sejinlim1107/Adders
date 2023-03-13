import cirq

# 이거 버전 안맞아서 에러나서 수정함
# 주석처리 해놓은 코드가 Siyi 코드임
class RecycledGate(cirq.Operation.gate):#(cirq.ops.SingleQubitGate):
    """
        This is a gate that is used as a placeholder in the diagrams
    """

    def __init__(self, name = "NoName"):
        self.name = name

    def __str__(self):
        return self.name