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
                if (response.success) {
                    title = 'Парсер запущен';
                    text = 'Активирован парсинг пользователей по запросу ' + response.message;
                    type = "success";
                }
                else {
                    title = 'Ошибка';
                    text = 'Поиск по запросу ' + response.message + ' уже производился. Дождитесь окончания парсинга или просмотрите результаты предыдущих запросов.'
                    type = "warning";
                }
                swal({title: title,
                    text: text,
                    type: type,
                    timer: 5000,
                    showConfirmButton: false
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

});