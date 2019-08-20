var base = {
	get_device_no: function(device_btn_elm) {
		return new RegExp("\\d+").exec(device_btn_elm.getAttribute('id'));
	},
	get_device_type: function(device_btn_elm) {
		return device_btn_elm.getAttribute('class');
	},
	populate_thermistor_array: function() {
		$.ajax({
			url: '/api/thermistor/',
			method: 'GET',
			success: function(response) {
				for (var i = 0; i < response.length; ++i) {
					document.getElementById('t' + response[i].id).innerHTML = response[i].temperature;
				}
			}
		});
	},
	populate_heater_array: function() {
		$.ajax({
			url: '/api/heater/',
			method: 'GET',
			success: function(response) {
				for (var i = 0; i < response.length; ++i) {
					document.getElementById('h' + response[i].id).innerHTML = response[i].state;
				}
			}
		});
	},

};
