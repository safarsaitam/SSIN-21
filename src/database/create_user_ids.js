const User = require('../models/user.model');
const { customAlphabet } = require('nanoid');

const alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'; 
const idLength = 12;

User.find()
    .then(
        (users) => {
            users.forEach(user => {
                if (user.id === '') {
                    id = customAlphabet(alphabet, idLength);
                    user.id = id();
                    user.save();
                    console.log(user);
                }
            })
        }
    )
    .catch(console.error)

