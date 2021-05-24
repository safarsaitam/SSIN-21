const User = require('../models/user.model');

exports.squareRoot = async function squareRoot(req, res) { 

    const body = req.body;
    const certificate = req.headers.authorization;

    const user = await User.findOne({
        certificate: certificate
    }); 

    if(user == null) {
        res.status(404).send('Could not find user in database');
        return;
    }

    if (user.security_level < 1) {
        res.status(403).json('You do not have access to this service')
    } else {
        const number = body.number;
        const squareRoot = Math.sqrt(number);
        const result = { squareRoot: squareRoot };

        res.status(200).send(result);
    }
}

exports.cubicRoot = async function cubicRoot(req, res) {

    const body = req.body;
    const certificate = req.headers.authorization;

    const user = await User.findOne({
        certificate: certificate
    }); 

    if(user == null) {
        res.status(404).send('Could not find user in database');
        return;
    }

    if (user.security_level < 2) {
        res.status(403).json('You do not have access to this service')
    } else {
        const number = body.number;
        const cubicRoot = Math.cbrt(number);
        const result = { cubicRoot: cubicRoot };

        res.status(200).send(result);
    }
}

exports.nRoot = async function nRoot(req, res) {

    const body = req.body;
    const certificate = req.headers.authorization;

    const user = await User.findOne({
        certificate: certificate
    }); 

    if(user == null) {
        res.status(404).send('Could not find user in database');
        return;
    }

    if (user.security_level < 3) {
        res.status(403).json('You do not have access to this service')
    } else {
        const number = body.number;
        const index = body.index;
        const nRoot = Math.pow(number, 1/index);
        const result = { nRoot: nRoot };

        res.status(200).send(result);
    }
}