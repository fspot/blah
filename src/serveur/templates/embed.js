(function() {
    alert('{{ site }} / {{ article }}');
    var comments = {{ comz }};
	if (window.blah) {
		blah.onComments(comments);
	}
})();