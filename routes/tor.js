var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('tor', { title: 'TOR configuration' });
});

/* GET restart. */
router.get('/restart', function(req, res, next) {
  res.render('restarttor', { title: 'Restart TOR', message: 'Press button to restart TOR' });
});
/* POST reboot. */
router.post('/restart', function(req, res, next) {
  try 
  {
    res.render('xresult', { title: 'Restart TOR', message: 'TODO: Implement tor restart' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
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
    res.render('xresult', { title: 'Reset TOR', message: 'TODO: Implement tor reset' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});


module.exports = router;
