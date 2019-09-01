var main = {
	current_tab_changed: function(element) {
		tab_link_list = document.getElementsByClassName('tab-link');
		tab_content_list = document.getElementsByClassName('tab-content');

		for (var i = 0; i < tab_link_list.length; ++i) {
			tab_link_list[i].className = tab_link_list[i].className.replace(' active', ''); 
		}

		for (var i = 0; i < tab_content_list.length; ++i) {
			tab_content_list[i].style.display = 'none';
		}

		document.getElementById(element.href.substr(element.href.indexOf('#') + 1)).style.display = 'block';
		element.className += ' active';
	}
};
