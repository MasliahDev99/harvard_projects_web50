document.addEventListener("DOMContentLoaded", () => {
    
    const bootstrap = window.bootstrap
  
    // Event delegation para los botones de editar y guardar
    document.addEventListener("click", (event) => {
      // Manejar clic en botón de editar
      if (event.target.classList.contains("edit-button")) {
        const postId = event.target.getAttribute("data-post-id")
        const modalElement = document.getElementById(`editModal_${postId}`)
        const textarea = modalElement.querySelector(".modal-body textarea")
        const postContent = document.getElementById(`post-content-${postId}`).textContent
        textarea.value = postContent
      }
  
      // Manejar clic en botón de guardar
      if (event.target.classList.contains("save-edit")) {
        const modalElement = event.target.closest(".modal")
        const postId = modalElement.id.split("_")[1]
        const textarea = modalElement.querySelector(".modal-body textarea")
        const newContent = textarea.value.trim()
  
        handleSaveEdit(postId, newContent, modalElement)
      }
    })
  
    // Función para manejar el guardado de la edición
    function handleSaveEdit(postId, newContent, modalElement) {
      if (!newContent) {
        showAlert("Post content cannot be empty", "danger")
        return
      }
  
      fetch(`/edit/${postId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          content: newContent,
        }),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok")
          return response.json()
        })
        .then((data) => {
          if (data.success) {
            // Actualizar el contenido en la página
            document.getElementById(`post-content-${postId}`).textContent = newContent
  
            // Cerrar el modal correctamente
            const modal = bootstrap.Modal.getInstance(modalElement)
            modal.hide()
  
            // Limpiar el backdrop y la clase modal-open
            document.body.classList.remove("modal-open")
            const backdrop = document.querySelector(".modal-backdrop")
            if (backdrop) backdrop.remove()
  
            showAlert("Post updated successfully!", "success")
          } else {
            throw new Error(data.error || "Failed to update post")
          }
        })
        .catch((error) => {
          console.error("Error:", error)
          showAlert("Failed to update post. Please try again.", "danger")
        })
    }
  
    // Manejar el cierre de los modales
    document.querySelectorAll(".modal").forEach((modal) => {
      modal.addEventListener("hidden.bs.modal", () => {
        // Limpiar el backdrop y la clase modal-open
        document.body.classList.remove("modal-open")
        const backdrop = document.querySelector(".modal-backdrop")
        if (backdrop) backdrop.remove()
      })
    })
  
    function getCookie(name) {
      let cookieValue = null
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";")
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
  
    function showAlert(message, type) {
      const alertDiv = document.createElement("div")
      alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`
      alertDiv.style.zIndex = "9999"
      alertDiv.role = "alert"
      alertDiv.innerHTML = `
              ${message}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          `
  
      document.body.appendChild(alertDiv)
  
      setTimeout(() => {
        alertDiv.remove()
      }, 3000)
    }
  })
  
  