
q_inp=document.querySelector('#query')
content=document.querySelector("#content")

function getData(){
    setTimeout(()=>{
        let data;
	    let xhttp = new XMLHttpRequest();
	    xhttp.onreadystatechange = (state)=>{
	        if (state.target.readyState==4 && state.target.status==200){
	             try{
		            data=JSON.parse(xhttp.responseText)
		            console.log(data)
		        }catch{
		        
		        }
		        content.innerHTML="";
		        if (JSON.stringify(data)=='{}'){
		            let li = document.createElement('li')
                    let a = document.createElement('a')
                    a.setAttribute('href',`#`)
                    //li.setAttribute('class',"list-group-item list-group-item-action d-flex justify-content-between align-items-start")
                    a.setAttribute('class',"list-group-item")
                    let d1 = document.createElement('div')
                    d1.setAttribute('class',"flex")
                    d1.innerText='Not found'
                    a.appendChild(d1)
                    content.appendChild(a)
                    return 
		        }
		        for (name in data){
                    let li = document.createElement('li')
                    let a = document.createElement('a')
                    a.setAttribute('href',`/view?n=${name}`)
                    //li.setAttribute('class',"list-group-item list-group-item-action d-flex justify-content-between align-items-start")
                    a.setAttribute('class',"list-group-item")
                    let d1 = document.createElement('div')
                    d1.setAttribute('class',"flex")
                    let span = document.createElement('span')
                    let span2 = document.createElement('span')
                    span.setAttribute('class',"badge text-bg-primary rounded-pill")
                    span.innerText=`in ${data[name][0]}`
                    span2.innerText=`Subject: ${data[name][1]}`
                    d1.innerText=name
                    d1.appendChild(span)
                    a.appendChild(d1)
                    a.appendChild(span2)
                    content.appendChild(a)
                }
	        }   
	    }
	    var fdata = new FormData()
	    let val = q_inp.value
	    fdata.append('query',val)
	    xhttp.open("POST","/search",true)
	    if (val==""){
	        content.innerHTML=""
	        return
	    }
       xhttp.send(fdata);
    },500)
   
}
q_inp.addEventListener("input",()=>{ getData()});

