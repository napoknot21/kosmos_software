// This variable holds the URL of the server where the backend is hosted
let serverUrl = "http://10.42.0.1:5000";
// Alternative server URL (commented out)
// let serverUrl = "http://10.29.225.198:5000";

// This variable tracks the state of live video streaming
let live = false;

// Function to send a start request to the server
async function start() {
  // update the campagne metadata on the server
  try {
    const postResponse = await fetch(serverUrl + "/changeCampagne", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: localStorage.getItem('metadata')
    });

    const campagneData = await postResponse.json();

    // Assuming the response structure is { status: "ok" }
    if (campagneData.status === "ok") {
      console.log("Campagne metadata updated on the server");
    } else {
      throw new Error(`Failed to update campagne metadata on the server : ${campagneData.status}`);
    }
    const response = await fetch(serverUrl + "/start");
    if (!response.ok) {
      throw new Error(`Erreur du serveur : ${response.status}`);
    }

    const body = await response.json();  
    if (body.video_path) {
      // stocking the video path in the local storage
      localStorage.setItem('video_path', body.video_path);
    } else {
      console.error("Chemin de la vidéo non trouvé dans la réponse.");
    }
  } catch (error) {
    console.error("Error starting the video : ",error)
  }
}

// Function to send a stop request to the server
async function stop() {
  const response = await fetch(serverUrl + "/stop");
  const body = await response.json();
  // Redirect to the Metadata page after the stop request is successful
  if(body.status == "ok")
    window.location.href = "./metadata.html";

  console.log(body);
}

// Function to send a shutdown request to the server
async function shutdown() {
  const response = await fetch(serverUrl + "/shutdown");
  const body = await response.json();
  console.log(body);
}

// Function to fetch an image from the server and display it
async function getImage() {
  const response = await fetch(serverUrl + "/frame");
  const imageBlob = await response.blob();
  const imageObjectURL = URL.createObjectURL(imageBlob);
  const image = document.getElementById("frame");
  image.src = imageObjectURL;
}

// Function to set the live streaming state based on camera state
async function setLive(state) {
  try {
    const response = await fetch(serverUrl + "/state");
    const body = await response.json();

    if (state) {
      if (body.state === "KState.STANDBY") {
        live = true;
        frameLoop();
      } else {
        alert(
          "Cannot start live video while the camera is not in STANDBY state."
        );
      }
    } else {
      live = false;
    }
  } catch (error) {
    console.error("Error fetching camera state:", error);
  }
}


// Function to continuously fetch and display frames in a loop
async function frameLoop() {
  while (live) {
    await getImage();
  } 
}
