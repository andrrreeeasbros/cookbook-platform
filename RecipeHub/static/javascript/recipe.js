$('#addRecipeForm').on('submit', function(event) {
  event.preventDefault();

  const form = $(this);
  $('#form-errors').html('');

  $.ajax({
    type: "POST",
    url: "{% url 'RecipeHub:add_recipe' %}",
    data: form.serialize(),
    success: function(response) {
      if (response.success) {
        alert(response.message);
        $('#addRecipeModal').modal('hide');
        location.reload();
      } else {
        alert('Ошибка при добавлении рецепта.');
      }
    },
    error: function(response) {
      const errors = response.responseJSON.errors;
      let errorMessages = '<ul>';
      for (let field in errors) {
        errors[field].forEach(function(error) {
          errorMessages += `<li>${error}</li>`;
        });
      }
      errorMessages += '</ul>';
      $('#form-errors').html(errorMessages);
    }
  });
});

$('#recipeModal').on('show.bs.modal', function (event) {
  const button = $(event.relatedTarget);
  const recipeName = button.data('recipe-name');

  fetch(`/recipe-details/${recipeName}/`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Ошибка запроса');
      }
      return response.json();
    })
    .then(data => {
      if (data) {
        const recipeContent = document.getElementById('recipeContent');
        
        const cookingTime = data.cooking_time ? `
          <div class="cooking-time">
            <h5>Время приготовления:</h5>
            <span>${data.cooking_time}</span>
          </div>` : '';  

        recipeContent.innerHTML = `
          <h1 class="text-center">${data.name}</h1>
          <h5>Уровень сложности: ${data.level}</h5>
  
          <h5>Ингредиенты:</h5>
          <ul>${data.ingredients.map((ingredient, index) => `<li>${index + 1}. ${ingredient}</li>`).join('')}</ul>
  
          <h5>Этапы приготовления:</h5>
           <ul>
           ${data.steps.map((step) => `<li>${step.step_number}. ${step.step_description}</li>`).join('')}
           </ul>
  
          ${cookingTime}
        `;
      }
    })
    .catch(error => alert('Ошибка при загрузке данных рецепта'));
});
