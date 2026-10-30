/* ==========================================================================
   Dial In
   ========================================================================== */

const WORD_LENGTH = 10;
const MAX_ATTEMPTS = 3;
const MULTI_TAP_MS = 1000;   // how long a key keeps cycling letters before it locks in
const REVEAL_STEP_MS = 70;   // delay between each tile flip

const KEYPAD = {
    '2': 'ABC', '3': 'DEF',
    '4': 'GHI', '5': 'JKL', '6': 'MNO',
    '7': 'PQRS', '8': 'TUV', '9': 'WXYZ',
    '0': ' '
};

// Real touch-tone frequencies (low, high) for each key
const DTMF = {
    '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
    '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
    '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
    '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
};

const gameNumber = document.body.dataset.gameNumber;

let remainingAttempts = MAX_ATTEMPTS;
let emojiFeedbackGrid = [];
let gameOver = false;
let submitting = false;

// Current guess
let letters = new Array(WORD_LENGTH).fill(null);
let cursor = 0;
let pending = null;          // { key, index, cycle } while a key is mid multi-tap
let pendingTimer = null;

// Timer
let timerStarted = false;
let timerInterval = null;
let startTime = null;
let totalTime = 0; // in seconds

// Results
let finalWinStatus = null;
let finalTotalSeconds = null;
let finalAnswerWord = "";
let fullShareText = "";

const $ = id => document.getElementById(id);


/* ==========================================================================
   Input grid
   ========================================================================== */

function createInputGrid() {
    const inputGrid = $("guess-input-grid");
    inputGrid.innerHTML = "";

    for (let i = 0; i < WORD_LENGTH; i++) {
        const cell = document.createElement("div");
        cell.classList.add("grid-cell", "input-cell");
        cell.dataset.index = i;
        cell.addEventListener("click", () => moveCursorTo(i));
        inputGrid.appendChild(cell);
    }
    renderInput();
}

function inputCells() {
    return document.querySelectorAll(".input-cell");
}

function renderInput() {
    const cells = inputCells();
    cells.forEach((cell, i) => {
        const letter = letters[i];
        cell.textContent = letter && letter !== " " ? letter : "";
        cell.classList.toggle("filled", letter !== null);
        cell.classList.toggle("is-space", letter === " ");
        cell.classList.toggle("active-cell", i === cursor && !gameOver);
        if (!pending || pending.index !== i) cell.classList.remove("pending");
    });
    checkInput();
}

function checkInput() {
    const submitBtn = $("submit-btn");
    const isValid = letters.every(l => l !== null);

    submitBtn.disabled = !isValid;
    submitBtn.classList.toggle("disabled", !isValid);
    submitBtn.classList.toggle("active", isValid);

    $("delete-btn").classList.toggle("empty", letters.every(l => l === null));
}

function popCell(index) {
    const cell = inputCells()[index];
    if (!cell) return;
    cell.classList.remove("pop");
    void cell.offsetWidth; // restart animation
    cell.classList.add("pop");
}

function markPending(index) {
    const cell = inputCells()[index];
    if (!cell) return;
    cell.classList.remove("pending");
    void cell.offsetWidth; // restart the countdown bar
    cell.classList.add("pending");
}

function shakeInput() {
    const grid = $("guess-input-grid");
    if (!grid) return;
    grid.classList.remove("shake");
    void grid.offsetWidth;
    grid.classList.add("shake");
}


/* ==========================================================================
   Typing
   ========================================================================== */

function commitPending() {
    clearTimeout(pendingTimer);
    pendingTimer = null;
    pending = null;
}

function armPending() {
    clearTimeout(pendingTimer);
    pendingTimer = setTimeout(() => {
        commitPending();
        renderInput();
    }, MULTI_TAP_MS);
}

// Phone-style multi-tap: repeated taps on the same key cycle its letters
function pressDigit(digit) {
    if (!canType()) return;

    const chars = KEYPAD[digit];
    if (!chars) {
        shakeInput();
        return;
    }

    if (pending && pending.key === digit) {
        pending.cycle = (pending.cycle + 1) % chars.length;
        letters[pending.index] = chars[pending.cycle];
        renderInput();
        markPending(pending.index);
        popCell(pending.index);
        armPending();
        return;
    }

    commitPending();

    if (cursor >= WORD_LENGTH) {
        shakeInput();
        return;
    }

    const index = cursor;
    letters[index] = chars[0];
    cursor = index + 1;

    if (chars.length > 1) {
        pending = { key: digit, index, cycle: 0 };
        armPending();
    }

    renderInput();
    if (pending) markPending(index);
    popCell(index);
}

