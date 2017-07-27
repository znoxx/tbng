var express = require('express');
var router = express.Router();

var no_wifi_interface="Wireles interface not configured. Configure one manually at config/tbng.json";

var functions = require('./lib/functions.js');

/* GET home page. */
router.get('/', function(req, res, next) {
  try 
  {
      var wifiInstance=functions.wifi();
	  if(wifiInstance === null)
	  {
		  throw Error(no_wifi_interface);
	  }
	  else
	  {
	   
		var state=wifiInstance.getIfaceState();
		if (!state.success)
		{
			state.ssid = "Unknown";
			state.power = "Unknown";
			state.connection = "Unknown";   
		}
		console.log(state);
		res.render('wifi', { title: 'WiFi', state: state });
	  }
  }
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});

  } 
});

/* GET networks. */
router.get('/networks', function(req, res, next) {

  try
    {
	  var wifiInstance=functions.wifi();
      if(wifiInstance === null)
	  {
		  throw Error(no_wifi_interface);
	  }
	  var querystring = require('querystring');
	  wifiInstance.scanForWiFi( function(err, response) {
		if (err)
		{ 
		  res.render('xerror', { message: "Error occured", description: error});
		}
		else
		{
                  response.networks = response.networks.filter((network, index, self) => self.findIndex(t => t.ssid === network.ssid && t.security === network.security) === index);
		  response.msg=response.msg.replace(/\s\(\d+\sfound\)/g,"");
                   response.networks.forEach(function(entry) {
		   var current=entry;
		   entry.url=querystring.stringify({ssid: current.ssid,encryption: current.security});
		   //console.log(entry.url);
		  });
		  res.render('wifilist', { title: 'WiFi networks in range', scanned: response });
		}
	  });
	}
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});

  } 
  });

/* GET connect. */
router.get('/connect', function(req, res, next) {
 
  try 
  {
	var settings=req.query;
	var wifiInstance=functions.wifi();
    if(wifiInstance === null)
	{
      throw Error(no_wifi_interface);
	}
	  
    res.render('connect', { title: 'Connect to a network', settings: settings });
  }
  catch(e)
  {
	 var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});
  }
});

/* POST connect. */
router.post('/connect', function(req, res, next) {

  try
  {
	var wifiInstance=functions.wifi();
	if(wifiInstance === null)
	{
		  throw Error(no_wifi_interface);
	}
	console.log(req.body);
    var ssid = req.body.ssid;
    var password = req.body.wifi_password;
  
    var credentials = {};
 
  
    if (password.length != 0)
    {
       credentials = {ssid: ssid, password: password};
    }
    else
    { 
       credentials = {ssid: ssid};
    }

    var result=wifiInstance.connectToAP(credentials,function(err, response) {
      if (err) 
	  {
        res.render('xerror', { message: "Error occured", description: err});
      } 
	  else 
	  {
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



/* GET wifi reset. */
router.get('/reset', function(req, res, next) {
  try
  {
	var wifiInstance=functions.wifi();
	if(wifiInstance === null)
	{
		  throw Error(no_wifi_interface);
	}
    res.render('resetfi', { title: 'Reset WiFi', message: 'Press button to reset WiFi adapter' });
  }
  catch(e)
  {
     var strError = e.toString();
     res.render('xerror', { message: "Error occured", description: strError});
  } 
});
/* POST wifi reset */
router.post('/reset', function(req, res, next) {
  try 
  {
	var wifiInstance=functions.wifi();
	if(wifiInstance === null)
	{
		  throw Error(no_wifi_interface);
	} 
	
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
