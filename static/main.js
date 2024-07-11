q_inp=document.querySelector('#query')
q_inp.addEventListener('onchange',()=>{
	val = q_inp.value
	let data;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = ()=>{
		if (this.readState==4 and this.status==200){
			data=JSON.parse(xhttp.responseText)
		}
	}


})
