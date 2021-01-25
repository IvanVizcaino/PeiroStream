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
});