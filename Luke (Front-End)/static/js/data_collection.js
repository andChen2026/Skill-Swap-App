var username ="bing"
var part1="None"
var str="None"
window.addEventListener('load',setup)
mySkills=[]
function setup(){
    
    /*document.getElementById('get_match_results').addEventListener('click', function(){
        fetch('/process_value', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ value: arrAsString }) // Send as JSON
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    })*/
    $(document).ready (dropdown());

    //jquery dropdown test
    function dropdown(){
        $('select').autocompleteDropdown({

        // placeholder for the search field
        customPlaceholderText: "Search...",

        // default CSS classes
        wrapperClass: 'autocomplete-dropdown',
        inputClass: 'acdd-input',

        // allows additions to the select field
        allowAdditions: true,

        // text to show when no results
        noResultsText: 'No results found',

        // callbacks
        onChange: function() {
            window.console.log('select has changed');
        },
        onSelect: function() {
            window.console.log('an option has been selected');
        },
        })
    };
    /*$('select').autocompleteDropdown({

        // placeholder for the search field
        customPlaceholderText: "Search...",

        // default CSS classes
        wrapperClass: 'autocomplete-dropdown',
        inputClass: 'acdd-input',

        // allows additions to the select field
        allowAdditions: true,

        // text to show when no results
        noResultsText: 'No results found',

        // callbacks
        onChange: function() {
            window.console.log('select has changed');
        },
        onSelect: function() {
            window.console.log('an option has been selected');
        },
  
    })*/
   document.getElementById("suggestions").addEventListener('change', function(event){
        console.log(document.getElementById("suggestions").value)
   })
    document.getElementById('add_skill_button').addEventListener('click', function(){
        const listDiv=document.getElementById('mySkillList');
        newListItem=document.createElement('ul');
        skillText=document.getElementById('skills_bar').value;
        document.getElementById('skills_bar').value=""
        newListItem.innerHTML=skillText;
        newListItem.id=listDiv.childElementCount+1

        deleteButton=document.createElement('button')
        deleteButton.id="added_skill"+newListItem.id
        deleteButton.className="delete"
        deleteButton.innerHTML="Delete"
        newListItem.appendChild(deleteButton)
        listDiv.appendChild(newListItem)
        deleteButton.addEventListener('click', function(event){
            deleteID=event.target.id
            console.log(deleteID)
            ulToDelete=document.getElementById(deleteID).parentNode;
            listDiv.removeChild(ulToDelete)
        })
    })

    document.getElementById('add_needed_skill_button').addEventListener('click', function(){
        const listDiv=document.getElementById('myNeededSkillList');
        newListItem=document.createElement('ul');
        skillText=document.getElementById('needed_skills_bar').value;
        document.getElementById('needed_skills_bar').value=""
        newListItem.innerHTML=skillText;
        newListItem.id=listDiv.childElementCount+1

        deleteButton=document.createElement('button')
        deleteButton.id="added_needed_skill"+newListItem.id
        deleteButton.className="delete"
        deleteButton.innerHTML="Delete"
        newListItem.appendChild(deleteButton)
        listDiv.appendChild(newListItem)
        deleteButton.addEventListener('click', function(event){
            deleteID=event.target.id
            console.log(deleteID)
            ulToDelete=document.getElementById(deleteID).parentNode;
            listDiv.removeChild(ulToDelete)
        })
    })

    

    
    //get and display user's location
    getLocation;

    //schedule availability selection
    $('#example').scheduler();
    $('#example').scheduler({
        data: {
            2: [0,1,2,3,4,5],
            3: [10,11,12,13],
            4: [10,11,12,13]
        }
    });
    $('#example').scheduler({
        accuracy: 1
    });
    $('#example').scheduler({
        footer: true
    });
    $('#example').scheduler({
        multiple: false
    });
    $('#example').scheduler({
        disabled: true
    });
    $('#example').scheduler({
        // parameter: selected
        onDragStart: $.noop,
        onDragMove: $.noop,
        onDragEnd: $.noop,
        onSelect: $.noop,
        onRender: $.noop
    });
    // set
    //$('#example').scheduler('val', {1: [1,2,3,5], 2:[2]});

    // get
    $('#example').scheduler('val');

    $.fn.scheduler.locales['lanuage'] = {
        AM: 'Your String',
        PM: 'Your String',
        TIME_TITLE: 'Your String',
        WEEK_TITLE: 'Your String',
        WEEK_DAYS: ['Your String', 'Your String', 'Your String', 'Your String', 'Your String', 'Your String', 'Your String']
    };

    $('#example').scheduler({
        locale: 'language'
    });

    var data = {1: [1,2,3]};
    str = $.fn.scheduler.util.serialize(data);
    console.log(str)
    // => {1: [1,2,3]}

    $.fn.scheduler.util.parse(str);
    //serialToCalendar()

    username=window.location.href.substring(14)
    console.log("username="+username)

    whiteElements=document.getElementsByClassName("scheduler-hour")
    console.log(whiteElements)
    greenElements=document.getElementsByClassName("scheduler-hour.schedule-active")
    console.log(greenElements)
    //Gemini
    /*document.addEventListener('DOMContentLoaded', () => {
            fetch('/process_value')
                console.log("loaded")
                .then(response => response.json())
                .then(data => {
                    //const dynamicJsVariable = data.data;
                    document.getElementById('result').innerText = data.Schedule
                })
                .catch(error => console.error('Error fetching data:', error));
        });*/
        fetch('/process_value')
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
            console.log(data); // Do something with the data
            serialToCalendar(data.Schedule)
            console.log("myskills="+data.MySkills)
            mySkillsStringToPageSkills(data.MySkills)
            myNeededSkillsStringtoPageNeededSkills(data.MyNeededSkills)
            console.log("myneededskills="+data.MyNeededSkills)
        })
            .catch(error => {
              console.error('Error fetching data:', error);
        });

    //Gemini
    document.getElementById('submit_profile_data').addEventListener('click', function() {
        console.log('clicked')
        //const buttonValue = this.dataset.value; // Get value from data-attribute
        //const whiteBoxes=document.getElementsByClassName('scheduler-hour')
        //const serializedArr=[]
        /*for (let i=0; i<whiteBoxes.length; i++){
            serializedArr[7*whiteBoxes[i].getAttribute('data-row')+whiteBoxes[i].getAttribute('data-col')]=0
        }
        const greenBoxes=document.getElementsByClassName('scheduler-hour scheduler-active')
        for (let i=0; i<greenBoxes.length; i++){
            serializedArr[7*greenBoxes[i].getAttribute('data-row')+greenBoxes[i].getAttribute('data-col')]=1
        }*/
       const boxes=document.getElementsByClassName('scheduler-hour')
       /*for(let i=0; i<7; i++){
            for(let j=0; j<24; j++){
                let computedBackgroundColor = window.getComputedStyle(boxes[24*i+j]).getPropertyValue('background-color')
                console.log(computedBackgroundColor);
                if(computedBackgroundColor=="rgb(135, 189, 65)"){
                    serializedArr[24*i+j]=1
                    console.log(serializedArr[24*i+j])
                }
                else{
                    serializedArr[24*i+j]=0
                    console.log(serializedArr[24*i+j])
                }

                
                
            }
       }
      
        console.log(serializedArr)
        arrAsString=serializedArr.join('');
        console.log(arrAsString)*/

        let arrAsString=calendarToSerial();
        let mySkills=pageSkillsToSkillsString();
        let myNeededSkills=pageNeededSkillsToNeededSkillsString();
        console.log(myNeededSkills)

        fetch('/process_value', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ schedule: arrAsString, mySkills: mySkills, myNeededSkills: myNeededSkills}) // Send as JSON
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    console.log(part1)
      // Perform actions on each element, e.g., log its content
}
    //elements=document.getElementsByClassName(
