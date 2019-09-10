var ctrl = {
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
					document.getElementById(device_type[0] + response[i].id).setAttribute('data-active', response[i].state);
				}
			}
		});
	},
	make_element_active: function(element_id, active_flag) {
		document.getElementById(element_id).setAttribute('data-active', active_flag);
	},
	update_thermistor_controls: function(thermistor_data_object_array) {
		$(thermistor_data_object_array).each(function() {
			document.getElementById('t' + this.id).innerHTML = this.temperature;
		});
	},
	update_valve_controls: function(valve_data_object_array) {
		$(valve_data_object_array).each(function() {
			ctrl.make_element_active('v' + this.id, this.state);
		});
	},
	update_pump_controls: function(pump_data_object_array) {
		$(pump_data_object_array).each(function() {
			ctrl.make_element_active('p' + this.id, this.state);
		});
	},
	update_heater_controls: function(heater_data_object_array) {
		$(heater_data_object_array).each(function() {
			ctrl.make_element_active('h' + this.id, this.state);
		});
	},
	update_main_switch_control: function(data_object) {
		this.make_element_active('main-switch', data_object.state);
	},		
	make_secure_post_request: function(request_url) {
		$.ajax({
			url: request_url, 
			method: 'POST',
			data: { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value') } 
		});
	},
	toggle_device: function(device_btn_elm) {
		this.make_secure_post_request('/api/' + this.get_device_type(device_btn_elm) + '/' + this.get_device_no(device_btn_elm) + '/toggle/');
	},
	toggle_automation: function() {
		this.make_secure_post_request('/api/automation/toggle/');
	},
	update_all_controls: function() {
		$.ajax({
			url: '/api/',
			method: 'GET',
			success: function(responseData) {
				ctrl.update_thermistor_controls(responseData.thermistor);
				ctrl.update_valve_controls(responseData.valve);
				ctrl.update_pump_controls(responseData.pump);
				ctrl.update_heater_controls(responseData.heater);
				ctrl.update_main_switch_control(responseData.automation);
			}
		});
	},
	provision: function() {
		if (confirm('Are you sure?'))
			this.make_secure_post_request('/api/provision/');
	}
};
