$(function() {
    $('#apply').click(function() {
        $.ajax({
            type: "POST",
            url: "/portal/validate_post/",
             data: {
                'team_name' : $('#team_name').val(),
                'post' : $('#post').val(),
                'team_year' :$('#team_year').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
        });
    });
});