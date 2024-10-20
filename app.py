from groq import Groq
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

# Função para interagir com o modelo da GROQ
def consultar_IA_GROQ(prompt_text):
    client = Groq(api_key='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')
    
    # Criar a consulta ao modelo
    completion = client.chat.completions.create(
        model="llama3-8b-8192",  # Modelo que você está utilizando
        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    resposta = ""
    for chunk in completion:
        resposta += chunk.choices[0].delta.content or ""
    
    return resposta

# Função para criar o agente de suporte usando o prompt
def criar_agente_de_suporte(pergunta_cliente):
    # Definir o contexto do agente de suporte
    prompt_text = f"""
    Você é um agente de suporte de uma empresa fictícia chamada 'Empresa XPTO'. 
    Seu trabalho é ajudar os clientes com perguntas sobre produtos, políticas e suporte técnico.
    Pergunta do cliente: {pergunta_cliente}
    """
    
    # Enviar o prompt para a IA GROQ
    resposta = consultar_IA_GROQ(prompt_text)
    
    return resposta

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response_message = criar_agente_de_suporte(user_message)
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(debug=True)