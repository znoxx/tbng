var express = require('express');
var router = express.Router();

var functions = require('./lib/functions.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('system', { title: 'System' });
});
/* GET password change. */
router.get('/access', function(req, res, next) {
  res.render('access', { title: 'Change password', message: 'Enter current password, new password and confirmation' });
});
/* POST password change. */
router.post('/access', function(req, res, next) {
  try 
  {
    var result = functions.changePassword(req.body.current_password, req.body.new_password,req.body.confirm_password);
    res.render('xresult', { title: 'Password successfully changed', message: 'Reboot device to take effect' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});

/* GET reboot. */
router.get('/reboot', function(req, res, next) {
  res.render('reboot', { title: 'Reboot system', message: 'Press button to reboot system' });
});
/* POST reboot. */
router.post('/reboot', function(req, res, next) {
  try 
  {
    setInterval(function(){
       functions.reboot();
     },10000);
    res.render('xresult', { title: 'Reboot', message: 'Reboot in progress...' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});


/* GET shutdown. */
router.get('/shutdown', function(req, res, next) {
  res.render('shutdown', { title: 'Shutdown system', message: 'Press button to shutdown system' });
});
/* POST shutdown. */
router.post('/shutdown', function(req, res, next) {
  try 
  {
    setInterval(function(){
       functions.shutdown();
    },10000);
    res.render('xresult', { title: 'Shutdown', message: 'Shutdown in progress...' });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError}); 
   }
});

/* GET sysinfo. */
router.get('/info', function(req, res, next) {
    res.render('info', { title: 'System info', sysinfo: functions.sysInfo() });
});



module.exports = router;
