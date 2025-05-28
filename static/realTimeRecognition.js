// Ambil elemen DOM
const video = document.getElementById('video');
const resultElement = document.getElementById('result'); // Ganti nama agar tidak bentrok dengan variabel 'result'
const uploadRefInput = document.getElementById('uploadRef'); // Ganti nama agar tidak bentrok
const previewImage = document.getElementById('preview'); // Ganti nama agar tidak bentrok
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const matchButton = document.getElementById('matchButton'); // Tambahkan ID ke tombol "Face Match" di HTML
const detectorModelSelectRt = document.getElementById('detector-model-rt');
const recognitionModelSelectRt = document.getElementById('recognition-model-rt');

let stream = null; // Untuk menyimpan stream kamera

// Fungsi untuk memulai kamera
async function startCamera() {
    try {
        if (stream) { // Jika stream sudah ada, hentikan dulu
            stream.getTracks().forEach(track => track.stop());
        }
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        resultElement.textContent = "Kamera aktif. Klik 'Face Match' untuk membandingkan.";
        startButton.disabled = true;
        stopButton.disabled = false;
        matchButton.disabled = false;
    } catch (err) {
        console.error("Kesalahan webcam:", err);
        resultElement.textContent = "Gagal mengakses kamera: " + err.message;
        startButton.disabled = false;
        stopButton.disabled = true;
        matchButton.disabled = true;
    }
}

// Fungsi untuk menghentikan kamera
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        stream = null;
        resultElement.textContent = "Kamera tidak aktif.";
        startButton.disabled = false;
        stopButton.disabled = true;
        matchButton.disabled = true;
    }
}

// Event listener untuk tombol
startButton.addEventListener('click', startCamera);
stopButton.addEventListener('click', stopCamera);

// Event listener untuk unggah gambar referensi
uploadRefInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
        uploadReferenceImage(file); // Langsung unggah saat file dipilih
    }
});

// Fungsi untuk mengunggah gambar referensi
async function uploadReferenceImage(file) {
    const formData = new FormData();
    formData.append("file", file);
    resultElement.textContent = "Mengunggah gambar referensi...";
    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        if (response.ok) {
            resultElement.textContent = "Gambar referensi berhasil diunggah. " + (stream ? "Klik 'Face Match'." : "Aktifkan kamera dulu.");
        } else {
            resultElement.textContent = `Gagal mengunggah: ${data.error || 'Kesalahan tidak diketahui'}`;
        }
        console.log("Respons unggah:", data);
    } catch (err) {
        console.error("Unggah gagal:", err);
        resultElement.textContent = "Gagal mengunggah gambar referensi.";
    }
}

// Fungsi untuk memicu pencocokan wajah
matchButton.addEventListener('click', async () => {
    if (!stream || video.readyState !== video.HAVE_ENOUGH_DATA) {
        resultElement.textContent = "Kamera belum siap atau tidak aktif.";
        return;
    }
    if (!previewImage.src || previewImage.src.startsWith('http')) { // Cek apakah gambar referensi sudah ada
        resultElement.textContent = "Silakan unggah gambar referensi terlebih dahulu.";
        return;
    }


    resultElement.textContent = "Memproses...";
    matchButton.disabled = true;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameDataUrl = canvas.toDataURL('image/jpeg');

    const detectorModel = detectorModelSelectRt.value;
    const recognitionModel = recognitionModelSelectRt.value;

    try {
        const response = await fetch("/realtime_verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                frame_data: frameDataUrl,
                detector_backend: detectorModel,
                model_name: recognitionModel,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            if (data.error) {
                 resultElement.textContent = `Error: ${data.error}`;
            } else if (data.verified !== undefined) {
                resultElement.textContent = data.verified 
                    ? `COCOK ✅ (jarak: ${data.distance ? data.distance.toFixed(4) : 'N/A'})` 
                    : `TIDAK COCOK ❌ (jarak: ${data.distance ? data.distance.toFixed(4) : 'N/A'})`;
            } else {
                resultElement.textContent = "Respons tidak dikenali dari server.";
            }
        } else {
            resultElement.textContent = `Kesalahan server: ${data.error || response.statusText}`;
        }
    } catch (err) {
        console.error("Kesalahan saat mencocokkan:", err);
        resultElement.textContent = "Gagal melakukan pencocokan: " + err.message;
    } finally {
        matchButton.disabled = false; // Aktifkan kembali tombol setelah selesai
    }
});

// Inisialisasi kondisi tombol
stopButton.disabled = true;
matchButton.disabled = true;
resultElement.textContent = "Silakan aktifkan kamera dan unggah gambar referensi.";

