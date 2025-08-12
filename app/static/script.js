function selecionarDificuldade() {
    const dificuldade = document.getElementById("dificuldade").value;
    const tempo = document.getElementById("tempo");
    const caracteres = document.getElementById("caracteres");

    tempo.disabled = true;
    caracteres.disabled = true;

    if (dificuldade === "Fácil") {
        tempo.value = "300";
        caracteres.value = "500";

    } 
    else if (dificuldade === "Médio") {
        tempo.value = "180";
        caracteres.value = "300";

    } 
    else if (dificuldade === "Difícil") {
        tempo.value = "120";
        caracteres.value = "200";

    } 
    else {
        tempo.disabled = false;
        caracteres.disabled = false;
    }
}