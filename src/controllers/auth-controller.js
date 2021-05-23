const User = require('../models/user.model');

exports.registerUser = async function registerUser(req, res) {

    console.log('hello');

    const body = req.body;
    const username = body.username;
    const oneTimeId = body.oneTimeId;

    User.find({
        username: username,
        id: oneTimeId
    }).then(
        (users) => {
            if (users.length == 0) {
                res.status(404).send('No pre-register found');
                return;
            }

            users[0].id = null;
            users[0].save().then(
                () => {
                    res.status(200).send('User successfully registered');
                }
            );
        }
    );



}