// Physical keyboard: letters go straight in
function typeLetter(letter) {
    if (!canType()) return;
    commitPending();

    if (cursor >= WORD_LENGTH) {
        shakeInput();
        return;
    }

    letters[cursor] = letter;
    const index = cursor;
    cursor++;
    renderInput();
    popCell(index);
}

function deleteLetter() {
    if (!canType()) return;
    commitPending();

    if (cursor < WORD_LENGTH && letters[cursor] !== null) {
        letters[cursor] = null;
    } else if (cursor > 0) {
        cursor--;
        letters[cursor] = null;
    }
    renderInput();
}

function clearGuess() {
    if (!canType()) return;
    commitPending();
    letters.fill(null);
    cursor = 0;
    renderInput();
}

// "#": lock in the cycling letter, or step forward a cell
function nextCell() {
    if (!canType()) return;
    if (pending) {
        commitPending();
    } else if (cursor < WORD_LENGTH) {
        cursor++;
    }
    renderInput();
}

function moveCursorTo(index) {
    if (!canType()) return;
    commitPending();
    cursor = Math.max(0, Math.min(WORD_LENGTH, index));
    renderInput();
}

function canType() {
    return !gameOver && !submitting && !isAnyModalOpen();
}


/* ==========================================================================
   Keypad
   ========================================================================== */

function handleKeypadAction(key) {
    playTone(key);
    buzz();

    if (key === "*") clearGuess();
    else if (key === "#") nextCell();
    else pressDigit(key);
}

function flashKey(key) {
    const button = document.querySelector(`.key[data-key="${CSS.escape(key)}"]`);
    if (!button) return;
    button.classList.add("pressed");
    setTimeout(() => button.classList.remove("pressed"), 120);
}

// Fire on pointerdown for a snappy, phone-like feel; keep click for keyboard activation
function bindPress(element, action) {
    element.addEventListener("pointerdown", event => {
        if (event.button !== 0) return;
        event.preventDefault();
        element.classList.add("pressed");
        action();
    });

    const release = () => element.classList.remove("pressed");
    element.addEventListener("pointerup", release);
    element.addEventListener("pointerleave", release);
    element.addEventListener("pointercancel", release);

    element.addEventListener("click", event => {
        if (event.detail === 0) action(); // Enter / Space on a focused button
    });
}

function setupKeypad() {
    document.querySelectorAll(".keypad .key").forEach(button => {
        bindPress(button, () => handleKeypadAction(button.dataset.key));
    });

    bindPress($("delete-btn"), () => {
        buzz();
        deleteLetter();
    });

    bindPress($("submit-btn"), () => {
        if (!$("submit-btn").disabled) submitGuess();
    });
}


/* ==========================================================================
   Sound + haptics
   ========================================================================== */

let audioCtx = null;
let soundOn = localStorage.getItem("dialin-sound") !== "off";

function playTone(key) {
    if (!soundOn || !DTMF[key]) return;

    try {
        audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === "suspended") audioCtx.resume();

        const now = audioCtx.currentTime;
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.07, now + 0.01);
        gain.gain.setValueAtTime(0.07, now + 0.1);
        gain.gain.linearRampToValueAtTime(0, now + 0.14);
        gain.connect(audioCtx.destination);

        DTMF[key].forEach(freq => {
            const osc = audioCtx.createOscillator();
            osc.type = "sine";
            osc.frequency.value = freq;
            osc.connect(gain);
            osc.start(now);
            osc.stop(now + 0.15);
        });
    } catch (err) {
        // Audio is a nice-to-have; ignore failures
    }
}

function buzz() {
    if (navigator.vibrate) navigator.vibrate(8);
}

function renderSoundToggle() {
    $("sound-toggle").classList.toggle("muted", !soundOn);
}

$("sound-toggle").addEventListener("click", () => {
    soundOn = !soundOn;
    localStorage.setItem("dialin-sound", soundOn ? "on" : "off");
    renderSoundToggle();
});


/* ==========================================================================
   Guessing
   ========================================================================== */

