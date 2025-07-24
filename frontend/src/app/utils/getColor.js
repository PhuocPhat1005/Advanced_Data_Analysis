const niceColors = [
  "#F0561D",
  "#DCA614",
  "#37A3A3",
  "#63993D",
  "#876FD4",
];

function shuffle(array) {
  // Fisher–Yates shuffle
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Generator: trả về từng màu không trùng, tự shuffle khi hết
export function* colorGenerator() {
  let colors = [...niceColors];
  while (true) {
    shuffle(colors);
    for (const color of colors) {
      yield color;
    }
  }
}
