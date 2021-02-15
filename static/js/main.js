jQuery(document).ready(function(){
	jQuery(".shutdown").click(function(){
		var r = confirm("¿Estás seguro?");
		if (r == true) {
		  jQuery.get( "/shutdown", function( data ) {
			  window.close();
			}).fail(function() {
			    window.close();
			});
		} 
	})

	jQuery("#stopStreaming").click(function(){
		jQuery.get( "/stop", function( data ) {
			if(data.result){
				jQuery("#stopStreaming b").text("offline");
				jQuery("#stopStreaming b").css("color","red");
			}else{
				alert("Error. No se pudo detener la transmisión");
			}
			
		  }).fail(function() {
			  alert("Se produjo un error: "+data);
		  });
	})
});