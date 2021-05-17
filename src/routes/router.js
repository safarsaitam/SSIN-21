const router = require('express').Router();

router.use('/', (req, res) => {
    res.status(200).json("Boas");
});

module.exports = router;