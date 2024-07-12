
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
		        }catch{
		        
		        }
		        content.innerHTML="";
		        for (name in data){
                    let li = document.createElement('li')
                    li.setAttribute('class',"list-group-item list-group-item-action d-flex justify-content-between align-items-start")
                    let d1 = document.createElement('div')
                    d1.setAttribute('class',"ms-2 me-auto")
                    let span = document.createElement('span')
                    span.setAttribute('class',"badge text-bg-primary rounded-pill")
                    span.innerText=data[name]
                    d1.innerText=name
                    li.appendChild(d1)
                    li.appendChild(span)
                    content.appendChild(li)
                }
	        }   
	    }
	    var fdata = new FormData()
	    let val = q_inp.value
	    fdata.append('query',val)
	    xhttp.open("POST","/search",true)
        xhttp.send(fdata);
    },500)
   
}
q_inp.addEventListener("input",()=>{ getData()});

