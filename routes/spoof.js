var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  try
  {

    interfaces = functions.getWanInterfaces();  

    res.render('spoof', { title: 'Select interface to spoof', available_interfaces: interfaces  });   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError+"\nLooks like your WAN interface is not configured at all."});  
  }
 
});

router.post('/', function(req, res, next) {
  console.log(req.body.interface);
  try 
  {
    if ( typeof req.body.interface !== 'undefined' && req.body.interface )
    {
       functions.spoofInterface(req.body.interface);
       res.render('xresult', { title: 'Operation status', message: 'Attempted to spoof '+req.body.interface+'. Check result at System Info page' });
    }
    else
    {
       throw "Cannot use undefined interface";
    }
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
