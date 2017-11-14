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

/* GET DNSMasq restart. */
router.get('/dnsmasq', function(req, res, next) {
  try
  {
    res.render('dnsmasq', { title: 'Restart dnsmasq', message: 'Press button to restart dnsmasq service' });
  }
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});
  } 
});
/* POST dnsmasq restart */
router.post('/dnsmasq', function(req, res, next) {
 try 
  {
    var result = functions.restartDNSMasq();
    res.render('xresult', { title: 'Operation status', message: result });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }

});


module.exports = router;