function submitGuess() {
    if (gameOver || submitting) return;
    commitPending();

    if (letters.some(l => l === null)) {
        shakeInput();
        return;
    }

    const guess = letters.join("");
    submitting = true;

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            guess: guess,
            remainingAttempts: remainingAttempts
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.result === "error") {
            console.error("Invalid submission:", data.message);
            submitting = false;
            shakeInput();
            return;
        }

        if (data.word) {
            finalAnswerWord = data.word;
        }

        let emojiRow = "";
        for (let i = 0; i < guess.length; i++) {
            emojiRow += data.matches.includes(i) ? "🟩" : "⬛️";
        }
        emojiFeedbackGrid.push(emojiRow);

        remainingAttempts = Math.max(0, remainingAttempts - 1);
        const dot = $("dot" + (remainingAttempts + 1));
        if (dot) dot.classList.add("used");

        const isWin = data.result === "correct";
        const isLast = isWin || remainingAttempts <= 0;

        if (isLast) {
            gameOver = true;
            finalTotalSeconds = stopGameTimer();
        }

        const row = displayGuess(guess, data.matches);
        letters.fill(null);
        cursor = 0;

        if (isLast) {
            removeInputGrid();
        } else {
            renderInput();
        }

        const revealTime = WORD_LENGTH * REVEAL_STEP_MS + 400;
        setTimeout(() => {
            submitting = false;
            if (isLast) {
                if (isWin) row.classList.add("win");
                setTimeout(() => endGame(isWin), isWin ? 700 : 300);
            }
        }, revealTime);
    })
    .catch(err => {
        console.error("Guess submission failed:", err);
        submitting = false;
    });
}

function displayGuess(guessString, matchIndexes = []) {
    const guessContainer = $("guess-container");
    const guessRow = document.createElement("div");
    guessRow.classList.add("guess-row");

    guessString.split("").forEach((letter, index) => {
        const cell = document.createElement("div");
        cell.classList.add("grid-cell");
        cell.textContent = letter === " " ? "" : letter;
        if (letter === " ") cell.classList.add("is-space");

        const delay = index * REVEAL_STEP_MS;
        cell.style.animationDelay = `${delay}ms`;
        cell.classList.add("reveal");

        // Swap the color at the midpoint of the flip
        setTimeout(() => {
            cell.classList.add(matchIndexes.includes(index) ? "correct" : "incorrect");
        }, delay + 180);

        guessRow.appendChild(cell);
    });

    guessContainer.appendChild(guessRow);

    const board = $("board");
    requestAnimationFrame(() => {
        board.scrollTo({ top: board.scrollHeight, behavior: "smooth" });
    });

    return guessRow;
}

function removeInputGrid() {
    const inputGrid = $("guess-input-grid");
    if (inputGrid) inputGrid.remove();
}

function endGame(isWin) {
    finalWinStatus = isWin;

    $("game-container").classList.add("game-over");
    $("share-btn").classList.remove("hidden-share");

    showShareablePopup(isWin, finalTotalSeconds);
}


/* ==========================================================================
   Results
   ========================================================================== */

function showShareablePopup(isWin, totalSeconds) {
    let message;
    if (!isWin) {
        message = "Better luck next time!";
    } else if (remainingAttempts === 2) {
        message = "You're a star. Mom and Dad would be proud";
    } else if (remainingAttempts === 1) {
        message = "Super!";
    } else {
        message = "Get it together man";
    }

    const emojiGrid = emojiFeedbackGrid.join("\n");

    if (isWin) {
        fullShareText = `DIAL IN #${gameNumber} solved in ${formatTime(totalSeconds)}!\n${emojiGrid}`;
        $("final-time").textContent = `Solved in ${formatTime(totalSeconds)}`;
    } else {
        fullShareText = `DIAL IN #${gameNumber} defeated me!\n${emojiGrid}`;
        $("final-time").textContent = "";
    }

    $("shareable-text").innerText = fullShareText;
    $("popup-message").innerText = message;
    $("code-word").innerText = finalAnswerWord ? `"${finalAnswerWord}"` : "";

    openModal("shareable-popup");
}

function shareResults() {
    const fullMessage = `${fullShareText}\nhttps://dialin.fun`;

    if (navigator.share) {
        navigator.share({ text: fullMessage }).catch(err => {
            if (err.name !== "AbortError") console.error("Web Share failed:", err);
        });
    } else {
        copyText(fullMessage);
    }
}

function copyText(text) {
    const done = () => {
        const msg = $("copy-message");
        msg.classList.add("show");
        setTimeout(() => msg.classList.remove("show"), 2000);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done).catch(err => console.error("Copy failed:", err));
        return;
    }

    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.select();
    try {
        document.execCommand("copy");
        done();
    } catch (err) {
        console.error("Fallback copy failed:", err);
    }
    document.body.removeChild(textArea);
}

$("SHARE-RESULTS-BUTTON").addEventListener("click", shareResults);
$("COPY-RESULTS-BUTTON").addEventListener("click", () => copyText(`${fullShareText}\nhttps://dialin.fun`));
$("share-btn").addEventListener("click", () => showShareablePopup(finalWinStatus, finalTotalSeconds));

