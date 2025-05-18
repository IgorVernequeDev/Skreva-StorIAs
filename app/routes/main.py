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
    
    dificuldade = session.get('dificuldade')
    
    if dificuldade is None:
        dificuldade = 'Médio' 
        
    return render_template('index.html', dificuldade=dificuldade)

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
    dificuldade = session.get('dificuldade')
    
    
    if dificuldade == 'Fácil':
        caracteres = 2000
        tempo = 300
        
    elif dificuldade == 'Médio':
        caracteres = 1000
        tempo = 180
        
    elif dificuldade == 'Difícil':
        caracteres = 500
        tempo = 120
    
    else:
        caracteres = session.get('caracteres')
        tempo = session.get('tempo')
        
        print(f"caracteres: {caracteres}")
        print(f"tempo: {tempo}")
        
    return render_template('history.html', frase=frase, dificuldade=session['dificuldade'], caracteres=caracteres, tempo=tempo)

@main.route('/resultado' , methods=['POST'])
def resultado():
    frase = session.get('frase', None)
    historia = request.form.get('historia')

    resultado = client.completions.create(
        model="openai/gpt-4.1",
        prompt=f"De acordo com a história: {historia}, gostaria que você a avaliasse rigorosamente, como se fosse uma prova de faculdade, a história deve ter começo, meio e fim. Com introdução, desenvolvimento e conclusão. Avalie-a de acordo com os 5 elementos da narrativa e se ela se encaixa no gênero história. Leve em consideração esses pontos: 📚 Coerência, 🧠 Criatividade, 📝 Qualidade gramatical e textual, 🎯 Moral ou mensagem e 🔗 Relação com a frase: {frase}. A avaliação deve ser feita em uma escala de 0 a 10, onde 0 é o pior e 10 é o melhor. Explique de forma bem breve o motivo da nota. Exemplo: 📚 Coerência: 8 - Pois é uma leitura fácil e não é confusa. (...) ATENÇÃO: TIRE OS '**' DA AVALIAÇÃO. no número 6, apenas diga a nota e o motivo sem repetir a frase. Depois, faça a média das notas (Ex: 🔢 Média final: 8), na hora de avaliar a relação com a frase, faça assim: '🔗 Relação com a frase: 8' e não apenas o emoji. APENAS DÊ AS NOTAS, A MÉDIA E OS MOTIVOS! (informalidade e gírias não descontam a nota). Se não houver história, apenas diga: 'Você não enviou a história.'",
        max_tokens=250,
        temperature=0
    )

    return render_template('result.html', frase=frase, historia=historia, resultado=resultado.choices[0].text.strip())

@main.route('/configuracoes')
def configuracoes():
    dificuldade = session.get('dificuldade')
    return render_template('settings.html', dificuldade=dificuldade)


@main.route('/salvarconfiguracoes')
def salvarconfiguracoes():
    dificuldadeSelecionada = request.args.get('dificuldade')
    tempoSelecionado = request.args.get('tempo')
    caracteresSelecionado = request.args.get('caracteres')
    
    session['dificuldade'] = dificuldadeSelecionada
    session['tempo'] = tempoSelecionado
    session['caracteres'] = caracteresSelecionado
    
    return redirect(url_for('main.index'))