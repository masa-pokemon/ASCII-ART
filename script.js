const imageInput = document.getElementById("imageInput");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const asciiOutput = document.getElementById("asciiOutput");

const asciiChars = "@%#*+=-:. "; // 明るさに応じた文字

imageInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    const img = new Image();
    img.onload = function () {
      const width = 100;
      const height = (img.height / img.width) * width;

      canvas.width = width;
      canvas.height = height;

      ctx.drawImage(img, 0, 0, width, height);
      const imageData = ctx.getImageData(0, 0, width, height).data;

      let ascii = "";
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const offset = (y * width + x) * 4;
          const r = imageData[offset];
          const g = imageData[offset + 1];
          const b = imageData[offset + 2];

          const brightness = (r + g + b) / 3;
          const charIndex = Math.floor((brightness / 255) * (asciiChars.length - 1));
          ascii += asciiChars[charIndex];
        }
        ascii += "\n";
      }

      asciiOutput.textContent = ascii;
    };
    img.src = e.target.result;
  };

  reader.readAsDataURL(file);
});
