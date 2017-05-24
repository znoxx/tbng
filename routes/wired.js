var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('wired', { title: 'Wired network' });
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
