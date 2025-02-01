document.addEventListener("DOMContentLoaded", () => {
  const addOvinoForm = document.getElementById("addOvinoForm")
  const calificadorPurezaSelect = document.getElementById("calificador_pureza")
  const parentSection = document.getElementById("parentSection")
  const purchasedCheckboxContainer = document.getElementById("purchasedCheckboxContainer")
  const origenContainer = document.getElementById("origenContainer")
  const purchasedCheckbox = document.getElementById("purchased")
  const obsCheckbox = document.getElementById("obs")
  const observacionesContainer = document.getElementById("observacionesContainer")
  const rpContainer = document.getElementById("rpContainer")

  const rpInput = document.getElementById("RP")
  const fatherSheepInput = document.getElementById("oveja_padre")
  const motherSheepInput = document.getElementById("oveja_madre")
  const nombreAnimalInput = document.getElementById("nombre_animal")
  const pesoInput = document.getElementById("peso")

  function toggleParentFields() {
    const selectedValue = calificadorPurezaSelect.value.toLowerCase()
    const isPedigree = selectedValue === "pedigree" || selectedValue === "pedigri"

    parentSection.style.display = isPedigree ? "block" : "none"
    rpContainer.style.display = isPedigree ? "block" : "none"
    purchasedCheckboxContainer.style.display = "block"

    if (!isPedigree) {
      fatherSheepInput.value = ""
      motherSheepInput.value = ""
      rpInput.value = ""
    }

    togglePurchasedFields()
    updateRequiredFields(isPedigree)
  }

  function togglePurchasedFields() {
    const isChecked = purchasedCheckbox.checked
    origenContainer.style.display = isChecked ? "block" : "none"
  }

  function updateRequiredFields(isPedigree) {
    if (isPedigree) {
      fatherSheepInput.required = true
      motherSheepInput.required = true
      rpInput.required = true
      nombreAnimalInput.required = true
    } else {
      fatherSheepInput.required = false
      motherSheepInput.required = false
      rpInput.required = false
      nombreAnimalInput.required = false
    }
  }

  function validateWeight() {
    const weight = Number.parseFloat(pesoInput.value)
    pesoInput.setCustomValidity("")

    if (weight < 0) {
      pesoInput.setCustomValidity("El peso no puede ser negativo")
    } else if (weight < 1) {
      pesoInput.setCustomValidity("El peso mínimo es 1kg")
    }
  }

  function validateParentFields() {
    const father = fatherSheepInput.value
    const mother = motherSheepInput.value
    const RP = rpInput.value

    fatherSheepInput.setCustomValidity("")
    motherSheepInput.setCustomValidity("")
    rpInput.setCustomValidity("")

    if (father === mother && father !== "" && mother !== "") {
      const errorMsg = "Los RP de padre y madre no pueden ser iguales"
      fatherSheepInput.setCustomValidity(errorMsg)
      motherSheepInput.setCustomValidity(errorMsg)
    }

    if ((father === RP && RP !== "") || (mother === RP && RP !== "")) {
      const errorRPAnimal = "El RP del animal no puede ser igual al RP de su padre o madre"
      rpInput.setCustomValidity(errorRPAnimal)

      if (father === RP) {
        fatherSheepInput.setCustomValidity("El RP del padre no puede ser igual al RP del animal")
      }
      if (mother === RP) {
        motherSheepInput.setCustomValidity("El RP de la madre no puede ser igual al RP del animal")
      }
    }
  }

  obsCheckbox.addEventListener("change", function () {
    observacionesContainer.style.display = this.checked ? "block" : "none"
  })

  purchasedCheckbox.addEventListener("change", togglePurchasedFields)
  calificadorPurezaSelect.addEventListener("change", toggleParentFields)
  pesoInput.addEventListener("input", validateWeight)
  fatherSheepInput.addEventListener("input", validateParentFields)
  motherSheepInput.addEventListener("input", validateParentFields)
  rpInput.addEventListener("input", validateParentFields)

  addOvinoForm.addEventListener("submit", (event) => {
    const isPedigree =
      calificadorPurezaSelect.value.toLowerCase() === "pedigree" ||
      calificadorPurezaSelect.value.toLowerCase() === "pedigri"

    updateRequiredFields(isPedigree)
    validateWeight()
    validateParentFields()

    if (isPedigree) {
      if (!fatherSheepInput.value || !motherSheepInput.value || !rpInput.value || !nombreAnimalInput.value) {
        event.preventDefault()
        alert("Para ovejas pedigri, los campos RP, RP padre, RP madre y Nombre del animal son obligatorios.")
        return
      }
    }

    if (!addOvinoForm.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()
    }
    addOvinoForm.classList.add("was-validated")
  })

  // Initial setup
  toggleParentFields()
  observacionesContainer.style.display = "none"
})

