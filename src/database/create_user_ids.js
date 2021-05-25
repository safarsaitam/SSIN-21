const User = require('../models/user.model');
const { customAlphabet } = require('nanoid');

const alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'; 
const idLength = 12;

exports.GenerateForEveryUser = () => {
    User.find()
        .then(
            (users) => {
                users.forEach(user => {
                        id = customAlphabet(alphabet, idLength);
                        user.id = id();
                        user.save();
                        console.log(user);
                })
            }
            )
            .catch(console.error)
}

exports.GenerateForUser = (username) => {
    User.findOne({username: username})
        .then(
            (user) => {
                if (!user) {
                    console.log("No user found");
                    return;
                }
                id = customAlphabet(alphabet, idLength);
                user.id = id();
                user.save();
                console.log(user);
            }
        )
        .catch(console.error)
}

