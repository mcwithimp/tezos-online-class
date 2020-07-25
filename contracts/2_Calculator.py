import smartpy as sp

class Calculator(sp.Contract):
    def __init__(self):
        self.init(
            result=0
        )
    
    @sp.entry_point
    def add(self, params):
        self.data.result = params.x + params.y

@sp.add_test(name = "Calculator")
def test():
    scenario = sp.test_scenario()
    contract = Calculator()
    scenario += contract
    
    scenario.h1("Calculator")
    
    scenario.h2("Calculate 2 + 3")
    scenario += contract.add(x = 2, y = 3)
    
    scenario.h2("Calculate 10 + 100")
    scenario += contract.add(x = 10, y = 100)