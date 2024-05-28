document.addEventListener('DOMContentLoaded', function() {
    const ingredients = document.getElementById('ingredients');
    const directions = document.getElementById('directions');

    const ingredientsCount = document.createElement('div');
    const directionsCount = document.createElement('div');

    ingredients.parentNode.insertBefore(ingredientsCount, ingredients.nextSibling);
    directions.parentNode.insertBefore(directionsCount, directions.nextSibling);

    function updateRemainingChars(textarea, counter, maxChars) {
        const charsLeft = maxChars - textarea.value.length;
        counter.textContent = `${charsLeft} characters remaining`;
        counter.style.color = charsLeft < 0 ? 'red' : 'black'; 
    }

    updateRemainingChars(ingredients, ingredientsCount, 100);
    updateRemainingChars(directions, directionsCount, 900);

    ingredients.addEventListener('input', () => updateRemainingChars(ingredients, ingredientsCount, 100));
    directions.addEventListener('input', () => updateRemainingChars(directions, directionsCount, 900));
});
