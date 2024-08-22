// declare options
var id_superficie_select = {
    'Futbol':  ['Cesped Natural','Cesped sintetico','Otros'],
	'Tenis':   ['Cancha repida','Polvo de ladrillo','Otros'],
	'Basquet': ['Parquet','Cemento','Otros'],
	'Paddle':  ['Cancha rapida']
};

// get previus values for update view
var sportValue = $('#id_deporte').val();
var surfacesValue = $('#id_superficie').val();

loadSurfaces();

function loadSurfaces() {

	var $id_superficie = $('#id_superficie');

	// hide input
	$('#id_superficie').hide();

	// create fake select
	$("#id_superficie").after( "<select id='id_superficie_select'><option value=''>Selecciona un deporte primero</option></select>" );

	// set id on selects
	var $id_superficie_select = $('#id_superficie_select');
	var $id_deporte = $('#id_deporte');

	// generate values
	function generateSurfaces() {
	    var id_deporte =  $('#id_deporte').val(), lcns = id_superficie_select[id_deporte] || [];
	    var html = $.map(lcns, function(lcn){
	        return '<option value="' + lcn + '">' + lcn + '</option>'
	    }).join('');
	    $id_superficie_select.html(html);
	};

	$('#id_deporte').change(function () {
		console.log($('#id_deporte').val());
	    generateSurfaces();
	});

	// get values and set selects

	if ($('#id_deporte').length && $('#id_deporte').val().length) {
		$('#id_deporte').val(sportValue);
		generateSurfaces();
	} else {
		$('#id_deporte').val($("#id_deporte").val());
	};

	if ($('#id_superficie').length && $('#id_superficie').val().length) {
		$('#id_superficie_select').val(surfacesValue);
	} else {
		$('#id_superficie').val($("#id_superficie_select").val());
		$('#id_superficie_select').append('<option value="">Selecciona un deporte primero</option>');
	};

	// write inputs

	$( "#id_superficie_select" ).change(function() {
		$('#id_superficie').val($("#id_superficie_select").val());
	});

	$( "#id_deporte" ).change(function() {
		$('#id_deporte').val($("#id_deporte").val());
		$('#id_superficie').val($("#id_superficie_select").val());
	});
};
