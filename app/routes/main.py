from flask import Blueprint, render_template, redirect, session, url_for, request
from openai import OpenAI

main = Blueprint('main', __name__)

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key="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",
)

@main.route('/')
def index():
    session.pop('frase', None)
    return render_template('index.html')

@main.route('/gerar_frase')
def gerar_frase():
    try:
        resposta = client.completions.create(
            model="openai/gpt-4.1",
            prompt="Crie uma frase bem curta, engraçada e irônica. A frase deve ter até 10 palavras e fazer sentido. Não adicione explicações, apenas a frase.",
            max_tokens=25,
            temperature=1.4
        )
        frase_gerada = resposta.choices[0].text.strip()
        session['frase'] = frase_gerada
        return redirect(url_for('main.history'))
        
    except Exception as erro:
        session['frase'] = f"Erro ao gerar frase: {erro}"
        return redirect(url_for('main.history'))

@main.route('/history')
def history():
    frase = session.get('frase', None)
    return render_template('history.html', frase=frase)

@main.route('/resultado' , methods=['POST'])
def resultado():
    frase = session.get('frase', None)
    historia = request.form.get('historia')


    resultado = client.completions.create(
        model="openai/gpt-4.1",
        prompt=f"De acordo com a história: {historia}, gostaria que você avaliasse a história rigorosamente em alguns pontos: 📚 Coerência, 😂 Engraçado/Divertido, 🧠 Criatividade, 📝 Ortografia, 🎯 Moral ou mensagem, 🔗 Relação com a frase: {frase} A avaliação deve ser feita em uma escala de 0 a 10, onde 0 é o pior e 10 é o melhor. Explique de forma bem breve o motivo da nota. Exemplo: 📚 Coerência: 8 - Pois é uma leitura fácil e não é confusa. 😂 Engraçado/Divertido: 9 - Pois faz uso de ironia e humor de forma leve e engraçada. (...) ATENÇÃO: TIRE OS '**' DA AVALIAÇÃO. no número 6, apenas diga a nota e o motivo sem repetir a frase. Depois, faça a média das notas (Ex: 🔢 Média final: 8) APENAS DÊ AS NOTAS, A MÉDIA E OS MOTIVOS!",
        max_tokens=250,
        temperature=0
    )

    return render_template('result.html', frase=frase, historia=historia, resultado=resultado.choices[0].text.strip())