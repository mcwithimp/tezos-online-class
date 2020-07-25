import smartpy as sp

class VisitorBookCalculator(sp.Contract):
    def __init__(self):
        self.init(
            book=sp.map(tkey= sp.TAddress, tvalue=sp.TString),
            result=sp.map(tkey= sp.TAddress, tvalue=sp.TInt),
        )
    
    @sp.entry_point
    def write(self, params):
        self.data.book[sp.sender] = params.data
        
    @sp.entry_point
    def add(self, params):
        sp.set_type(params.x, sp.TInt)
        self.data.result[sp.sender] = params.x + params.y
        
    @sp.entry_point
    def sub(self, params):
        sp.set_type(params.x, sp.TInt)
        self.data.result[sp.sender] = params.x - params.y
        
@sp.add_test(name = "Visitor Book and Calculator")
def test():
    scenario = sp.test_scenario()
    contract = VisitorBookCalculator()
    scenario += contract
    
    scenario.h1("Visitor Book and Calculator")
    
    scenario.h2("Visitor tz1 comes first")
    scenario += contract.write(data = "I am here!").run(sender = sp.address("tz1"))
    
    scenario.h2("Visitor tz1 add 5 + 2")
    scenario += contract.add(x = 5, y = 2).run(sender = sp.address("tz1"))
    
    scenario.h2("Visitor tz2 comes first")
    scenario += contract.write(data = "My name is tz2!").run(sender = sp.address("tz2"))
    
    scenario.h2("Visitor tz1 comes again")
    scenario += contract.write(data = "tz1 is back!").run(sender = sp.address("tz1"))
    
    scenario.h2("Visitor tz2 sub 1 - 1000")
    scenario += contract.sub(x = 1, y = 1000).run(sender = sp.address("tz2"))
    
    