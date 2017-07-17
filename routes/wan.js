var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('wan', { title: 'WAN configuration' });
});

router.use('/interface',require('./interface'));
router.use('/wifi',require('./wifi'));
router.use('/spoof', require('./spoof'));

module.exports = router;
