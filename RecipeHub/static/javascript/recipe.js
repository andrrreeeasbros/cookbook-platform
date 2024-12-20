// Обработчик для отправки формы добавления рецепта через AJAX
$('#addRecipeForm').on('submit', function(event) {
    event.preventDefault(); // Отменяем стандартную отправку формы
  
    const form = $(this); // Получаем форму
    $('#form-errors').html('');  // Очищаем место для ошибок
  
    // Отправляем данные формы на сервер с использованием AJAX
    $.ajax({
      type: "POST",
      url: "{% url 'RecipeHub:add_recipe' %}",  // Путь к представлению для добавления рецепта
      data: form.serialize(),  // Сериализуем данные формы
      success: function(response) {
        if (response.success) {
          alert(response.message);  // Показываем сообщение об успехе
          $('#addRecipeModal').modal('hide');  // Закрываем модальное окно
          location.reload();  // Перезагружаем страницу для отображения нового рецепта
        } else {
          alert('Ошибка при добавлении рецепта.');
        }
      },
      error: function(response) {
        // Если ошибка при добавлении, отображаем ошибки формы
        const errors = response.responseJSON.errors;
        let errorMessages = '<ul>';
        for (let field in errors) {
          errors[field].forEach(function(error) {
            errorMessages += `<li>${error}</li>`;
          });
        }
        errorMessages += '</ul>';
        $('#form-errors').html(errorMessages);  // Показываем ошибки на странице
      }
    });
  });
  
  // Обработчик для открытия модального окна и загрузки данных рецепта
  $('#recipeModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const recipeName = button.data('recipe-name');  // Используем имя рецепта
  
    // Делаем запрос на сервер для получения данных рецепта
    fetch(`/recipe-details/${recipeName}/`)  // Путь к API для получения данных рецепта
      .then(response => {
        if (!response.ok) {
          throw new Error('Ошибка запроса');
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          const recipeContent = document.getElementById('recipeContent');
          
          // Добавляем вывод времени приготовления
          const cookingTime = data.cooking_time ? `
            <div class="cooking-time">
              <h5>Время приготовления:</h5>
              <span>${data.cooking_time}</span>
            </div>` : '';  
  
          recipeContent.innerHTML = `
            <h1 class="text-center">${data.name}</h1>
            <h5>Уровень сложности: ${data.level}</h5>
    
            <!-- Ингредиенты -->
            <h5>Ингредиенты:</h5>
            <ul>${data.ingredients.map((ingredient, index) => `<li>${index + 1}. ${ingredient}</li>`).join('')}</ul>
    
            <!-- Этапы приготовления -->
            <h5>Этапы приготовления:</h5>
             <ul>
             ${data.steps.map((step) => `<li>${step.step_number}. ${step.step_description}</li>`).join('')}
             </ul>
    
            <!-- Время приготовления -->
            ${cookingTime}
          `;
        }
      })
      .catch(error => alert('Ошибка при загрузке данных рецепта'));
  });
  