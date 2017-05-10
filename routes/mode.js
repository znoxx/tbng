var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  try
  {
    strStatus = functions.readStatus();
    res.render('mode', { title: 'Select operation mode', status: strStatus });   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError+"\nReboot the device. If error persists, please fix it via SSH"});  
  }
 
});

router.post('/', function(req, res, next) {
  console.log(req.body.mode);
  try 
  {
    var result = functions.switchMode(req.body.mode);
    res.render('xresult', { title: 'Operation status', message: 'Current operation mode is '+req.body.mode });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
