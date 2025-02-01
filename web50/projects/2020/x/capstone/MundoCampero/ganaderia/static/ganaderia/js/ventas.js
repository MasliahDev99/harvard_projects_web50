document.addEventListener("DOMContentLoaded", () => {
  // DOM elements
  const saleType = document.getElementById("saleType")
  const batchSale = document.getElementById("batchSale")
  const animalSelect = document.getElementById("animalSelect")
  const selectedAnimals = document.getElementById("selectedAnimals")
  const frigorificoFields = document.getElementById("frigorificoFields")
  const remateFields = document.getElementById("remateFields")
  const individualFields = document.getElementById("individualFields")
  const totalWeight = document.getElementById("totalWeight")
  const pricePerKg = document.getElementById("pricePerKg")
  const remateTotal = document.getElementById("remateTotal")
  const totalSaleValue = document.getElementById("totalSaleValue")
  const confirmSaleBtn = document.getElementById("confirmSale")
  const saleDate = document.getElementById("saleDate")

  let availableSheep = []

  function fetchAvailableSheep() {
    fetch("/api/ovejas/")
      .then((response) => {
        if (!response.ok) throw new Error("Error loading the list of animals.")
        return response.json()
      })
      .then((data) => {
        availableSheep = data
        loadSheepOptions()
      })
      .catch((error) => console.error("Error:", error))
  }

  function loadSheepOptions() {
    animalSelect.innerHTML = ""
    const fragment = document.createDocumentFragment()
    availableSheep.forEach((sheep) => {
      const option = document.createElement("option")
      option.value = sheep.id
      option.textContent = sheep.RP
        ? `RP: ${sheep.RP} - Weight: ${sheep.weight} kg`
        : `ID: ${sheep.id} - Purity: ${sheep.purity_qualifier} - Weight: ${sheep.weight} kg`
      fragment.appendChild(option)
    })
    animalSelect.appendChild(fragment)
  }

  fetchAvailableSheep()

  // Event Listeners
  saleType.addEventListener("change", updateFormFields)
  batchSale.addEventListener("change", updateAnimalSelection)
  animalSelect.addEventListener("change", updateSelectedAnimals)
  pricePerKg.addEventListener("input", calculateSlaughterhouseTotal)
  remateTotal.addEventListener("input", updateTotalSaleValue)
  confirmSaleBtn.addEventListener("click", submitSaleForm)

  function updateFormFields() {
    frigorificoFields.style.display = saleType.value === "slaughterhouse" ? "block" : "none"
    remateFields.style.display = saleType.value === "auction" ? "block" : "none"
    individualFields.style.display = saleType.value === "individual" ? "block" : "none"

    if (saleType.value === "donation") {
      totalSaleValue.value = "0"
    }

    updateAnimalSelection()
    updateSelectedAnimals()
  }

  function updateAnimalSelection() {
    animalSelect.multiple = !batchSale.checked
    if (batchSale.checked) {
      Array.from(animalSelect.selectedOptions)
        .slice(10)
        .forEach((option) => (option.selected = false))
    }
    updateSelectedAnimals()
  }

  function updateSelectedAnimals() {
    selectedAnimals.innerHTML = ""
    let totalWeightValue = 0

    Array.from(animalSelect.selectedOptions).forEach((option) => {
      const animal = availableSheep.find((a) => a.id.toString() === option.value)
      if (animal) {
        const li = document.createElement("li")
        li.className = "list-group-item d-flex justify-content-between align-items-center"
        li.textContent = animal.RP
          ? `RP: ${animal.RP} - ${animal.weight} kg`
          : `ID: ${animal.id} - Purity: ${animal.purity_qualifier} - ${animal.weight} kg`

        if (saleType.value === "individual") {
          const input = document.createElement("input")
          input.type = "number"
          input.className = "form-control form-control-sm w-25"
          input.id = `price_${animal.id}`
          input.name = `price_${animal.id}`
          input.placeholder = "Price"
          input.addEventListener("input", calculateIndividualTotal)
          li.appendChild(input)
        }

        selectedAnimals.appendChild(li)
        totalWeightValue += animal.weight
      }
      option.style.color = "green"
    })

    Array.from(animalSelect.options).forEach((option) => {
      if (!option.selected) {
        option.style.color = ""
      }
    })

    totalWeight.value = totalWeightValue.toFixed(2)
    calculateSlaughterhouseTotal()
  }

  function calculateSlaughterhouseTotal() {
    if (saleType.value === "slaughterhouse") {
      const total = (Number.parseFloat(totalWeight.value) || 0) * (Number.parseFloat(pricePerKg.value) || 0)
      totalSaleValue.value = total.toFixed(2)
    }
  }

  function calculateIndividualTotal() {
    if (saleType.value === "individual") {
      let total = 0
      selectedAnimals.querySelectorAll("input").forEach((input) => {
        total += Number.parseFloat(input.value) || 0
      })
      totalSaleValue.value = total.toFixed(2)
    }
  }

  function updateTotalSaleValue() {
    if (saleType.value === "auction") {
      totalSaleValue.value = remateTotal.value
    }
  }

  function submitSaleForm(event) {
    event.preventDefault()
  
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value
  
    const individualPrices = []
  
    selectedAnimals.querySelectorAll("input").forEach((input) => {
      const animalId = input.id.split("_")[1]
      individualPrices.push({
        animal_id: animalId,
        sale_price: Number.parseFloat(input.value) || 0,
      })
    })
  
    console.log("Individual Prices:", individualPrices)
  
    const URL = `${window.location.origin}/hub/dashboard/ventas/`
    console.log("Fetch URL:", URL)
  
    const saleData = {
      tipo_venta: saleType.value,
      por_lote: batchSale.checked,
      ovinos: Array.from(animalSelect.selectedOptions).map((o) => o.value),
      fecha_venta: saleDate.value,
      valor_total: totalSaleValue.value,
      precio_individual: individualPrices,
    }
  
    if (saleType.value === "slaughterhouse") {
      saleData.peso_total = totalWeight.value
      saleData.precio_kg = pricePerKg.value
    } else if (saleType.value === "auction") {
      saleData.remate_total = remateTotal.value
    }
  
    console.log("Sale data to be sent:", saleData)
  
    fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(saleData),
    })
      .then(async (response) => {
        const contentType = response.headers.get("content-type")
        if (contentType && contentType.includes("application/json")) {
          return response.json()
        }
        const text = await response.text()
        throw new Error(`Server returned non-JSON response: ${text}`)
      })
      .then((data) => {
        if (data.success) {
          console.log("Sale registered successfully:", data)
          window.location.reload()
        } else {
          console.error("Error in sale registration:", data.error)
          alert(`Error: ${data.error}`)
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        alert("An error occurred while processing the sale. Please check the console for details.")
      })
  
    bootstrap.Modal.getInstance(document.getElementById("addSaleModal")).hide()
    document.getElementById("addSaleForm").reset()
  }
  
  
})

