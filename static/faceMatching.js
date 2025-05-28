async function sendImages() {
  const refInput = document.getElementById("ref-input").files[0];
  const targetInput = document.getElementById("target-input").files[0];
  const detectorModel = document.getElementById("detector-model").value; // Get detector model
  const recognitionModel = document.getElementById("recognition-model").value; // Get recognition model

  if (!refInput || !targetInput) {
    alert("Please select both images.");
    return;
  }

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  const refImgBase64 = await toBase64(refInput);
  const targetImgBase64 = await toBase64(targetInput);

  const res = await fetch("/match", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ref_img: refImgBase64,
      target_img: targetImgBase64,
      user_id: "web-user",
      detector_backend: detectorModel, // Send detector model
      model_name: recognitionModel      // Send recognition model
    })
  });

  const result = await res.json();
  document.getElementById("result").innerText = JSON.stringify(result, null, 2);
}