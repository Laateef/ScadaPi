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
	populate_generic_device_array: function(device_type) {
		$.ajax({
			url: '/api/' + device_type + '/',
			method: 'GET',
			success: function(response) {
				for (var i = 0; i < response.length; ++i) {
					document.getElementById(device_type[0] + response[i].id).innerHTML = response[i].state;
				}
			}
		});
	},	
	populate_heater_array: function() {
		this.populate_generic_device_array('heater');
	},
	populate_pump_array: function() {
		this.populate_generic_device_array('pump');
	},
	populate_valve_array: function() {
		this.populate_generic_device_array('valve');
	},
	toggle_device: function(device_btn_elm) {
		$.ajax({
			url: '/api/' + this.get_device_type(device_btn_elm) + '/' + this.get_device_no(device_btn_elm) + '/toggle/', 
			method: 'PATCH'
		});
	},
	adjust_main_switch: function() {
		$.ajax({
			url: '/api/automation/', 
			method: 'GET',
			success: function(response) {
				if (response[0].state)
					document.getElementById('main_switch').innerHTML = 'Stop';
				else
					document.getElementById('main_switch').innerHTML = 'Start';
			}
		});

	},
	toggle_automation: function() {
		$.ajax({
			url: '/api/automation/toggle/', 
			method: 'PATCH'
		});
	},
};
