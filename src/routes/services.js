const router = require('express').Router();
const serviceController = require('../controllers/service-controller');


router.get('/:service/by/:user/params/:number', serviceController.callService);

module.exports = router;

