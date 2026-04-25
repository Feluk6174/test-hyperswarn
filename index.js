const Hyperswarm = require('hyperswarm')
const crypto = require('crypto')
const readline = require('readline')

const TOPIC = crypto.createHash('sha256').update('hyperswarm-chat').digest()
const MAX_PEERS = 64

let username = 'Anonymous'
let usernameSet = false

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

const conns = new Set()
const swarm = new Hyperswarm()

process.stdout.write('\x1b[36mEnter your name: \x1b[0m')
rl.question('', (name) => {
  username = name.trim() || 'Anonymous'
  usernameSet = true
  process.stdout.write('\x1b[32m' + username + '\x1b[0m joined the chat\n')
  process.stdout.write('Connected to peers on topic: ' + TOPIC.toString('hex').slice(0, 16) + '...\n\n')

  const discovery = swarm.join(TOPIC, { client: true, server: true, limit: MAX_PEERS })

  discovery.flushed().then(() => {
    process.stdout.write('\x1b[33mConnected to swarm!\x1b[0m\n')
  }).catch(err => {
    process.stderr.write('Discovery error: ' + err.message + '\n')
  })
})

swarm.on('connection', (conn, info) => {
  conns.add(conn)
  const peerId = conn.remotePublicKey ? conn.remotePublicKey.toString('hex').slice(0, 8) : 'unknown'

  process.stdout.write('\x1b[36m* connected to ' + peerId + ' *\x1b[0m\n')

  conn.on('data', (data) => {
    try {
      const msg = JSON.parse(data.toString())
      process.stdout.write('\x1b[35m<' + msg.username + '>\x1b[0m ' + msg.text + '\n')
    } catch (e) {
      process.stdout.write(data.toString() + '\n')
    }
  })

  conn.on('close', () => {
    conns.delete(conn)
    process.stdout.write('\x1b[31m* disconnected from ' + peerId + ' *\x1b[0m\n')
  })

  conn.on('error', (err) => {
    process.stdout.write('\x1b[31mConnection error: ' + err.message + '\x1b[0m\n')
  })
})

rl.on('line', (line) => {
  const text = line.trim()
  if (!text || !usernameSet) return

  const msg = JSON.stringify({ username, text })

  for (const conn of conns) {
    try {
      conn.write(msg + '\n')
    } catch (e) {
    }
  }

  process.stdout.write('\x1b[90mYou: \x1b[0m' + text + '\n')
})

process.on('SIGINT', () => {
  process.stdout.write('\n\x1b[33mGoodbye!\x1b[0m\n')
  swarm.destroy()
  process.exit(0)
})

process.on('exit', () => {
  swarm.destroy()
})