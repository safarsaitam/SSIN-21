const User = require('../models/user.model');
const { nanoid } = require('nanoid');

const idLength = 12;

User.find()
    .then(
        (users) => {
            users.forEach(user => {
                if (user.id === "") {
                    user.id = nanoid(idLength);
                    user.save();
                    // console.log(user);
                }
            })
        }
    )
    .catch(console.error)
