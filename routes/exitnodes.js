var express = require('express');
var functions = require('./lib/functions.js');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  var countries=[];
  
 
 try{
     countries = functions.getCountryList();  
     res.render('exitnodes', { title: 'Exclude TOR exit nodes by country', countries: countries });   
  }
  catch(e)
  {
    var strError = e.toString();
    res.render('xerror', { message: 'Error occured', description: strError});  
  }
 
});

router.post('/', function(req, res, next) {

  countries=[];
  try 
  {
    Object.keys(req.body).forEach(function(value) {
     countries.push(value);
    });
    functions.setExitNodes(countries);
    res.render('xresult', { title: 'Exit nodes excluded', message: countries.length > 0 ? countries.join(","):"none" });
  }
  catch(e)
   {
     var strError = e.toString();
     res.render('xerror', { message: 'Error occured',description: strError}); 
   }
});


module.exports = router;
