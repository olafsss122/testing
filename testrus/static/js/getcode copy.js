$(document).ready(function() {
    // Функция для выполнения запроса к серверу
    
    document.getElementById('select-option').addEventListener('click', function() {
        var selectedOption = document.querySelector('input[name="2fa-type"]:checked').value;
        console.log(selectedOption);
        // Отобразить только выбранную форму
        document.getElementById(selectedOption + '-form').style.display = 'block';
        document.getElementById('select').style.display = 'none';
        if (selectedOption == 'code-from-device') {
        device();
    }
    });
    function checkcode() {
        $.ajax({
            type: "GET",
            url: "/getcode",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
            success: function(response) {
                console.log(response[0]);
                if (response[0] != null) {
                    document.getElementById('result').innerHTML = 'Prove authorisation, press the next number on your phone: ' + response[0];
                }  else {
                    // Если значение не 'Yes' или 'No', продолжить опрос через 5 секунд
                    setTimeout(checkcode, 5000);
                }
            },
            error: function(error) {
                console.error("Ошибка при проверке значения code")
             
                setTimeout(checkcode, 5000);
            }
        });
    }
    function device() {
        $.ajax({
            type: "POST",
            headers: {"Content-Type": "application/json"},
            url: "/device",
            data: {
                key1: 'pss'
            }, 
            success: function(response) {
                console.log(response)
                setTimeout(checkcode(), 5000);
            },
            error: function(error) {
                console.error("Ошибка при post");
                console.error(error);
            }
        });
    }
});