function serialToCalendar(serial){
    serialString=serial.toString()
    //$('#example').scheduler('val', {1: [1,2,3,5], 2:[2]});
    dict={};
    for(let i=1; i<8; i++){
        tuple=[];
        for(let j=0; j<24; j++){
            if(serialString.charAt(24*(i-1)+j)=='1'){
                tuple.push(j)
            }
        }
        if(tuple.length!=0) dict[i]=tuple;
    }
    $('#example').scheduler('val', dict);
    /*console.log("executing method")
    const boxes=document.getElementsByClassName('scheduler-hour')
    serialString=serial.toString()
    for(let i=0; i<7; i++){
        for(let j=0; j<24; j++){
            
            if(serialString.charAt(24*i+j)=='1'){
                boxes[24*i+j].style.backgroundColor='#87bd41'
            }
            else{
                boxes[24*i+j].style.backgroundColor='#ffffff'
            }
        }
    }*/
}
function pageSkillsToSkillsString(){
    const pageSkillsDiv=document.getElementById("mySkillList")
    console.log(pageSkillsDiv.childElementCount)
    skillsString=""
   for(const child of pageSkillsDiv.children){
        //console.log(child.tagName)
        console.log(child.innerHTML.split("<")[0]);
        if(skillsString.length!=0) skillsString=skillsString+",";
        skillsString=skillsString+child.innerHTML.split("<")[0]
   }
   return skillsString;

}
function mySkillsStringToPageSkills(mySkillsString){
    if(mySkillsString!=null){
        mySkillsArr=mySkillsString.split(",")
        const pageSkillsDiv=document.getElementById("mySkillList")
        for(i=0; i<mySkillsArr.length; i++){
            newListItem=document.createElement('ul');
            skillText=mySkillsArr[i];
            //document.getElementById('needed_skills_bar').value=""
            newListItem.innerHTML=skillText;
            newListItem.id=pageSkillsDiv.childElementCount+1

            deleteButton=document.createElement('button')
            deleteButton.id="added_skill"+newListItem.id
            deleteButton.className="delete"
            deleteButton.innerHTML="Delete"
            newListItem.appendChild(deleteButton)
            pageSkillsDiv.appendChild(newListItem)
            deleteButton.addEventListener('click', function(event){
                deleteID=event.target.id
                console.log(deleteID)
                ulToDelete=document.getElementById(deleteID).parentNode;
                pageSkillsDiv.removeChild(ulToDelete)
            })
        }
    }
    
}

