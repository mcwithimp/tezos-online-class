import smartpy as sp

class Calculator2(sp.Contract):
    def __init__(self):
        self.init(
            result=sp.int(0)
        )
    
    @sp.entry_point
    def add(self, params):
        sp.set_type(params.x, sp.TInt)
        self.data.result = params.x + params.y
        
    @sp.entry_point
    def sub(self, params):
        sp.set_type(params.x, sp.TInt)
        self.data.result = params.x - params.y
        
@sp.add_test(name = "Calculator2")
def test():
    scenario = sp.test_scenario()
    contract = Calculator2()
    scenario += contract
    
    scenario.h1("Calculator2")
    
    scenario.h2("Calculate 2 + 3")
    scenario += contract.add(x = 2, y = 3)

    scenario.h2("Calculate 10 - 100")
    scenario += contract.sub(x = 10, y = 100)