// // Puzzle: What letters get logged to the console?

const letters = ['GLM', 'LO', 'CPMA', 'DRAON', 'ETC', 'I', 'SIC', 'HORT', 'IETR', 'NMI'];
let index = 4;

index = (index + 8) % letters.length;

if (index % 2 === 0) {
  index = index / 2;
} else {
  index = (index * 3 + 1) % letters.length;
}

index = index - letters[index].length;

if (letters[index] === 'LO' || letters[index] === 'ETC') {
  index = (index + 7) % letters.length;
} else {
  index = Math.abs(index - 5);
}

console.log(letters[index]);
