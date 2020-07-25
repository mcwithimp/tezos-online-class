import smartpy as sp

class Memo(sp.Contract):
    def __init__(self):
        self.init(
            memo="hello"
        )
    
    @sp.entry_point
    def write(self, params):
        self.data.memo = params.data
        
@sp.add_test(name = "Simple Memo")
def test():
    scenario = sp.test_scenario()
    contract = Memo()
    scenario += contract
    
    scenario.h1("Simple Memo")
    
    scenario.h2("First memo")
    scenario += contract.write(data = "world")

    scenario.h2("Second memo")
    scenario += contract.write(data = "blockchain")