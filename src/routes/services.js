const router = require('express').Router();
const serviceController = require('../controllers/service-controller');
const hasValidCertificate = require('../middlewares/hasValidCertificate');

router.post('/sqrt', hasValidCertificate, serviceController.squareRoot);
router.post('/cbrt', hasValidCertificate, serviceController.cubicRoot);
router.post('/nrt', hasValidCertificate, serviceController.nRoot);

module.exports = router;

