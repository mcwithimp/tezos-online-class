import smartpy as sp

class Memo(sp.Contract):
    def __init__(self):
        self.init(
            memo = "hello",
        )   
    
    @sp.entry_point
    def write(self, params):
        self.data.memo = params.data

@sp.add_test(name = "ContractName")
def test():
    scenario = sp.test_scenario()
    contract = ContractName()
    scenario += contract
    
    scenario.h1("ContractName")
    
    scenario.h2("First memo")
    scenario += contract.entrypoint1(data = "world")

    scenario.h2("Second memo")
    scenario += contract.entrypoint1(data = "blockchain")
