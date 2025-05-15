function comecarHistoria() {
    formHistoria = document.getElementById("formHistoria");
    formHistoria.style.display = "block";

    comecarHistoria = document.getElementById("comecarHistoria");
    comecarHistoria.style.display = "none";

    timerText = document.getElementById("timerText");
    timerText.style.display = "block";
    
    let tempoRestante = 30;
    const timerDisplay = document.getElementById("timer");
    const textarea = document.querySelector('textarea');

    function atualizarTimer() {
        const minutos = Math.floor(tempoRestante / 60).toString().padStart(2, '0');
        const segundos = (tempoRestante % 60).toString().padStart(2, '0');
        timerDisplay.textContent = `${minutos}:${segundos}`;

        if (tempoRestante <= 0) {
            clearInterval(intervalo);
            textarea.readOnly = true;
            timerDisplay.textContent = "Tempo esgotado!";
        }

        tempoRestante--;
    }

    const intervalo = setInterval(atualizarTimer, 1000);
    atualizarTimer();
};

function dificuldade() {
    alert('oi')
    selectDificuldade = document.getElementById("dificuldade");
    if (selectDificuldade.value == "facil") {
        alert('Você escolheu a dificuldade fácil! Boa sorte!');
    }
}