const router = require('express').Router();
const serviceController = require('../controllers/service-controller');


router.post('/sqrt', serviceController.squareRoot);
router.post('/cbrt', serviceController.cubicRoot);
router.post('/nrt', serviceController.nRoot);

module.exports = router;

