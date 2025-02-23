document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality (placeholder)
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            // Aquí iría la lógica AJAX para dar like al post
        });
    });

    // Mostrar/Ocultar el formulario de nuevo post
    const addPostButton = document.getElementById('addPostButton');
    const createPostForm = document.getElementById('create-post-form');

    addPostButton.addEventListener('click', (event) => {
        event.preventDefault();
        createPostForm.style.display = (createPostForm.style.display === 'none') ? 'block' : 'none';
    });

    // Validación del contenido al hacer submit
    const postForm = createPostForm.querySelector('form');
    const contentPost = document.getElementById('content-post');
    const errorPost = document.getElementById('error-Post');

    postForm.addEventListener('submit', (event) => {
        if (contentPost.value.trim() === '') {
            event.preventDefault(); // Evita el envío del formulario
            contentPost.classList.remove('border-primary');
            contentPost.classList.add('border-danger');
            errorPost.innerHTML = '<small class="text-danger">Content is required.</small>';
        } else {
            contentPost.classList.remove('border-danger');
            contentPost.classList.add('border-primary');
            errorPost.innerHTML = '';
        }
    });

    // Limpieza de errores al escribir
    contentPost.addEventListener('input', () => {
        if (contentPost.value.trim() !== '') {
            contentPost.classList.remove('border-danger');
            contentPost.classList.add('border-primary');
            errorPost.innerHTML = '';
        }
    });

    const paginationLinks = document.querySelectorAll('.pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
 

});