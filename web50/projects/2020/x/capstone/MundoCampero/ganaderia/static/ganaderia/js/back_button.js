document.addEventListener("DOMContentLoaded", function() {
    const previousUrl = document.referrer;

    const sheepdUrl = 'hub/dashboard/ovejas/';
    const salesUrl = 'hub/dashboard/ventas/';

    const backButtonContainer = document.querySelector('.back-button-container');
    if (backButtonContainer) {
        const backButton = document.createElement('a');
        backButton.className = 'btn btn-outline-secondary';
        backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Back';

        if (previousUrl.includes(sheepdUrl)) {
            backButton.href = '/hub/dashboard/ovejas'; // Redirect to dashboard
        } else if (previousUrl.includes(salesUrl)) {
            backButton.href = '/hub/dashboard/ventas/'; // Redirect to ventas
        } else {
            backButton.href = 'javascript:history.back()'; 
        }

        backButtonContainer.appendChild(backButton);
    }
});