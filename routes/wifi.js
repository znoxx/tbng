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
            var connection={}
            connection.ssid="Unknown"
            connection.msg="Not connected"
            connection.mode="Unknown"
            connection.signal_level="Unknown"

            wifiInstance.getCurrentConnections(function(err, currentConnections) {
             if (err) {
             console.log(err);
             }
             else
             {
                if(currentConnections.length)
                {
                   connection.msg="Connected"
                   connection.ssid=currentConnections[0].ssid
                   connection.mode=currentConnections[0].mode
                   connection.signal_level=currentConnections[0].signal_level
                }
             }
            res.render('wifi', { title: 'WiFi', connection: connection });
            console.log(currentConnections);
           });

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

         wifiInstance
           .scan()
           .then(function(networks) {
             var response={}
             response.msg="Scan results"
             response.networks=networks
             response.networks = response.networks.filter((network, index, self) => self.findIndex(t => t.ssid === network.ssid && t.security === network.security) === index);
             response.networks.forEach(function(entry) {
                var current=entry;
                entry.url=querystring.stringify({ssid: current.ssid,encryption: current.security});
                });
                res.render('wifilist', { title: 'WiFi networks in range', scanned: response });
           })
           .catch(function(error) {
            var strError = error.toString();
            res.render('xerror', { message: "Error occured", description: strError});
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
       credentials = {ssid: ssid, password: ""};
    }

    wifiInstance.connect(credentials, function(err) {
      if (err) {
         console.log(err);
         res.render('xerror', { message: "Error occured", description: err});
      } else {
       res.render('xresult', { title: 'Network connection result', message: "Connected" });
       console.log("Connected");
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

       
       wifiInstance.disconnect(function(err) {
         if (err) {
          console.log(err)
          res.render('xerror', { message: "Error occured", description: err});
         }
         else {
           res.render('xresult', { title: 'Reset WiFi', message: "Disconnected" });
           console.log("Disconnected") 
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
