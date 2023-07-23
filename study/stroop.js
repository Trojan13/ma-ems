const colors = ["Red", "Blue", "Green", "Yellow"];
const roundsContainer = document.getElementById("rounds");

let seed = 4; // Can be any integer
function seededRandom() {
  let x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
}

function shuffleArray(array, seed) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(seededRandom(seed) * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function generateLatinSquare(n) {
  return Array.from({ length: n }, (_, i) =>
    Array.from(
      { length: colors.length },
      (_, j) => colors[(i + j) % colors.length]
    )
  );
}

function generateColorOrder(n, type) {
  if (type === "latin") {
    return generateLatinSquare(n);
  }
  // Default to "random"
  return Array.from({ length: n }, () => shuffleArray([...colors], seed));
}

function createButton(buttonColor, outputColor, remainingColors, isCorrect) {
  const buttonText = remainingColors.splice(
    Math.floor(seededRandom() * remainingColors.length),
    1
  )[0];
  const textColor = isCorrect ? outputColor : remainingColors[0];

  if (buttonColor === textColor) {
    // set buttonColor to a different color
    buttonColor = remainingColors[1];
  }

  return {
    buttonColor: buttonColor,
    buttonText: buttonText,
    textColor: textColor,
    isCorrect: isCorrect,
  };
}

function createRound(i, colorOrder) {
  const currentColorOrder = colorOrder[i % colorOrder.length];
  const outputColor =
    currentColorOrder[Math.floor(seededRandom() * currentColorOrder.length)];
  const correctButtonIndex = Math.floor(
    seededRandom() * currentColorOrder.length
  );

  const buttons = currentColorOrder.map((color, index) => {
    let remainingColors = [...currentColorOrder];
    remainingColors.splice(index, 1);
    if (index !== correctButtonIndex) {
      const outputColorIndex = remainingColors.indexOf(outputColor);
      if (outputColorIndex > -1) {
        remainingColors.splice(outputColorIndex, 1);
      }
    }
    return createButton(
      color,
      outputColor,
      remainingColors,
      index === correctButtonIndex
    );
  });

  return {
    roundNumber: i + 1,
    outputColor: outputColor,
    buttons: buttons,
  };
}

function generateButtonStructure(n, type) {
  const colorOrder = generateColorOrder(n, type);
  const rounds = Array.from({ length: n }, (_, i) =>
    createRound(i, colorOrder)
  );

  return { rounds: rounds };
}

function renderRounds(type, count) {
  const testStructure = generateButtonStructure(count, type);
  const rounds = testStructure.rounds;

  // Output the JSON structure
  console.log(JSON.stringify(testStructure, null, 2));
  console.log(checkSequenceForErrors(rounds));
  rounds.forEach((round) => {
    const roundElement = document.createElement("div");
    roundElement.classList.add("round");
    roundElement.innerHTML = `Round ${round.roundNumber}, Output Color: ${round.outputColor}`;

    round.buttons.forEach((button) => {
      const buttonElement = document.createElement("div");
      buttonElement.classList.add("button");
      buttonElement.style.backgroundColor = button.buttonColor;
      buttonElement.style.color = button.textColor;
      buttonElement.innerHTML = button.buttonText;

      roundElement.appendChild(buttonElement);
    });

    roundsContainer.appendChild(roundElement);
  });
}

// Render rounds with "random" color order
renderRounds("random", 50);

// Render rounds with "latin" color order
// renderRounds("latin");

// Helper function to check if only one button is correct and only one button has the output color
function checkSequenceForErrors(rounds) {
  for (let i = 0; i < rounds.length; i++) {
    const round = rounds[i];
    const correctButtons = round.buttons.filter((button) => button.isCorrect);
    const outputColorButtons = round.buttons.filter(
      (button) => round.outputColor === button.textColor
    );
    const sameColorButtons = round.buttons.filter(
      (button) => button.buttonColor === button.textColor
    );

    if (
      correctButtons.length !== 1 ||
      outputColorButtons.length !== 1 ||
      sameColorButtons.length !== 0
    ) {
      console.log(`Round ${round.roundNumber} is incorrect:`);
      console.log(`- Number of correct buttons: ${correctButtons.length}`);
      console.log(
        `- Number of buttons with output color: ${outputColorButtons.length}`
      );
      console.log(
        `- Number of buttons with same button and text color: ${sameColorButtons.length}`
      );
      console.log(round);
      return false;
    }
  }

  return true;
}
