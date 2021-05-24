const User = require('../models/user.model');
const pem = require('pem');

exports.registerUser = async function registerUser(req, res) {

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

                        const certificateLines = keys.certificate.split('\n');

                        let certificate = ''

                        for(let i = 1; i < certificateLines.length - 1; i++) {
                            certificate += certificateLines[i]
                        }

                        res.status(200).json({
                            'certificate': keys.certificate, 
                            'serviceKey': keys.serviceKey,
                        });

                        users[0].certificate = certificate;
                        users[0].save();
                    });
                }
            );
        }
    );
}

exports.addMessageServer = async (req, res) => {
    User.findOne({ certificate: req.header.certificate }).then((user) => {
        user.message_server_address = req.body.ip;
        user.message_server_port = req.body.port;
        user.save();
        res.status(200).send('Added message server');
    })
}

exports.getMessageServer = async (req, res) => {
    User.findOne({ username: req.query.username }).then((user) => {
        if (!user) res.status(400).send('No user found');
        
        res.status(200).json({
            'address': user.message_server_address,
            'port': user.message_server_port,
        });
    }).catch(res.status(500));
}

exports.whoIs = async (req, res) => {
    User.findOne({ certificate: req.body.certificate }).then((user) => {
        if (!user) res.status(400).send('No user found');

        res.status(200).json({
            'username': user.username,
            'full_name': user.full_name,
        });
    }).catch(res.status(500));
}
