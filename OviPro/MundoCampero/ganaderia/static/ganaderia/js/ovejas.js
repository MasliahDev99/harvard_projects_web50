document.addEventListener('DOMContentLoaded', function() {
    const bornDateInput = document.getElementById('bornDate');
    const ageInput = document.getElementById('age');
    const hasDefectsCheckbox = document.getElementById('hasDefects');
    const defectsTextareaContainer = document.getElementById('defectsTextareaContainer');

    // calculamos la edad segun la fecha de nacimiento en meses
    // si cambia el anio avanza la edad tambien, 
    //error en el script es que si el animal nacio en el 2024 cuando supera el 2024 la edad queda -1
   
    bornDateInput.addEventListener('change', function() {
        const birthDate = new Date(this.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        

    });

    // Show/hide defects textarea
    hasDefectsCheckbox.addEventListener('change', function() {
        defectsTextareaContainer.classList.toggle('d-none', !this.checked);
    });

    // capturamos el genero de la oveja
    const gender = document.getElementById('gender')
    const type = document.getElementById('type')  
});