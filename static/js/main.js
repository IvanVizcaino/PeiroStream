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
		stopStreaming();
	});

	var stopStreaming = function(){
		jQuery.get( "/stop", function( data ) {
			if(data.result){
				jQuery("#stopStreaming b").text("offline");
				jQuery("#stopStreaming b").css("color","red");
				jQuery("#stopStreaming i").removeClass('fa-stop-circle');
				jQuery("#stopStreaming i").addClass('fa-play-circle');
				jQuery("#stopStreaming").unbind( "click" );
				jQuery("#stopStreaming").attr('id','startStreaming');
				jQuery("#startStreaming").click(function(){
					startStreaming();
				})
			}else{
				alert("Error. No se pudo detener la transmisión");
			}
			
		  }).fail(function() {
			  alert("Se produjo un error: "+data);
		  });
	}
	var startStreaming = function(){
		jQuery.get( "/start", function( data ) {
			if(data.result){
				jQuery("#startStreaming b").text("live");
				jQuery("#startStreaming b").css("color","green");
				jQuery("#startStreaming i").removeClass('fa-play-circle');
				jQuery("#startStreaming i").addClass('fa-stop-circle');
				jQuery("#startStreaming").unbind( "click" );
				jQuery("#startStreaming").attr('id','stopStreaming');
				jQuery("#stopStreaming").click(function(){
					stopStreaming();
				});			
			}else{
				alert("Error. No se pudo detener la transmisión");
			}
			
		  }).fail(function() {
			  alert("Se produjo un error: "+data);
		  });
	}
});