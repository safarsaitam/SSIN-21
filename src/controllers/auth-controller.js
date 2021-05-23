const User = require('../models/user.model');

exports.registerUser = async function registerUser(req, res) {

    console.log('hello');

    const body = req.body;
    const username = body.username;
    const oneTimeId = body.oneTimeId;

    let user = await User.find({
        username: username,
        id: oneTimeId 
    });

    if(user == null) {
        res.status(404).send('No pre-register found');
        return;
    }

    user.id = null;
    await user.save();

    console.log('AFTER REGISTER');
    console.log(user);

    res.status(200).send('User successfully registered');

}