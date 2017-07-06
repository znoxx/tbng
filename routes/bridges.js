var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  
  
    //stub
    var modes= [];
    var someMode1 = {};
    var someMode2 = {};
    var someMode3 = {};
       

    someMode1.name="none";
    someMode1.current=true;
    
    modes.push(someMode1);
     
    someMode2.name="obfs3";
    someMode2.current=false;
    someMode2.value="obfs3 stub";
    modes.push(someMode2);

    someMode3.name="obfs4";
    someMode3.current=false;
    someMode3.value="obfs4 stub";
    modes.push(someMode3);

 try{
     //interfaces = functions.getObfsModes();  

    res.render('bridge', { title: 'Configure TOR bridges', available_modes: modes, data: "OBFS STUB"  });   
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
    
     var bridges = req.body.data.split('\n');
     var resultData ={};
     resultData.mode=req.body.mode.trim();
     resultData.bridges=[];
     bridges.forEach(function(bridge,i) {
        if(bridge.trim() != "") resultData.bridges.push(bridge.trim()); 
     });
     console.log(JSON.stringify(resultData));
    
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
