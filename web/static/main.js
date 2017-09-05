(function(url) {

    var base_url = url;

    function get_items() {
        var xhr = new XMLHttpRequest();
        var url = base_url + '/get';

        xhr.open('GET', url, true);
        xhr.send();

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                var response = xhr.responseText;

                console.log(responseText);
            }
        }
    }

})(url);