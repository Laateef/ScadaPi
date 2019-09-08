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
			}, {
				label: 'T2    ',
				backgroundColor: 'rgb(255, 159, 64)',
				borderColor: 'rgb(255, 159, 64)',
				data: [],
			}, {
				label: 'T3    ',
				backgroundColor: 'rgb(255, 225, 0)',
				borderColor: 'rgb(255, 225, 0)',
				data: [],
			}, {
				label: 'T4    ',
				backgroundColor: 'rgb(107,142,35)',
				borderColor: 'rgb(107,142,35)',
				data: [],
			}, {
				label: 'T5    ',
				backgroundColor: 'rgb(54, 162, 235)',
				borderColor: 'rgb(54, 162, 235)',
				data: [],
			}, {
				label: 'T6    ',
				backgroundColor: 'rgb(153, 102, 255)',
				borderColor: 'rgb(153, 102, 255)',
				data: [],
			}, {
				label: 'T7    ',
				backgroundColor: 'rgb(0, 245, 250)',
				borderColor: 'rgb(0, 245, 250)',
				data: [],
			}, {
				label: 'T8    ',
				backgroundColor: 'rgb(160, 160, 160)',
				borderColor: 'rgb(160, 160, 160)',
				data: [],
			}]
		},
		options: {
			events: ['click', 'mousemove'],
			responsive: true,
			animation: {
				duration: 0,
			},
			legend: {
				onHover: function(e) { 
					e.target.style.cursor = 'pointer';
				}
			},
			hover: {
				animationDuration: 0,
				mode: 'nearest',
				intersect: true,
				onHover: function(e) {
					e.target.style.cursor = 'default';
				}
			},
			responsiveAnimationDuration: 0,
			title: {
				display: true,
				text: ''
			},
			tooltips: {
				enabled: false,
			},
			elements: {
				point: {
					radius: 0,
				},
				line: {
					borderWidth: 1,
					fill: false,
					tension: 0,				
				}
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
				}],
			}
		}
	},
	reset_chart_data: function() {
		this.chart_config.data.labels = [];
		$(this.chart_config.data.datasets).each(function(index){
			this.data = [];
		});
	},
	init: function() {
		var chart_element = document.getElementById('temperature-chart');
		var chart_context = chart_element.getContext('2d');
		this.chart_object = new Chart(chart_context, this.chart_config);

		plot.reset_chart_data();
	},
	append_temperature_data: function(data_object) {
		this.chart_config.data.labels.push(moment(data_object.date));

		$(this.chart_config.data.datasets).each(function(index){
			this.data.push(data_object.temperature_array[index]);
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

		var experiment_plot_button_element = document.createElement('button');
		experiment_plot_button_element.setAttribute('class', 'experiment-plot-button');
		experiment_plot_button_element.setAttribute('data-active', '0');
		// when an experiment button is clicked, make it current and then update the chart
		experiment_plot_button_element.setAttribute('onclick', 'plot.select_experiment_and_fetch_temperature(this)'); 
		experiment_plot_button_element.appendChild(experiment_id_element);
		experiment_plot_button_element.appendChild(decorative_arrow_element);
		experiment_plot_button_element.appendChild(experiment_date_element);

		var experiment_delete_button_element = document.createElement('button');
		experiment_delete_button_element.setAttribute('class', 'experiment-delete-button');
		experiment_delete_button_element.setAttribute('onclick', 'plot.delete_experiment(this.parentElement)'); 
		experiment_delete_button_element.innerHTML = 'X';

		var experiment_item_element = document.createElement('li');
		experiment_item_element.setAttribute('class', 'experiment-item');
		experiment_item_element.appendChild(experiment_plot_button_element);
		experiment_item_element.appendChild(experiment_delete_button_element);

		$('#experiment-item-list').prepend(experiment_item_element);
	},
	select_experiment: function(experiment_item_element) {
		$('.experiment-item').attr('data-active', '0');
		$(experiment_item_element).attr('data-active', '1');

		plot.reset_chart_data();
	},
	update_temperature: function() {
		if ($('.experiment-item[data-active="1"]').length == 0)
			return;

		var request_url = '/api/temperature/?experiment=' + $('.experiment-item[data-active="1"]')[0].children[0].children[0].innerHTML;

		if (plot.chart_config.data.labels.length)
			request_url += '&last_date=' + plot.chart_config.data.labels[plot.chart_config.data.labels.length - 1].format(moment.HTML5_FMT.DATETIME_LOCAL_SECONDS);

		$.ajax({
			url: request_url,
			method: 'GET',
			success: function(response) {
				$(response).each(function(){ 
					plot.append_temperature_data(this); 
				});

				plot.chart_object.update();
			}
		});
	},
	update_experiment: function() {
		var request_url = '/api/experiment/';
 
		if ($('.experiment-item').length)
			request_url += '?last=' + $('.experiment-item')[0].children[0].children[0].innerHTML;

		$.ajax({
			url: request_url,
			method: 'GET',
			success: function(response) {
				$(response).each(function(){ 
					plot.prepend_experiment_data(this); 
				});

				if ($('.experiment-item[data-active="1"]').length == 0)
					plot.select_experiment($('.experiment-item')[0]);
			}
		});
	},
	select_experiment_and_fetch_temperature: function(experiment_item_element) {
		plot.select_experiment(experiment_item_element);
		plot.update_temperature();
	},
	delete_experiment: function(experiment_delete_button_element) {
		if ($('.experiment-item[data-active="1"]').length == 0)
			return;

		var experiment_item_element = experiment_delete_button_element.parentElement;
		var experiment_id = experiment_item_element.firstElementChild.firstElementChild.innerHTML;
		ctrl.make_secure_post_request('/api/experiment/' + experiment_id + '/delete/');
	}
};
