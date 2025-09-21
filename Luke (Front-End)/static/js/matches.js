var username ="bing"
var part1="None"
var str="None"
window.addEventListener('load',setup)
mySkills=[]
function setup(){
    fetch('/calculate_matches')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
            console.log(data); // Do something with the data
        })
            .catch(error => {
              console.error('Error fetching data:', error);
    });


}