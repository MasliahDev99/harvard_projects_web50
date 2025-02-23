document.addEventListener("DOMContentLoaded", () => {
 
  document.body.addEventListener("click", (event) => {
    if (
      event.target.classList.contains("like-button") ||
      event.target.closest(".like-button")
    ) {
      const button = event.target.classList.contains("like-button")
        ? event.target
        : event.target.closest(".like-button");
      handleToggleLike(button);
    }
  });

  function handleToggleLike(button) {
    const postId = button.getAttribute("data-post-id");
    const url = `/like/${postId}/`; // URL de la vista toggle

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((data) => {
        if (data.success) {
         
          if (data.liked) {
          
            button.classList.remove("btn-outline-primary");
            button.classList.add("btn-primary");
            const icon = button.querySelector("i");
            if (icon) {
              icon.classList.remove("fa-thumbs-up");
              icon.classList.add("fa-thumbs-down");
            }
          } else {

            button.classList.remove("btn-primary");
            button.classList.add("btn-outline-primary");
            const icon = button.querySelector("i");
            if (icon) {
              icon.classList.remove("fa-thumbs-down");
              icon.classList.add("fa-thumbs-up");
            }
          }
          // Actualiza el contador de likes
          const likeCountElement = document.getElementById(`like-count-${postId}`);
          if (likeCountElement) {
            likeCountElement.textContent = `${data.like_count} like${data.like_count !== 1 ? "s" : ""}`;
          }
        } else {
          throw new Error(data.error || "Failed to toggle like.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
       
      });
  }

  // Función para obtener el CSRF token de las cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


});
