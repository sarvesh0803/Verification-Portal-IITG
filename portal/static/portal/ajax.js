$(function() {
    $('#search_team').keyup(function() {
        $.ajax({

            type: "POST",
            url: "/portal/search_team/",
            data: {
                'search_text' : $('#search_team').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data)
}