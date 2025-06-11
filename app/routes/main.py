from flask import Blueprint, render_template, redirect, session, url_for, request
from openai import OpenAI
from app import db
from app.models import Historias
import re
# from app.openrouter_client import client

main = Blueprint('main', __name__)

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key="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",
)

@main.route('/teste')
def teste():
    return "Rota de teste"

@main.route('/')
def index():
    session.pop('frase', None)
    
    if 'dificuldade' not in session or session['dificuldade'] is None:
        session['dificuldade'] = 'Médio'

    dificuldade = session.get('dificuldade')

    return render_template('index.html', dificuldade=dificuldade)

@main.route('/gerar_frase')
def gerar_frase():
    try:
        resposta = client.completions.create(
            model="openai/gpt-4.1",
            prompt="Crie uma frase bem curta e aleatória que esteja dentro do contexto de uma história/conversa para que o usuário crie uma história em que essa frase se encaixe nela. A frase deve ter até 10 palavras e fazer sentido. Não adicione explicações, apenas a frase.",
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
        caracteres = 500
        tempo = 300
        
    elif dificuldade == 'Médio':
        caracteres = 300
        tempo = 180
        
    elif dificuldade == 'Difícil':
        caracteres = 200
        tempo = 120
    
    else:
        caracteres = session.get('caracteres')
        tempo = session.get('tempo')
        
        print(f"caracteres: {caracteres}")
        print(f"tempo: {tempo}")
        
    return render_template('history.html', frase=frase, dificuldade=session['dificuldade'], caracteres=caracteres, tempo=tempo)

@main.route('/resultado', methods=['POST'])
def resultado():
    frase = session.get('frase', None)
    historia = request.form.get('historia')

    resultado = client.completions.create(
        model="openai/gpt-4.1",
        prompt=f"De acordo com a história: {historia}, gostaria que você a avaliasse rigorosamente, como se fosse uma prova de faculdade, a história deve ter começo, meio e fim. Com introdução, desenvolvimento e conclusão. Avalie-a de acordo com os 5 elementos da narrativa e se ela se encaixa no gênero história. Leve em consideração esses pontos: 📚 Coerência, 🧠 Criatividade, 📝 Qualidade gramatical e textual, 🎯 Moral ou mensagem e 🔗 Relação com a frase: {frase}. A avaliação deve ser feita em uma escala de 0 a 10, onde 0 é o pior e 10 é o melhor. Explique de forma bem breve o motivo da nota. Exemplo: 📚 Coerência: 8 - Pois é uma leitura fácil e não é confusa. (...) ATENÇÃO: TIRE OS '**' DA AVALIAÇÃO. no número 6, apenas diga a nota e o motivo sem repetir a frase. Depois, faça a média das notas (Ex: 🔢 Média final: 8), na hora de avaliar a relação com a frase, faça assim: '🔗 Relação com a frase: 8' e não apenas o emoji. APENAS DÊ AS NOTAS, A MÉDIA E OS MOTIVOS! (informalidade e gírias não descontam a nota). Se não houver história, apenas diga: 'Você não enviou nada... Tente denovo, por favor.'",
        max_tokens=300,
        temperature=0
    )
    
    media = client.completions.create(
        model="openai/gpt-4.1",
        prompt=f"Qual a média das notas: {resultado.choices[0].text.strip()}? Responda apenas com a média, sem explicações.",
        max_tokens=50,
        temperature=0
    )
    
    media_final = media.choices[0].text.strip()
    
    def extrair_nota(emoji, texto):
        padrao = rf"{re.escape(emoji)}.*?:\s*(\d+)"
        match = re.search(padrao, texto)
        return match.group(1) if match else "0"

    resultado_texto = resultado.choices[0].text.strip()

    coerencia = extrair_nota("📚", resultado_texto)
    diversao = extrair_nota("🧠", resultado_texto)
    gramatica = extrair_nota("📝", resultado_texto)
    moral = extrair_nota("🎯", resultado_texto)
    relacao = extrair_nota("🔗", resultado_texto)
    
    resultado_texto = resultado.choices[0].text.strip()
    
    nova_historia = Historias(
        historia=historia,
        dificuldade=session.get('dificuldade', 'Médio'),
        coerencia=coerencia,
        diversao=diversao,
        gramatica=gramatica,
        moral=moral,
        relacaofrase=relacao,
        media=media_final,
        frase=frase
    )
    db.session.add(nova_historia)
    db.session.commit()

    return render_template('result.html', frase=frase, historia=historia, resultado=resultado_texto, media=media_final, dificuldade=session.get('dificuldade', 'Médio'), nota_media=media.choices[0].text.strip())
    
@main.route('/configuracoes')
def configuracoes():
    dificuldade = session.get('dificuldade')
    tempo = session.get('tempo')
    caracteres = session.get('caracteres')
    
    return render_template('settings.html', dificuldade=dificuldade, tempo=tempo, caracteres=caracteres)

@main.route('/salvarconfiguracoes')
def salvarconfiguracoes():
    dificuldadeSelecionada = request.args.get('dificuldade')
    tempoSelecionado = request.args.get('tempo')
    caracteresSelecionado = request.args.get('caracteres')
    
    session['dificuldade'] = dificuldadeSelecionada
    session['tempo'] = tempoSelecionado
    session['caracteres'] = caracteresSelecionado
    
    return redirect(url_for('main.index'))

@main.route('/historias')
def historias_salvas():
    historias = Historias.query.all()
    return render_template('stories.html', historias=historias)

@main.route('/historia/<int:id>')
def historia(id):
    historia = Historias.query.get_or_404(id)
    return render_template('storia.html', historia=historia)

@main.route('/deletar_historia/<int:id>')
def deletar_historia(id):
    historia = Historias.query.get_or_404(id)
    db.session.delete(historia)
    db.session.commit()
    return redirect(url_for('main.historias_salvas'))