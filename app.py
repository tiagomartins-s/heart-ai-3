from flask import Flask, request, jsonify, render_template
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

app = Flask(__name__)

# ============================================================
# CREDENCIAIS
# ============================================================
API_KEY      = os.environ.get('WATSON_API_KEY',      'SBGOIHVNAk_kFl2gdYuokH_6o0Xggj9_ZNTnbDwsZ6EK')
URL          = os.environ.get('WATSON_URL',           'https://api.au-syd.assistant.watson.cloud.ibm.com')
WORKSPACE_ID = os.environ.get('WATSON_WORKSPACE_ID', '9075bbd2-f07f-4876-95f4-6ad014d595a9')

# ============================================================
# Autenticação — AssistantV1 (compatível com plano Lite)
# ============================================================
authenticator = IAMAuthenticator(API_KEY)
watson = AssistantV1(version='2021-06-14', authenticator=authenticator)
watson.set_service_url(URL)


# ============================================================
# Rotas Flask
# ============================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/mensagem', methods=['POST'])
def trocar_mensagem():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({'erro': 'Body da requisição está vazio ou não é JSON'}), 400

        texto_usuario = dados.get('mensagem', '').strip()
        context       = dados.get('context', {})  # mantém o estado da conversa

        # Envia a mensagem para o Watson
        resposta = watson.message(
            workspace_id=WORKSPACE_ID,
            input={'text': texto_usuario},
            context=context
        ).get_result()

        # Extrai o texto da resposta
        textos       = resposta.get('output', {}).get('text', [])
        resposta_bot = " ".join(textos) if textos else "Sem resposta do assistente."

        # Retorna o context para manter o estado na próxima mensagem
        return jsonify({
            'resposta': resposta_bot,
            'context':  resposta.get('context', {})
        }), 200

    except Exception as e:
        import traceback
        print("====== ERRO DO WATSON ======")
        traceback.print_exc()
        print("============================")
        return jsonify({'erro': str(e)}), 500


# ============================================================
# Entry point
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)