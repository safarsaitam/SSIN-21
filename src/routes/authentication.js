const router = require('express').Router();
const authController = require('../controllers/auth-controller');
const hasValidCertificate = require('../middlewares/hasValidCertificate');

router.post('/register', authController.registerUser);
router.post('/login', authController.login);
router.get('/available/username/:username', hasValidCertificate, authController.checkUsernameAvailability);
router.post('/set-username-password', hasValidCertificate, authController.setUsernameAndPassword);

router.get('/messageServer', hasValidCertificate, authController.getMessageServer);
router.post('/messageServer', hasValidCertificate, authController.addMessageServer);

router.post('/whoIs', hasValidCertificate, authController.whoIs);

module.exports = router;
