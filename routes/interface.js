var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  try
  {
    //stub
    interfaces= {};

    interfaces[0]={
      name: "wlan1",
      current: false
     }

     
    interfaces[1]={
      name: "bond0",
      current: true
    }


     interfaces = functions.getWanInterfaces();  

    res.render('interface', { title: 'Select WAN interface', available_interfaces: interfaces  });   
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
       functions.setDefaultInterface(req.body.interface);
       res.render('xresult', { title: 'Operation status', message: 'Attempted to switch to '+req.body.interface });
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
