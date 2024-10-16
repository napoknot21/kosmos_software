// Mock JSON file location
const testUrl = "./test.json"; // Ensure this file is placed correctly in your project structure

// Function to fetch metadata from the local mock JSON file
async function fetchMetadata() {
  try {
    const response = await fetch(testUrl); // Fetching the local JSON file
    const data = await response.json(); // Parsing the JSON data
    return data; // Return the parsed data
  } catch (error) {
    console.error("Error fetching mock data:", error);
    return null;
  }
}

// Function to populate the table with metadata and make cells editable (values only)
async function populateMetadataTable() {
  const fileTable = document.getElementById("metadataTable");

  // Fetch metadata from the mock JSON file
  const metadata = await fetchMetadata();

  if (metadata) {
    // CAMPAGNE section
    const campagneData = metadata.campagne;

    // Add a header row for 'Campagne' section
    let row = fileTable.insertRow();
    let headerCell = row.insertCell();
    headerCell.colSpan = 2;
    headerCell.style.fontWeight = 'bold';
    headerCell.textContent = 'Campagne Information';

    // Add Zone Dict row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Zone Information";
    let zoneCell = row.insertCell();
    zoneCell.innerHTML = `
      <label>Campagne:</label> <input type="text" name="campagne" value="${campagneData.zoneDict.campagne}">
      <label>Zone:</label> <input type="text" name="zone" value="${campagneData.zoneDict.zone}">
      <label>Lieu-dit:</label> <input type="text" name="lieudit" value="${campagneData.zoneDict.lieudit}">
      <label>Protection:</label> <input type="text" name="protection" value="${campagneData.zoneDict.protection}">
    `;

    // Add Date Dict row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Date Information";
    let dateCell = row.insertCell();
    dateCell.innerHTML = `
      <label>Date:</label> <input type="text" name="date" value="${campagneData.dateDict.date}">
    `;

    // Add Deploiement Dict row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Déploiement Information";
    let deploiementCell = row.insertCell();
    deploiementCell.innerHTML = `
      <label>Bateau:</label> <input type="text" name="bateau" value="${campagneData.deploiementDict.bateau}">
      <label>Pilote:</label> <input type="text" name="pilote" value="${campagneData.deploiementDict.pilote}">
      <label>Equipage:</label> <input type="text" name="equipage" value="${campagneData.deploiementDict.equipage}">
      <label>Partenaires:</label> <input type="text" name="partenaires" value="${campagneData.deploiementDict.partenaires}">
    `;

    // VIDEO section
    const videoData = metadata.video;

    // Add a header row for 'Video' section
    row = fileTable.insertRow();
    headerCell = row.insertCell();
    headerCell.colSpan = 2;
    headerCell.style.fontWeight = 'bold';
    headerCell.textContent = 'Video Information';

    // Add Code Station row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Code Station";
    let codeStationCell = row.insertCell();
    let codeStationInput = document.createElement("input");
    codeStationInput.type = "text";
    codeStationInput.name = "codeStation";
    codeStationInput.value = videoData.codeStation;
    codeStationCell.appendChild(codeStationInput);

    // Add Heure row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Heure";
    let heureCell = row.insertCell();
    heureCell.innerHTML = `
      <label>Heure:</label> <input type="text" name="heure" value="${videoData.heureDict.heure}">
      <label>Minute:</label> <input type="text" name="minute" value="${videoData.heureDict.minute}">
      <label>Seconde:</label> <input type="text" name="seconde" value="${videoData.heureDict.seconde}">
    `;

    // Add GPS row with latitude and longitude
    row = fileTable.insertRow();
    row.insertCell().textContent = "GPS Coordinates";
    let gpsCell = row.insertCell();
    gpsCell.innerHTML = `
      <label>Latitude:</label> <input type="text" name="latitude" value="${videoData.gpsDict.latitude}">
      <label>Longitude:</label> <input type="text" name="longitude" value="${videoData.gpsDict.longitude}">
    `;

    // Add CTD row with profondeur and temperature
    row = fileTable.insertRow();
    row.insertCell().textContent = "CTD (Profondeur / Température)";
    let ctdCell = row.insertCell();
    ctdCell.innerHTML = `
      <label>Profondeur:</label> <input type="text" name="profondeur" value="${videoData.ctdDict.profondeur}">
      <label>Température:</label> <input type="text" name="temperature" value="${videoData.ctdDict.temperature}">
    `;

    // Add Astro row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Astro (Lune / Marée)";
    let astroCell = row.insertCell();
    astroCell.innerHTML = `
      <label>Lune:</label> <input type="text" name="lune" value="${videoData.astroDict.lune}">
      <label>Marée:</label> <input type="text" name="maree" value="${videoData.astroDict.maree}">
      <label>Coefficient:</label> <input type="text" name="coefficient" value="${videoData.astroDict.coefficient}">
    `;

    // Add Météo Air row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Météo Air (Ciel / Vent)";
    let meteoAirCell = row.insertCell();
    meteoAirCell.innerHTML = `
      <label>Ciel:</label> <input type="text" name="ciel" value="${videoData.meteoAirDict.ciel}">
      <label>Vent:</label> <input type="text" name="vent" value="${videoData.meteoAirDict.vent}">
      <label>Direction:</label> <input type="text" name="direction" value="${videoData.meteoAirDict.direction}">
      <label>Température:</label> <input type="text" name="tempAir" value="${videoData.meteoAirDict.tempAir}">
    `;

    // Add Météo Mer row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Météo Mer (État de la Mer / Houle)";
    let meteoMerCell = row.insertCell();
    meteoMerCell.innerHTML = `
      <label>État Mer:</label> <input type="text" name="etatMer" value="${videoData.meteoMerDict.etatMer}">
      <label>Houle:</label> <input type="text" name="houle" value="${videoData.meteoMerDict.houle}">
    `;

    // Add Analyse row
    row = fileTable.insertRow();
    row.insertCell().textContent = "Analyse (Exploitabilité / Habitat / Faune)";
    let analyseCell = row.insertCell();
    analyseCell.innerHTML = `
      <label>Exploitabilité:</label> <input type="text" name="exploitabilite" value="${videoData.analyseDict.exploitabilite}">
      <label>Habitat:</label> <input type="text" name="habitat" value="${videoData.analyseDict.habitat}">
      <label>Faune:</label> <input type="text" name="faune" value="${videoData.analyseDict.faune}">
    `;
  } else {
    console.error("No data available to populate the table.");
  }
}

