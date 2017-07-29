var express = require('express');
var router = express.Router();
var functions = require('./lib/functions.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  var wifiInstance=functions.wifi();
  var hasWifi=true;
  if(wifiInstance === null)
  {
    hasWifi=false;
  } 
  res.render('wan', { title: 'WAN configuration',hasWifi: hasWifi  });
});

router.use('/interface',require('./interface'));
router.use('/wifi',require('./wifi'));
router.use('/spoof', require('./spoof'));

module.exports = router;
