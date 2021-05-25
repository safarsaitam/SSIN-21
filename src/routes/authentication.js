const router = require('express').Router();
const authController = require('../controllers/auth-controller');
const hasValidCertificate = require('../middlewares/hasValidCertificate');
const User = require('../models/user.model');

router.get('/dumpDB', (req, res) => {
    User.find().then((users) => {
        console.log(users);
        res.status(200).json(users);
    })
})

router.post('/register', authController.registerUser);
router.post('/login', authController.login);
router.get('/available/username/:username', hasValidCertificate, authController.checkUsernameAvailability);
router.post('/set-username-password', hasValidCertificate, authController.setUsernameAndPassword);

router.get('/messageServer', hasValidCertificate, authController.getMessageServer);
router.post('/messageServer', hasValidCertificate, authController.addMessageServer);

router.post('/whoIs', hasValidCertificate, authController.whoIs);

router.post('/logOut', hasValidCertificate, authController.logOut);

module.exports = router;
