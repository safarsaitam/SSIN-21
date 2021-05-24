const User = require('../models/user.model');

module.exports = (req, res, next) => {
    User.findOne({ certificate: req.header('authorization') }).then((user) => {
        if (!user) res.status(403).send('Invalid certificate');
        else next();
    });
}