// Function to collect data from input fields and send to server
function confirmChanges() {
  // Collect data from input fields
  const updatedData = {
    campagne: {
      zoneDict: {
        campagne: document.querySelector('input[name="campagne"]').value,
        zone: document.querySelector('input[name="zone"]').value,
        lieudit: document.querySelector('input[name="lieudit"]').value,
        protection: document.querySelector('input[name="protection"]').value,
      },
      dateDict: {
        date: document.querySelector('input[name="date"]').value,
      },
      deploiementDict: {
        bateau: document.querySelector('input[name="bateau"]').value,
        pilote: document.querySelector('input[name="pilote"]').value,
        equipage: document.querySelector('input[name="equipage"]').value,
        partenaires: document.querySelector('input[name="partenaires"]').value,
      },
    },
    video: {
      codeStation: document.querySelector('input[name="codeStation"]').value,
      heureDict: {
        heure: document.querySelector('input[name="heure"]').value,
        minute: document.querySelector('input[name="minute"]').value,
        seconde: document.querySelector('input[name="seconde"]').value,
      },
      gpsDict: {
        latitude: parseFloat(document.querySelector('input[name="latitude"]').value),
        longitude: parseFloat(document.querySelector('input[name="longitude"]').value),
      },
      ctdDict: {
        profondeur: parseFloat(document.querySelector('input[name="profondeur"]').value),
        temperature: parseFloat(document.querySelector('input[name="temperature"]').value),
      },
      astroDict: {
        lune: document.querySelector('input[name="lune"]').value,
        maree: document.querySelector('input[name="maree"]').value,
        coefficient: parseInt(document.querySelector('input[name="coefficient"]').value),
      },
      meteoAirDict: {
        ciel: document.querySelector('input[name="ciel"]').value,
        vent: parseInt(document.querySelector('input[name="vent"]').value),
        direction: document.querySelector('input[name="direction"]').value,
        tempAir: parseFloat(document.querySelector('input[name="tempAir"]').value),
      },
      meteoMerDict: {
        etatMer: document.querySelector('input[name="etatMer"]').value,
        houle: parseInt(document.querySelector('input[name="houle"]').value),
      },
      analyseDict: {
        exploitabilite: document.querySelector('input[name="exploitabilite"]').value,
        habitat: document.querySelector('input[name="habitat"]').value,
        faune: document.querySelector('input[name="faune"]').value,
      },
    },
  };

  const videoPath = localStorage.getItem('video_path');
  if (videoPath) {
    updatedData.video_path = videoPath;
    localStorage.removeItem('video_path');
  }
  // Send updated data to server
  fetch('/update-metadata', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedData),
  })
    .then((response) => {
      if (response.ok) {
        alert('Metadata updated successfully!');
      } else {
        alert('Failed to update metadata.');
      }
    })
    .catch((error) => {
      console.error('Error updating metadata:', error);
      alert('An error occurred while updating metadata.');
    });
}

// Add event listener to Confirm button
document.getElementById('confirmButton').addEventListener('click', confirmChanges);

// Call the function to populate the table when the page loads
populateMetadataTable();
