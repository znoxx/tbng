var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

router.get('/', function(req, res, next) {
  var strStatus;
  try
  {
    res.render('i2p', { title: 'Select i2p action'});   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError+"\nReboot the device. If error persists, please fix it via SSH"});  
  }
 
});

router.post('/', function(req, res, next) {
  console.log(req.body.i2p);
  try 
  {
    var result = functions.i2pAction(req.body.i2p);
    res.render('xresult', { title: 'Operation status', message: result });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
