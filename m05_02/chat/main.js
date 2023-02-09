console.log('Running...')

const ws = new WebSocket('ws://127.0.0.1:8080')

ws.onopen = () => {
    console.log('WebSocket connect')
}

formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data
    const elForMsg = document.createElement('div')
    elForMsg.textContent = text
    subscribe.appendChild(elForMsg)
}