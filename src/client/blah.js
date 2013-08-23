(function() {
    window.blah = window.blah || {};

    blah.onComments = function(comments) {
        console.log(comments);
    };

    blah.fetchComments = function() {
        // ajax cross domain:
        (function() {
            var xhr = new (window.XDomainRequest || window.XMLHttpRequest)();
            xhr.onload = function() {
                var response = JSON.parse(xhr.responseText);
                blah.onComments(response.comments);
            }
            xhr.open("GET", blah.url_api + blah.site + "/" + blah.article + "/comments");
            xhr.send();
        })();
    };

    blah.post = function(comment) {
        var xhr = new (window.XDomainRequest || window.XMLHttpRequest)();
        xhr.onload = function() {
            console.log(xhr);
            var comz = JSON.parse(xhr.responseText);
            console.log(comz);
            document.getElementById("commentaires").innerHTML = xhr.responseText;
        }
        xhr.open("POST", blah.url_api + blah.site + "/" + blah.article + "/post");
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.send(JSON.stringify(comment));
    };

    blah.init = function(url_api, site, article) {
        blah.url_api = url_api;
        blah.site = site;
        blah.article = article;
        blah.fetchComments();
    };
})();