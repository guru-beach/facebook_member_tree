/* Grabs member data from facebook's member page and outputs
 * returns a dictionary { "member_name" : "adder" : <adder>, "timestamp" : <timestamp> }
 * {"Jake Lundberg":{"adder":"Added by Lucas Lundberg over a year ago","timestamp":"Monday, September 15, 2014 at 9:18am"}}
 * This outputs to a new web page, so you may get a message about popups, just allow this one popup
 *
 *
 * Facebook will output a warning message when you open up the console, don't worry, this code
 * will not take over your computer.
 * 
 * SAVE THE OUTPUT TO <sbg_tree_path>/members.json
 *
 *
 */

var member_obj = document.getElementsByClassName("_6a _5u5j _6b");
var members = {};
for (i=0; i < member_obj.length; i++) {
  var name = member_obj[i].getElementsByClassName("fsl fwb fcb")[0].innerText;
  var adder = member_obj[i].getElementsByClassName("fsm fwn fcg")[0].innerText.split('\n')[1];
  var timestamp = member_obj[i].getElementsByClassName("timestamp")[0].title;
  members[name] = { 'adder' : adder, 'timestamp' : timestamp };
}

var url = 'data:text/json;charset=utf8,' + JSON.stringify(members);
window.open(url, '_blank');
window.focus();
