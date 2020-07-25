import React, { useState, useEffect } from 'react'
import { Tezos } from '@taquito/taquito'
import './Memo.css'

// const RPC_ADDR = 'http://127.0.0.1:8732'
const RPC_ADDR = 'http://192.168.0.171:8732'
const CONTRACT_ADDR = "KT1DBaG4RWxHw8Sjoj4gwJSeQ4KBZ61TtGvX"
const PRIVATE_KEY = "edsk4c9wy8vTyXJY8awsDQ7HU9zWEWRjSxXA2PgXr8azfJ8vZzfmZg"
const PASSPHRASE = ""

Tezos.setProvider({ rpc: RPC_ADDR })
importKey(PRIVATE_KEY, PASSPHRASE)

async function importKey(key: string, passphrase ?: string) {
  return Tezos.importKey(key, passphrase)
}

async function getStorage() {
  const contract =  await getContract()
  const storage = await contract.storage()
  return storage as string
}

async function getContract() {
  return await Tezos.contract.at(CONTRACT_ADDR)
}

async function injectMemo(content: string) {
  const contract = await getContract()
  const response = await contract.methods.main(content).send()
  const level = await response.confirmation()
  return level
}

const Memo = () => {
  const [userInput, setUserInput] = useState('')
  const [inTransaction, setInTransaction] = useState(false)
  const [storage, setStorage] = useState('Loading ...')

  const updateStorage = async () => {
    const storage = await getStorage()
    setStorage(storage)
  }

  useEffect(() => {
    const interval = setInterval(updateStorage, 2000)
    return () => clearInterval(interval)
  }, [])

  const onMemoInject = async (userInput: string) => {
    try {
      setInTransaction(true)
      const level = await injectMemo(userInput)
      alert(`Your memo is included at block ${level}`)
      setUserInput('')
      setInTransaction(false)
    } catch (e) {
      alert(e.message)
      setInTransaction(false)
    }
  }


  return (
    <div className="app">
      <header>
        Memo<br/>
        {inTransaction && <p>Waiting for a block confirmation...</p>}
      </header>

      <main>
        <div className="memo">
          <div>
            {storage}
          </div>
        </div>
      </main>

      <footer>
        <label>
          <span>Content</span>
          <textarea
            placeholder="Write your memo here"
            value={userInput}
            disabled={inTransaction}
            onChange={ev => setUserInput(ev.currentTarget.value) }
          />
        </label>

        <button
          disabled={inTransaction}
          onClick={() => onMemoInject(userInput)}
        >
          {'Write Memo'}
        </button>
      </footer>

    </div>

  );
}

export default Memo
