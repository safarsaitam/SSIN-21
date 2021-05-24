const router = require('express').Router();
const authController = require('../controllers/auth-controller');

router.post('/register', authController.registerUser);

router.get('/messageServer', authController.getMessageServer);
router.post('/messageServer', authController.addMessageServer);

module.exports = router;

