var plot = {
	chart_object: null,
	chart_config: {
		type: 'line', 
		data: {
			labels: [],
			datasets: [{
				label: 'T1    ',
				backgroundColor: 'rgb(255, 0, 0)',
				borderColor: 'rgb(255, 0, 0)',
				data: [],
				fill: false,
			}, {
				label: 'T2    ',
				backgroundColor: 'rgb(255, 159, 64)',
				borderColor: 'rgb(255, 159, 64)',
				data: [],
				fill: false,
			}, {
				label: 'T3    ',
				backgroundColor: 'rgb(255, 225, 0)',
				borderColor: 'rgb(255, 225, 0)',
				data: [],
				fill: false,
			}, {
				label: 'T4    ',
				backgroundColor: 'rgb(107,142,35)',
				borderColor: 'rgb(107,142,35)',
				data: [],
				fill: false,
			}, {
				label: 'T5    ',
				backgroundColor: 'rgb(54, 162, 235)',
				borderColor: 'rgb(54, 162, 235)',
				data: [],
				fill: false,
			}, {
				label: 'T6    ',
				backgroundColor: 'rgb(153, 102, 255)',
				borderColor: 'rgb(153, 102, 255)',
				data: [],
				fill: false,
			}, {
				label: 'T7    ',
				backgroundColor: 'rgb(0, 245, 250)',
				borderColor: 'rgb(0, 245, 250)',
				data: [],
				fill: false,
			}, {
				label: 'T8    ',
				backgroundColor: 'rgb(160, 160, 160)',
				borderColor: 'rgb(160, 160, 160)',
				data: [],
				fill: false,
			}]
		},
		options: {
			responsive: true,
			title: {
				display: true,
				text: ''
			},
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true
			},
			scales: {
				xAxes: [{
					type: 'time',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Date and Time'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Temperature'
					}
				}]
			}
		}
	},
	init: function() {
		var chart_element = document.getElementById('temperature-chart');
		var chart_context = chart_element.getContext('2d');
		
		this.chart_object = new Chart(chart_context, this.chart_config);
	},
	append_temperature_data: function(data_object) {
		this.chart_config.data.labels.push(data_object.date);

		this.chart_config.data.datasets.forEach(function(dataset, index){
			dataset.data.push(data_object.temperature_array[index]);
		});
	},
	prepend_experiment_data: function(data_object) {
		var experiment_id_element = document.createElement('span');
		experiment_id_element.setAttribute('class', 'experiment-id');
		experiment_id_element.innerHTML = data_object.id;

		var decorative_arrow_element = document.createElement('span');
		decorative_arrow_element.setAttribute('class', 'decorative-arrow');
		decorative_arrow_element.innerHTML = '>';

		var experiment_date_element = document.createElement('span');
		experiment_date_element.setAttribute('class', 'experiment-date');
		experiment_date_element.innerHTML = data_object.start_date;

		var experiment_anchor_element = document.createElement('a');
		experiment_anchor_element.setAttribute('class', 'experiment-link');
		experiment_anchor_element.setAttribute('onclick', 'plot.select_experiment(this)');
		experiment_anchor_element.appendChild(experiment_id_element);
		experiment_anchor_element.appendChild(decorative_arrow_element);
		experiment_anchor_element.appendChild(experiment_date_element);

		$('#experiment-view').prepend(experiment_anchor_element);
	},
	select_experiment: function(experiment_anchor_element) {
		$('.experiment-link.active').removeClass('active');
		$(experiment_anchor_element).addClass('active');
	},
	update_temperature: function() {
		if ($('.experiment-link.active').length == 0)
			return;

		var request_url = '/api/temperature/?experiment=' + $('.experiment-link.active')[0].firstElementChild.innerHTML;

		if (this.chart_config.data.labels.length)
			request_url += '&last_date=' + plot.chart_config.data.labels[plot.chart_config.data.labels.length - 1];

		$.ajax({
			url: request_url,
			method: 'GET',
			success: function(response) {
				response.forEach(function(object){ 
					plot.append_temperature_data(object); 
				});
			}
		});
		
		this.chart_object.update();
	},
	update_experiment: function() {
		var request_url = '/api/experiment/';
 
		if ($('.experiment-link').length)
			request_url += '?last=' + $('.experiment-link')[0].children[0].innerHTML;

		$.ajax({
			url: request_url,
			method: 'GET',
			success: function(response) {
				response.forEach(function(object){ 
					plot.prepend_experiment_data(object); 
				});

				if ($('.experiment-link.active').length == 0)
					plot.select_experiment(document.getElementById('experiment-view').firstElementChild);
			}
		});
	}
};
