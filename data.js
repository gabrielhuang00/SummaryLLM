chrome.runtime.onInstalled.addListener(({reason}) => {
    if (reason === 'install') {
      chrome.tabs.create({
        url: "onboarding.html"
      });
    }
  });
  
chrome.tabs.query({
active: true,
currentWindow: true
}, function(tabs) {
tabURL = tabs[0].url;
const button = document.getElementById("theButton")
const data = document.getElementById("info")
const url = {"url": tabURL};
button.onclick= function(){

fetch("http://127.0.0.1:5000/receiver", 
{
    method: 'POST',
    headers: { 
        'Accept': 'application/json',
        'Content-Type': 'application/json' 
    },
    body:JSON.stringify(url)}).then(res=>{
        if(res.ok){
            return res.json()
        }else{
            alert("something is wrong")
        }
    }).then(jsonResponse=>{
        
        document.getElementById('output').innerHTML = JSON.stringify(jsonResponse)
        console.log(jsonResponse)
        console.log("hello")
    } 
    ).catch((err) => console.error(err));
}

});
  

