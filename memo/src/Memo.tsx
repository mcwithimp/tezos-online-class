import React, { useState, useEffect } from 'react'
import './Memo.css'

async function importKey(key: string, passphrase ?: string) { }
async function getStorage() { }
async function getContract() { }
async function injectMemo(content: string) { }

const Memo = () => {
  const [userInput, setUserInput] = useState('')
  const [inTransaction, setInTransaction] = useState(false)
  const [storage, setStorage] = useState('world')

  const updateStorage = async () => { }

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

