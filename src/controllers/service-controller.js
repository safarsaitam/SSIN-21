const User = require('../models/user.model');

exports.callService = async function callService(req, res) {
    const user = req.param('user');
    const mongoUser = await User.findById(user);

    if (mongoUser.security_level < service) {
        res.status(403).json('You do not have access to this service')
    } else {
        switch (service) {
            case 1:
                squareRoot(req.param('number'), res);
                break;
            default:
                break;
        }
    }



}

function squareRoot(number, res) {

    const squareRoot = Math.sqrt(number);
    const result = { squareRoot: squareRoot };

    res.status(200).send(result);
}