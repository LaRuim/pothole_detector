const express = require('express')
const server = express()
const port = 3002

server.get('/', (req, res) => res.send('Hello World!'))

server.listen(port)