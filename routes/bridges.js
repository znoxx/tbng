var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  
  
    //stub
    var modes= [];
    var someMode1 = {};
       

    someMode1.name="none";
    someMode1.current=true;
    someMode1.value="";
    modes.push(someMode1);
     
//    modes[1].name="obfs3";
//    modes[1].current=false;
 //   modes[1].value="obfs3 stub";

 //   modes[2].name="obfs4";
 //   modes[2].current=false;
 //   modes[2].value="obfs4 stub"
    

 try{
     //interfaces = functions.getObfsModes();  

    res.render('bridge', { title: 'Configure TOR bridges', available_modes: modes  });   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError+"\nLooks error applying tor bridges"});  
  }
 
});

router.post('/', function(req, res, next) {
  console.log(req.body.data);
  console.log(req.body.mode);
  try 
  {
    
     res.render('xresult', { title: 'Configure TOR bridges', message: 'TODO: Implement tor tor bridges' });
    //if ( typeof req.body.interface !== 'undefined' && req.body.interface )
    //{
    //   functions.setDefaultInterface(req.body.interface);
    //   res.render('xresult', { title: 'Operation status', message: 'Attempted to switch to '+req.body.interface });
   // }
    //else
    //{
    //   throw "Cannot use undefined interface";
   // }
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
