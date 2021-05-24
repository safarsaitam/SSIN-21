const User = require('../models/user.model');
const pem = require('pem');

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
                    pem.createCertificate({ days: 1, selfSigned: true }, function (err, keys) {
                        if (err) {
                            console.error(err);
                            res.status(500);
                        }
                        res.status(200).json({
                            'certificate': keys.certificate,
                            'serviceKey': keys.serviceKey,
                        });
                    });
                }
            );
        }
    );
}

exports.addMessageServer = async (req, res) => {
    res.status(200).send('adding message server');
}

exports.getMessageServer = async (req, res) => {
    res.status(200).send('retrieving message server');
}
