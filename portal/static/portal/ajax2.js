$(function() {
    $('#login').click( function(){
        $.ajax({

            type: "POST",
            url: "/portal/login/",
            data: {
                'webmail' : $('#webmail').val(),
                'password' : $('#password').val(),
                'server' : $('#server').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#login-results').html(data)
}