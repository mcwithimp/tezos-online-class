import smartpy as sp
class Voting(sp.Contract):
    def __init__(self):
        initial_candidates = {'Satoshi': 0, 'Arthur': 0, 'Vitalik': 0}
        self.init(
            owner = sp.address("tz1Kk1jF734jwhK4asf5LWMxWWN5yHiA9h7n"),
            candidates = sp.map(l = initial_candidates, tkey = sp.TString, tvalue = sp.TInt),
            voters = sp.map(tkey = sp.TAddress, tvalue = sp.TBool),
            voting_ended = False
        )
    @sp.entry_point
    def remove_candidate(self, params):
        sp.if (self.data.voting_ended == True):
            sp.failwith("Voting has already ended")
        sp.if (self.data.owner != sp.sender):
            sp.failwith("Only contract owner can remove candidate")
        sp.if (self.data.candidates.contains(params.name)):
            del self.data.candidates[params.name]
        sp.else:
            sp.failwith("No candidate")
    @sp.entry_point
    def add_candidate(self, params):
        sp.if (self.data.voting_ended == True):
            sp.failwith("Voting has already ended")
        sp.if (self.data.candidates.contains(params.name)):
            sp.failwith("Candidate already present")
        sp.else:
            self.data.candidates[params.name] = 0
    @sp.entry_point
    def close_election(self, params):
        sp.if (self.data.owner != sp.sender):
            sp.failwith("Only contract owner can close election")
        self.data.voting_ended = True
    @sp.entry_point
    def vote(self, params):
        sp.if (self.data.voting_ended == True):
            sp.failwith("Voting has already ended")
        addr = sp.sender
        sp.if (self.data.voters.contains(addr)):
            sp.failwith("Voter has already voted")
        sp.else:
            self.data.voters[addr] = True
        name = params.name
        sp.if (self.data.candidates.contains(name)):
            self.data.candidates[name] += 1
        sp.else:
            sp.failwith("Candidate is not valid")
            
if "templates" not in __name__:
    @sp.add_test(name = "Calculator")
    def test():
        owner = sp.address("tz1Kk1jF734jwhK4asf5LWMxWWN5yHiA9h7n")
        c1 = Voting()
        scenario = sp.test_scenario()
        scenario += c1
        scenario += c1.vote(name = "Satoshi").run(sender = sp.address("tz1a"))
        scenario += c1.vote(name = "Arthur").run(valid = False, sender = sp.address("tz1a"))
        scenario += c1.vote(name = "Lee").run(valid = False, sender = sp.address("tz1b"))
        scenario += c1.vote(name = "Arthur").run(sender = sp.address("tz1b"))
        scenario += c1.vote(name = "Arthur").run(sender = sp.address("tz1c"))
        scenario += c1.add_candidate(name = "Arthur").run(valid = False, sender = sp.address("tz1b"))
        scenario += c1.add_candidate(name = "Lee").run(sender = sp.address("tz1b"))
        scenario += c1.remove_candidate(name = "Lee").run(valid = False, sender = sp.address("tz1b"))
        scenario += c1.remove_candidate(name = "Lee").run(sender = owner)
        scenario += c1.close_election().run(valid = False, sender = sp.address("tz1b"))
        scenario += c1.close_election().run(sender = owner)
        scenario += c1.add_candidate(name = "Choi").run(valid = False, sender = sp.address("tz1b"))
        scenario += c1.vote(name = "Arthur").run(valid = False, sender = sp.address("tz1d"))
        # scenario.verify(c1.data.value == 524)