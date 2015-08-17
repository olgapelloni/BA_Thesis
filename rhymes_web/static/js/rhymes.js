function showEntry() {
    $('a#lemma').click(function() {
        $.getJSON('/_get_entry', {
            lemma: $( this ).text()
        }, function(data) {
            $('html, body').css('position', 'relative');
            $("#entry").html(data.entryHtml);
        });
        return false;
    });
}

// Action after submit search query
$(function() {
    $("#submit_button").click(function(event) {
        $.ajax({
            type: "GET",
            url: "/handler/",
            data: { word: $('input[id="dict_search"]').val()},
            dataType: "json",
            success: function(data) {
                $("#recently").html(data.recently);
                $("#rhymes").html(data.entries);
                }

        });
        event.preventDefault();
    });
});