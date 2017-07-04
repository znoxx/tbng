var express = require('express');
var functions = require('./lib/functions.js'); 
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('tor', { title: 'TOR configuration' });
});

/* GET restart. */
router.get('/restart', function(req, res, next) {
  res.render('restarttor', { title: 'Restart TOR', message: 'Press button to restart TOR' });
});
/* POST restart. */
router.post('/restart', function(req, res, next) {
  try
    {
      var result = functions.tor_restart();
      res.render('xresult', { title: 'Operation status', message: result });
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


router.use('/bridge', require('./bridges'));

module.exports = router;
