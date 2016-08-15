/**
 * Created by sp41mer on 15.08.16.
 */
$(function() {
    $('#buttonStart').click(function() {
        $.ajax({
            url: '/input_query',
            data: $('#queryForm').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});