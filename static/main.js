
let q_inp=document.querySelector('#query')
let content=document.querySelector("#content")
let modal = document.querySelector('#popup')
let closeBtn = document.querySelector('#close')
let modal_title=document.querySelector('#modal-title')
let table=document.querySelector('#table')


closeBtn.addEventListener('click',()=>closeModal())
function openModal(data){
    modal.classList.add('active')
    modal_title.innerText=`Timetable for ${data}`
    let xhttp = new XMLHttpRequest();
    let rec_data,response;
    xhttp.onreadystatechange = (state)=>{
        if (state.target.readyState==4 && state.target.status==200){
             try{
                response=JSON.parse(xhttp.responseText)
                table.innerHTML="<th><tr><td>Zero</td><td>First</td><td>Second</td><td>Third</td><td>Fourth</td><td>Recess</td><td>Fifth</td><td>Sixth</td><td>Seventh</td><td>Eighth</td> </tr></th>"
                rec_data = response["data"]
            }catch{
            }
            for (let i = 0; i < 6; i++) {
                let tr = document.createElement('tr')
                if (i==response["day"]){
                    tr.setAttribute('class','active')
                }
                for (let j = 0; j < rec_data[i].length; j++) {
                    let td = document.createElement('td')
                    if (j==response["period"]){
                        td.setAttribute('class','active')
                    }
                    console.log(rec_data[i][j])
                    td.innerText=rec_data[i][j]
                    tr.appendChild(td)
                }
                table.appendChild(tr)
            }
        }   
    }
    var fdata = new FormData()
    fdata.append('n',data)
    xhttp.open("POST","/view",false)
    xhttp.send(fdata);

}
function closeModal(){
    modal.classList.remove('active')
}

function getData(){
    setTimeout(()=>{
        let data;
	    let xhttp = new XMLHttpRequest();
	    xhttp.onreadystatechange = (state)=>{
	        if (state.target.readyState==4 && state.target.status==200){
	             try{
		            data=JSON.parse(xhttp.responseText)
		            //console.log(data)
		        }catch{
		        
		        }
		        content.innerHTML="";
		        if (JSON.stringify(data)=='{}'){
		            let li = document.createElement('li')
                    let a = document.createElement('a')
                    a.setAttribute('class',"list-group-item")
                    let d1 = document.createElement('div')
                    d1.setAttribute('class',"flex")
                    d1.innerText='Not found'
                    a.appendChild(d1)
                    content.appendChild(a)
                    return 
		        }
		        for (f_name in data){
                    let li = document.createElement('li')
                    let a = document.createElement('a')
                    a.setAttribute('class',"list-group-item f-data")
                    a.setAttribute('id',f_name)
                    let d1 = document.createElement('div')
                    d1.setAttribute('class',"flex")
                    let span = document.createElement('span')
                    let span2 = document.createElement('span')
                    span.setAttribute('class',"badge text-bg-primary rounded-pill")
                    span.innerText=`in ${data[f_name][0]}`
                    span2.innerText=`Subject: ${data[f_name][1]}`
                    // a.addEventListener('click',()=>{openModal()})
                    if (data[f_name][1] != "None"){
                        a.setAttribute('onclick',`openModal("${f_name}")`)
                    }
                    d1.innerText=f_name
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

