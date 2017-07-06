var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var strStatus;
  
 

 try{
     modes = functions.getObfsModes();  
     obfs_data = "";
     modes.forEach(function(mode){
       if (mode.current && mode.name!="none")
       {
          obfs_data = mode.bridges.join("\n")
       }
     });
     res.render('bridge', { title: 'Configure TOR bridges', available_modes: modes, data: obfs_data  });   
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
     if(req.body.mode != "none")
     {
       bridges.forEach(function(bridge,i) {
          if(bridge.trim() != "") resultData.bridges.push(bridge.trim()); 
       });
     }
     functions.setObfsMode(resultData);
     res.render('xresult', { title: 'Bridge applied', message: "Bridge mode is "+resultData.mode+". Don't forget to switch to TOR mode" });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