function updateCountdown() {
    const now = new Date();
    const chicagoNow = new Date(now.toLocaleString('en-US', { timeZone: 'America/Chicago' }));

    const tomorrow = new Date(chicagoNow);
    tomorrow.setDate(chicagoNow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);

    const diffMs = (tomorrow - chicagoNow) + 60000; // add 1 minute
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    $("countdown-hours").textContent = `${hours} hour${hours !== 1 ? 's' : ''}`;
    $("countdown-minutes").textContent = `${minutes} minute${minutes !== 1 ? 's' : ''}`;
}
updateCountdown();
setInterval(updateCountdown, 60000);


/* ==========================================================================
   Timer
   ========================================================================== */

function startGameTimer() {
    if (timerStarted || gameOver) return;
    timerStarted = true;
    startTime = Date.now();

    timerInterval = setInterval(() => {
        totalTime = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(totalTime / 60);
        const seconds = totalTime % 60;
        $("game-timer").textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function stopGameTimer() {
    clearInterval(timerInterval);
    if (startTime) totalTime = Math.floor((Date.now() - startTime) / 1000);
    return totalTime;
}

function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;

    const minText = m === 1 ? "1 min" : `${m} mins`;
    const secText = s === 1 ? "1 sec" : `${s} secs`;

    return m > 0 ? `${minText} ${secText}` : secText;
}


/* ==========================================================================
   Intro + modals
   ========================================================================== */

function openModal(id) {
    ["how-to-play-popup", "shareable-popup"].forEach(other => {
        if (other !== id) $(other).classList.add("hidden");
    });
    $(id).classList.remove("hidden");
}

function closeModal(id) {
    $(id).classList.add("hidden");
}

function isAnyModalOpen() {
    return !$("how-to-play-popup").classList.contains("hidden")
        || !$("shareable-popup").classList.contains("hidden")
        || isIntroVisible();
}

function isIntroVisible() {
    return $("game-intro").style.display !== "none";
}

function closeHowToPlay() {
    closeModal("how-to-play-popup");
    startGameTimer();
}

$("play-btn").addEventListener("click", () => {
    $("game-intro").style.display = "none";
    openModal("how-to-play-popup");
});

$("help-icon").addEventListener("click", () => openModal("how-to-play-popup"));
$("close-how-to-play").addEventListener("click", closeHowToPlay);
$("play-button").addEventListener("click", closeHowToPlay);
$("close-popup").addEventListener("click", () => closeModal("shareable-popup"));

// Tap the dimmed backdrop to close
$("how-to-play-popup").addEventListener("click", event => {
    if (event.target === event.currentTarget) closeHowToPlay();
});
$("shareable-popup").addEventListener("click", event => {
    if (event.target === event.currentTarget) closeModal("shareable-popup");
});


/* ==========================================================================
   Physical keyboard
   ========================================================================== */

document.addEventListener("keydown", event => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;

    const howToOpen = !$("how-to-play-popup").classList.contains("hidden");
    const shareOpen = !$("shareable-popup").classList.contains("hidden");

    if (isIntroVisible()) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("play-btn").click();
        }
        return;
    }

    if (howToOpen) {
        if (event.key === "Enter" || event.key === "Escape") {
            event.preventDefault();
            closeHowToPlay();
        }
        return;
    }

    if (shareOpen) {
        if (event.key === "Escape") closeModal("shareable-popup");
        return;
    }

    if (gameOver) return;

    const key = event.key;

    // A focused button handles its own Enter / Space activation
    if ((key === "Enter" || key === " ") && event.target.closest("button")) return;

    if (key === "Enter") {
        event.preventDefault();
        submitGuess();
    } else if (key === "Backspace") {
        event.preventDefault();
        flashButton($("delete-btn"));
        deleteLetter();
    } else if (key === "ArrowLeft") {
        moveCursorTo(cursor - 1);
    } else if (key === "ArrowRight") {
        moveCursorTo(cursor + 1);
    } else if (/^[a-zA-Z]$/.test(key)) {
        typeLetter(key.toUpperCase());
    } else if (key === " ") {
        event.preventDefault();
        typeLetter(" ");
    } else if (DTMF[key]) {
        // Number keys, * and # work just like the on-screen keypad
        flashKey(key);
        handleKeypadAction(key);
    }
});

function flashButton(button) {
    button.classList.add("pressed");
    setTimeout(() => button.classList.remove("pressed"), 120);
}


/* ==========================================================================
   Init
   ========================================================================== */

document.documentElement.style.setProperty("--multitap-ms", `${MULTI_TAP_MS}ms`);
createInputGrid();
setupKeypad();
renderSoundToggle();
