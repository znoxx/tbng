var express = require('express');
var functions = require('./lib/functions.js'); 
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('tor', { title: 'TOR configuration' });
});

/* GET restart. */
router.get('/restart', function(req, res, next) {
  var strStatus;
  try
  {
    res.render('restarttor', { title: 'Select TOR action', message: 'Warning! Stopping TOR will cause functionality loss and will automatically switch device to DIRECT mode.'});   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError+"\nReboot the device. If error persists, please fix it via SSH"});  
  }
 
});
/* POST restart. */
router.post('/restart', function(req, res, next) {
  console.log(req.body.tor);
  try 
  {
    var result = functions.torAction(req.body.tor);
    res.render('xresult', { title: 'Operation status', message: result });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


/* GET reset. */
  router.get('/reset', function(req, res, next) {
  res.render('resettor', { title: 'Reset TOR', message: 'Press button to reset TOR configuration' });
});
/* POST reset. */
router.post('/reset', function(req, res, next) {
  try 
  {
    functions.resetTOR();
    res.render('xresult', { title: 'Reset TOR', message: 'Removed generated bridge and country settings.' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});


router.use('/bridge', require('./bridges'));
router.use('/exitnodes', require('./exitnodes'));
module.exports = router;
