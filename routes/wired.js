var express = require('express');
var router = express.Router();
var functions = require('./lib/functions.js');
/* GET home page. */
router.get('/', function(req, res, next) {

  var strStatus;
  try
  {

    interfaces = functions.getWanInterfaces();
    bHasWired=false;
    interfaces.forEach(function(interface){
       if (interface.wireless==false) {
         bHasWired=true;
       }
    });

    if (bHasWired == false)
    {
        throw new Error("No wired interfaces configured.");
    }
    
    res.render('wired', { title: 'Wired network' });
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError});
  }


});

/* GET macspoof. */
router.get('/macspoof', function(req, res, next) {
  res.render('wiredspoof', { title: 'Spoof wired MAC', message: 'Press button to randomly change wired MAC address' });
});
/* POST reboot. */
router.post('/macspoof', function(req, res, next) {
  try 
  {
    res.render('xresult', { title: 'Spoof wired MAC', message: 'TODO: Implement wired MAC spoof' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});

module.exports = router;