function pageNeededSkillsToNeededSkillsString(){
    const pageNeededSkillsDiv=document.getElementById("myNeededSkillList")
    neededSkillsString=""
   for(const child of pageNeededSkillsDiv.children){
        //console.log(child.tagName)
        console.log(child.innerHTML.split("<")[0]);
        if(neededSkillsString.length!=0) neededSkillsString=neededSkillsString+",";
        neededSkillsString=neededSkillsString+child.innerHTML.split("<")[0]
   }
   return neededSkillsString;
}

function myNeededSkillsStringtoPageNeededSkills(neededSkillsString){
    console.log("executing!!!")
    if(neededSkillsString!=null){
        console.log("not null")
        neededSkillsArr=neededSkillsString.split(",")
        const pageNeededSkillsDiv=document.getElementById("myNeededSkillList")
        for(i=0; i<neededSkillsArr.length; i++){
            newListItem=document.createElement('ul');
            skillText=neededSkillsArr[i];
            //document.getElementById('needed_skills_bar').value=""
            newListItem.innerHTML=skillText;
            newListItem.id=pageNeededSkillsDiv.childElementCount+1

            deleteButton=document.createElement('button')
            deleteButton.id="added_needed_skill"+newListItem.id
            deleteButton.className="delete"
            deleteButton.innerHTML="Delete"
            newListItem.appendChild(deleteButton)
            pageNeededSkillsDiv.appendChild(newListItem)
            deleteButton.addEventListener('click', function(event){
                deleteID=event.target.id
                console.log("parent="+document.getElementById(deleteID).parentNode)
                console.log(deleteID)
                ulToDelete=document.getElementById(deleteID).parentNode;
                pageNeededSkillsDiv.removeChild(ulToDelete)
            })
        }
    }
}
function calendarToSerial(){
    const serializedArr=[]
    const boxes=document.getElementsByClassName('scheduler-hour')
       for(let i=0; i<7; i++){
            for(let j=0; j<24; j++){
                let computedBackgroundColor = window.getComputedStyle(boxes[24*i+j]).getPropertyValue('background-color')
                if(computedBackgroundColor=="rgb(135, 189, 65)"){
                    serializedArr[24*i+j]=1
 
                }
                else{
                    serializedArr[24*i+j]=0
                }

                
                
            }
       }
        console.log(serializedArr)
        arrAsString=serializedArr.join('');
        console.log(arrAsString)
    return arrAsString;
}
//from sitelint.com
function getRealBackgroundColor(element) {
  const rootElement = element || document.documentElement;
  const originalBackgroundColor = window.getComputedStyle(rootElement)?.getPropertyValue("background-color");

  rootElement.style.setProperty("background-color", "Window");

  const realColor = window.getComputedStyle(rootElement)?.getPropertyValue("background-color");

  if (typeof originalBackgroundColor === "string") {
    rootElement.style.setProperty("background-color", originalBackgroundColor);
  }

  if (realColor === undefined) {
    return "rgba(0, 0, 0, 0)";
  }

  return realColor;
}

function getLocation(){
    console.log(document.getElementById("location").innerHTML)
    document.getElementById("location").innerHTML="executing method"
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition)
    }
    else{
        document.getElementById("location").innerHTML="Location disabled."
    }
}

function showPosition(position){
    document.getElementById("location").innerHTML=position.coords.latitude+" "+position.coords.longitude;
}


