var express = require('express');
var router = express.Router();

var functions = require('./lib/functions.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  var wifiInstance=functions.wifi();
  var state=wifiInstance.getIfaceState();
  if (!state.success)
  {
      state.ssid = "Unknown";
      state.power = "Unknown";
      state.connection = "Unknown";   
  }
  console.log(state);
  res.render('wifi', { title: 'WiFi', state: state });
});

/* GET networks. */
router.get('/networks', function(req, res, next) {
  var wifiInstance=functions.wifi();
  var querystring = require('querystring');
  wifiInstance.scanForWiFi( function(err, response) {
    if (err)
    { 
      res.render('xerror', { message: "Error occured", description: error});
    }
    else
    {
      response.networks.forEach(function(entry) {
       var current=entry;
       entry.url=querystring.stringify({ssid: current.ssid,encryption: current.security});
       //console.log(entry.url);
      });
      res.render('wifilist', { title: 'WiFi networks in range', scanned: response });
    }
  });

/* GET connect. */
router.get('/connect', function(req, res, next) {
  var settings=req.query;
  res.render('connect', { title: 'Connect to a network', settings: settings });
});

/* POST connect. */
router.post('/connect', function(req, res, next) {

  console.log(req.body);
  var ssid = req.body.ssid;
  var password = req.body.wifi_password;
  var wifiInstance=functions.wifi();
  var credentials = {};
 
  
  if (password.length != 0)
  {
     credentials = {ssid: ssid, password: password};
  }
  else
  { 
     credentials = {ssid: ssid};
  }


  try
  {
    var result=wifiInstance.connectToAP(credentials,function(err, response) {
      if (err) {
        res.render('xerror', { message: "Error occured", description: err});
      } else {
          if (response.success)
          {
            res.render('xresult', { title: 'Network connection result', message: response.msg });
          }
          else
          {
            res.render('xerror', { message: "Error occured", description: response.msg});
          }
        }
      });
  }
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});

  } 

}); 

}); 


/* GET macspoof. */
router.get('/macspoof', function(req, res, next) {
  res.render('macspoof', { title: 'MAC Spoof', message: 'Press button to randomly change MAC address' });
});
/* POST macspoof. */
router.post('/macspoof', function(req, res, next) {
   
  

  try
  {
     var spoof=functions.MacSpoof();
     res.render('xresult', { title: 'MAC Spoof', message: spoof });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});
   }
});

/* GET wifi reset. */
router.get('/reset', function(req, res, next) {
  res.render('resetfi', { title: 'Reset WiFi', message: 'Press button to reset WiFi adapter' });
});
/* POST wifi reset */
router.post('/reset', function(req, res, next) {
 
  var wifiInstance=functions.wifi()

  try 
  {
    var result=wifiInstance.resetWiFi(function(err, response) {
      if (err) {
        res.render('xerror', { message: "Error occured", description: err});
      } else {
          if (response.success)
          {
            res.render('xresult', { title: 'Reset WiFi', message: response.msg });
          }
          else
          {
            res.render('xerror', { message: "Error occured", description: response.msg});
          }
        }
      });
  }
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});
  }

});





module.exports = router;
