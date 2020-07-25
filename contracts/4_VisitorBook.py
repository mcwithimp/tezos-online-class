import smartpy as sp

class VisitorBook(sp.Contract):
    def __init__(self):
        self.init(
            book=sp.map(tkey= sp.TAddress, tvalue=sp.TString)
        )
    
    @sp.entry_point
    def write(self, params):
        self.data.book[sp.sender] = params.data
        
@sp.add_test(name = "Visitor Book")
def test():
    scenario = sp.test_scenario()
    contract = VisitorBook()
    scenario += contract
    
    scenario.h1("Visitor Book")
    
    scenario.h2("Visitor tz1 comes first")
    scenario += contract.write(data = "I am here!").run(sender = sp.address("tz1"))
    
    scenario.h2("Visitor tz2 comes first")
    scenario += contract.write(data = "My name is tz2!").run(sender = sp.address("tz2"))
    
    scenario.h2("Visitor tz1 comes again")
    scenario += contract.write(data = "tz1 is back!").run(sender = sp.address("tz1"))