import React, { useState, useEffect } from 'react'
import './Voting.css'

async function importKey(key: string, passphrase ?: string) { }
async function getStorage() { }
async function getContract() { }

const Voting = () => {
  const [key, setKey] = useState({
    pkh: '',
    sk: '',
    passphrase: '',
    isKeyImported: false
  })
  const [inTransaction, setInTransaction] = useState(false)
  const [storage, setStorage] = useState<Storage>()
  const [newCandidateName, setNewCandidateName] = useState('')
  const isDisabled = !key.isKeyImported || inTransaction

  const updateStorage = async () => {
    const storage = await getStorage()
    setStorage(storage)
  }

  useEffect(() => {
    const interval = setInterval(updateStorage, 2000)
    return () => clearInterval(interval)
  }, [])

  async function injection(opName: string, name?: string) { }
  const onVote = (name: string) => injection("vote", name)
  const onRemoveCandidate = (name: string) => injection("remove", name)
  const onAddCandidate = (name: string) => injection("add", name)
  const onCloseElection = () => injection("close")

  return (
    <div className="app">
      <header>
        <h2>Key</h2>
        <label>
          <span>Private Key</span>
          <input
            type="password"
            value={key.sk}
            disabled={key.isKeyImported}
            onChange={ev => setKey({ ...key, sk: ev.currentTarget.value })}
          />
        </label>
        <label>
          <span>Passphrase (optional)</span>
          <input
            type="password"
            value={key.passphrase}
            disabled={key.isKeyImported}
            onChange={ev => setKey({ ...key, passphrase: ev.currentTarget.value })}
          />
        </label>
        <button onClick={async () => {
          try {
            await importKey(key.sk, key.passphrase)
            const pkh = await Tezos.signer.publicKeyHash()
            setKey({ ...key, pkh: pkh, isKeyImported: true })
          }
          catch(e) {
            alert(e.message)
            setKey({ pkh: "", sk: "", passphrase: "", isKeyImported: false })
          }
        }}>
          Import Keys
        </button>
      </header>
      <main className="vote">
        <h2>
          {
            (storage === undefined)
              ? 'Loading ...'
              : `Voting is ` + (storage.voting_ended ? 'ended' : 'ongoing')
          }<br/>
        </h2>
        <h3>
          {
            (!key.isKeyImported || !storage)
              ? ""
              : (
                storage.voters.hasOwnProperty(key.pkh)
                  ? `${key.pkh}(voted)`
                  : `${key.pkh}(not voted)`
              )
          }
        </h3>
        {inTransaction && <p>Waiting for block confirmation..</p>}

        <div className="candidates">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Votes</th>
                <th colSpan={2}></th> 
              </tr>
            </thead>
            <tbody>
              {candidates.map(({ name, votes }) => (
                <tr key={name}>
                  <td>{name}</td>
                  <td>{votes}</td>
                  <td>
                    <button 
                      onClick={() => onVote(name)}
                      disabled={isDisabled}
                    >
                      Vote
                    </button>
                  </td>
                  <td>
                    <button 
                      onClick={() => onRemoveCandidate(name)}
                      disabled={isDisabled}
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
      <footer>
        <div>
          <h4>Add Candidate</h4>
          <div>
            <input
              type="text"
              value={newCandidateName}
              disabled={isDisabled}
              onChange={ev => setNewCandidateName(ev.currentTarget.value)}
            />
            <button
              onClick={() => onAddCandidate(newCandidateName)}
              disabled={isDisabled}
            >
              Add candidate
            </button>
          </div>
        </div>

        <div>
          <h4>Close Election</h4>
          <button
            disabled={isDisabled}
            onClick={() => {
              if (window.confirm('Close this election? This action is irreversable.')) {
                onCloseElection()
              }
            }}
          >
            Close Election
          </button>
        </div>
      </footer>
    </div>
  );
}

export default Voting
