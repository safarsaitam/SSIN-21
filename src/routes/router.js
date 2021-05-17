const router = require('express').Router();

router.use('/', (req, res) => res.sendFile('../test_html.html', {root: __dirname }));

module.exports = router;