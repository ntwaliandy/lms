

// 	CHECKOUT
function formTrigger() {
	checkbox = document.getElementById('checkAlternate');
	form = document.getElementById('formAlternate');
	
	if (checkbox.checked == true) {
		form.style.display = 'block';
	}else{
		form.style.display = 'none';
	}
}