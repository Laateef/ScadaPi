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
	init: function() {
		var chart_element = document.getElementById('temperature-chart');
		var chart_context = chart_element.getContext('2d');
		this.chart_object = new Chart(chart_context, this.chart_config);
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

		var experiment_anchor_element = document.createElement('a');
		experiment_anchor_element.setAttribute('class', 'experiment-link');
		experiment_anchor_element.setAttribute('data-active', '0');
		// when an experiment link is clicked, make it current and then update the chart
		experiment_anchor_element.setAttribute('onclick', 'plot.select_experiment_and_fetch_temperature(this)'); 
		experiment_anchor_element.appendChild(experiment_id_element);
		experiment_anchor_element.appendChild(decorative_arrow_element);
		experiment_anchor_element.appendChild(experiment_date_element);

		$('#experiment-view').prepend(experiment_anchor_element);
	},
	select_experiment: function(experiment_anchor_element) {
		$('.experiment-link').attr('data-active', '0');
		$(experiment_anchor_element).attr('data-active', '1');
	},
	update_temperature: function() {
		if ($('.experiment-link[data-active="1"]').length == 0)
			return;

		var request_url = '/api/temperature/?experiment=' + $('.experiment-link[data-active="1"]')[0].firstElementChild.innerHTML;

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
 
		if ($('.experiment-link').length)
			request_url += '?last=' + $('.experiment-link')[0].children[0].innerHTML;

		$.ajax({
			url: request_url,
			method: 'GET',
			success: function(response) {
				$(response).each(function(){ 
					plot.prepend_experiment_data(this); 
				});

				if ($('.experiment-link[data-active="1"]').length == 0)
					plot.select_experiment($('.experiment-link')[0]);
			}
		});
	},
	select_experiment_and_fetch_temperature: function(experiment_anchor_element) {
		plot.select_experiment(experiment_anchor_element);
		plot.update_temperature();
	}
};
