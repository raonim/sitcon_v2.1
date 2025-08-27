from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import inspect
from models import db, AMV, Sinais, Usuario, MatriculasValidas, CDV
import csv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitcon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'univesp' 

TRADUCOES_GERAIS = {
    'idamv': 'AMV',
    'tipofuncao': 'Tipo da Função',
    'idcdv': 'CDV',
    'tipo': 'Tipo',
    'idSinais': 'SINAL',
    'tipoAspecto': 'Tipo do Aspecto',
    'L1': 'Locação 1',
    'L2': 'Locação 2',
    'L3': 'Locação 3',
    'L4': 'Locação 4',
    'L5': 'Locação 5',
    'L6': 'Locação 6',
    'L7': 'Locação 7',
    'L8': 'Locação 8',
    'L9': 'Locação 9',
    'L10': 'Locação 10',
    'tower': 'NX',
    'interface': 'Bastidor de Interface',
    'L14': 'Locação 14',
    'L15': 'Locação 15',
    'L16': 'Locação 16',
    'L17': 'Locação 17',
    'L18': 'Locação 18',
    'L19': 'Locação 19',
    'L20': 'Locação 20',
    'L21': 'Locação 21',
    'L22': 'Locação 22',
    'L23': 'Locação 23'
}

def formatar_valor_locacao(valor):
    """Transforma um valor como 'B-B-29' em 'Caixa B, TB B-29'."""
    if not isinstance(valor, str) or '-' not in valor:
        # Se não for um texto ou não tiver o formato esperado, retorna o valor original
        return valor
    
    partes = valor.split('-')
    
    if len(partes) >= 3:
        # Formato esperado: "B-B-29" ou mais partes
        caixa = f"Caixa {partes[0]}"
        tb = f"TB {partes[1]}-{partes[2]}"
        return f"{caixa}, {tb}"
    elif len(partes) == 2:
        # Formato como "B-B"
        caixa = f"Caixa {partes[0]}"
        tb = f"TB {partes[1]}"
        return f"{caixa}, {tb}"
    else:
        # Outros casos, retorna o valor original
        return valor

# sitcon_v2/app.py

def formatar_registros(registros, model_class):
    """
    Recebe uma lista de registros do SQLAlchemy e formata para exibição.
    Retorna uma lista de dicionários com nomes de campo traduzidos.
    """
    dados_formatados = []
    if not registros:
        return dados_formatados

    for registro in registros:
        campos_registro = {}
        for coluna in model_class.__table__.columns:
            nome_original = coluna.name
            nome_amigavel = TRADUCOES_GERAIS.get(nome_original, nome_original)
            
            valor = getattr(registro, nome_original)

            # --- LINHAS A SEREM ADICIONADAS ---
            # Se a coluna for de locação (L1, L2, etc.), formata o valor
            if nome_original.startswith('L') and nome_original[1:].isdigit():
                valor = formatar_valor_locacao(valor)
            # --- FIM DAS LINHAS A SEREM ADICIONADAS ---

            if valor not in [None, '']:
                campos_registro[nome_amigavel] = valor
        dados_formatados.append(campos_registro)
    return dados_formatados

def processar_importacao_csv(model_class, pk_fields):
    """
    Processa o upload de um arquivo CSV e o importa para um modelo de DB.
    :param model_class: A classe do modelo SQLAlchemy (ex: AMV, CDV).
    :param pk_fields: Uma lista de strings com os nomes dos campos da chave primária.
    """
    if 'arquivo' not in request.files:
        return "Nenhum arquivo enviado", 400

    arquivo = request.files['arquivo']
    if not arquivo.filename.endswith('.csv'):
        return "Formato inválido. Envie um arquivo .csv", 400

    try:
        stream = arquivo.stream.read().decode("utf-8-sig")
        lines = stream.splitlines()

        leitor = csv.DictReader(lines, delimiter=',', quotechar='"', skipinitialspace=True)

        criados = 0
        atualizados = 0

        colunas_modelo = [c.name for c in model_class.__table__.columns]

        for linha in leitor:
            linha_limpa = {k.strip('"'): v for k, v in linha.items()}

            # Constrói o filtro da chave primária dinamicamente
            filtro_pk = {field: linha_limpa[field] for field in pk_fields}
            existente = model_class.query.filter_by(**filtro_pk).first()

            if existente:
                # Atualiza o registro existente
                for coluna in colunas_modelo:
                    if coluna in linha_limpa:
                        setattr(existente, coluna, linha_limpa.get(coluna))
                atualizados += 1
            else:
                # Cria um novo registro
                # Filtra a linha para conter apenas colunas que o modelo espera
                dados_novo = {k: v for k, v in linha_limpa.items() if k in colunas_modelo}
                novo_registro = model_class(**dados_novo)
                db.session.add(novo_registro)
                criados += 1

        db.session.commit()
        return f"""
            <h3>Importação concluída!</h3>
            <p>✅ {criados} novos registros criados</p>
            <p>🔄 {atualizados} registros atualizados</p>
            <a href="{request.path}">Voltar</a>
        """

    except KeyError as e:
        db.session.rollback()
        return f"Erro: Coluna essencial faltando no CSV - {str(e)}", 400
    except Exception as e:
        db.session.rollback()
        return f"Erro na importação: {str(e)}", 500

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logado'):
            flash('Acesso não autorizado. Por favor, faça login.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

@app.route('/importar_csv', methods=['GET', 'POST'])
def importar_csv():
    if request.method == 'POST':
        return processar_importacao_csv(AMV, ['idamv', 'tipofuncao'])
    
    return '''
    <h2>Importar CSV para AMV</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="arquivo" accept=".csv" required>
      <button type="submit">Importar</button>
    </form>
    '''

@app.route('/importar_csv_cdv', methods=['GET', 'POST'])
def importar_csv_cdv():
    if request.method == 'POST':
        return processar_importacao_csv(CDV, ['idcdv', 'tipo'])

    return '''
    <h2>Importar CSV para CDV</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="arquivo" accept=".csv" required>
      <button type="submit">Importar</button>
    </form>
    '''

@app.route('/importar_sinais_csv', methods=['GET', 'POST'])
def importar_sinais_csv():
    if request.method == 'POST':
        return processar_importacao_csv(Sinais, ['idSinais', 'tipoAspecto'])
    
    return '''
    <h2>Importar CSV para Sinais</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="arquivo" accept=".csv" required>
      <button type="submit">Importar</button>
    </form>
    '''

@app.route('/verificar_sinais')
def verificar_sinais():
    registros = Sinais.query.order_by(Sinais.idSinais, Sinais.tipoAspecto).limit(50).all()
    return render_template('verificar_sinais.html', registros=registros)



USUARIO = 'teste'
SENHA = 'teste'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    
    if request.method == 'POST':
        login = request.form['usuario']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(login=login).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            session['logado'] = True
            session['usuario_id'] = usuario.id 
            return redirect(url_for('sitcon'))
        else:
            erro = 'Credenciais inválidas ou usuário não cadastrado!'
    
    return render_template('login.html', erro=erro)

@app.route('/static/<path:filename>')
def static_files(images):
    return send_from_directory('static', images)

@app.route('/sitcon')
@login_required
def sitcon():
    return render_template('sitcon.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        login = request.form.get('login')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        

        if not MatriculasValidas.query.filter_by(matricula=matricula).first():
            flash('Matrícula não encontrada no sistema. Cadastro não permitido.', 'error')
            return redirect(url_for('cadastro'))
        

        if Usuario.query.filter_by(matricula=matricula).first():
            flash('Esta matrícula já possui cadastro ativo.', 'error')
            return redirect(url_for('cadastro'))
        

        if Usuario.query.filter_by(login=login).first():
            flash('Nome de usuário já em uso. Escolha outro.', 'error')
            return redirect(url_for('cadastro'))
        

        novo_usuario = Usuario(
            matricula=matricula,
            login=login,
            nome=nome,
            senha=generate_password_hash(senha)
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html', titulo="Cadastro de Usuário")

@app.route('/amv')
@login_required
def amv():
    amv_numbers = [3, 7, 9, 11, 25, 27, 29, 31, 39, 43, 47]
    return render_template('amv.html', 
                        amvs=amv_numbers,
                        titulo='Aparelhos de Mudança de Via')

@app.route('/amv_comando/<amv_id>')
def amv_comando(amv_id):
    return mostrar_amv(amv_id, tipo='Comando')

@app.route('/amv_indicacao/<amv_id>')
def amv_indicacao(amv_id):
    return mostrar_amv(amv_id, tipo='Indicação')


@login_required
def mostrar_amv(amv_id, tipo):
    try:
        amv_number = int(amv_id)
    except ValueError:
        flash('ID do AMV deve ser um número', 'error')
        return redirect(url_for('amv'))
    
    try:
        if tipo == 'Comando':
            registros = AMV.query.filter_by(idamv=amv_number)\
                               .filter(AMV.tipofuncao.in_(['NWR', 'WR']))\
                               .order_by(AMV.tipofuncao)\
                               .all()
        else: 
            registros = AMV.query.filter_by(idamv=amv_number)\
                               .filter(AMV.tipofuncao.in_(['NWP', 'WP']))\
                               .order_by(AMV.tipofuncao)\
                               .all()
        
        # O bloco de formatação foi substituído por esta linha
        dados = formatar_registros(registros, AMV)
            
    except Exception as e:
        flash(f'Erro ao acessar banco de dados: {str(e)}', 'error')
        return redirect(url_for('amv'))
    
    if not dados:
        flash(f'Nenhum registro de {tipo} encontrado para AMV {amv_number}', 'warning')
        return redirect(url_for('amv'))
    
    return render_template('amv_detail.html',
                         amv_id=amv_number,
                         registros=dados,
                         tipo=tipo)

@app.route('/amv/<amv_id>')
@login_required
def amv_detail(amv_id):
    try:
        amv_number = int(amv_id)
    except ValueError:
        flash('ID do AMV inválido', 'error')
        return redirect(url_for('amv'))
    

    registros = AMV.query.filter_by(idamv=amv_number).order_by(AMV.tipofuncao).all()
    
    if not registros:
        flash(f'AMV {amv_number} não encontrado', 'warning')
        return redirect(url_for('amv'))
    

    dados = []
    for registro in registros:
        campos_registro = {}
        for coluna in AMV.__table__.columns:
            nome = coluna.name
            valor = getattr(registro, nome)
            if valor not in [None, '']:
                campos_registro[nome] = valor
        dados.append(campos_registro)
    
    return render_template('amv_detail.html',
                        amv_id=amv_number,
                        registros=dados)

@app.route('/cdv')
@login_required
def cdv():
    cdvs = ['1N08', '1N09', '1N10', '1N11', '1S06', '1S07', '1S09', 
            '1S11', '1S12', '1S13', '1S14', '2N06', '2N07', '2N08', 
            '2N09', '2N10', '2S08', '2S09', '2S10', '2S11', '2S12', 
            '2S13', '2S14', '2S15']
    return render_template('cdv.html', cdvs=cdvs, titulo='Circuitos de Via')

@app.route('/cdv/<cdv_id>')
@login_required
def cdv_detail(cdv_id):
    registros = CDV.query.filter_by(idcdv=cdv_id).all()
    
    if not registros:
        flash(f'CDV {cdv_id} não encontrado', 'warning')
        return redirect(url_for('cdv'))

    # O bloco de formatação foi substituído por esta linha
    dados = formatar_registros(registros, CDV)

    return render_template('cdv_detail.html',
                         cdv_id=cdv_id,
                         registros=dados)

@app.route('/sinais')
@login_required
def sinais():
    sinais = [4, 6, 12, 16, 20, 22, 28, 30, 52, 54, 56, 62, 64, 66, 68, 70, 72, 78, 80]
    return render_template('sinais.html', sinais=sinais, titulo='Sinais')

@app.route('/sinais/<sinal_id>')
@login_required
def sinal_detail(sinal_id):
    try:
        sinal_number = int(sinal_id)
    except ValueError:
        flash('ID do SINAL inválido', 'error')
        return redirect(url_for('sinais'))
    
    registros = Sinais.query.filter_by(idSinais=sinal_number).all()
    
    if not registros:
        flash(f'SINAL {sinal_number} não encontrado', 'warning')
        return redirect(url_for('sinais'))

    # O bloco de formatação foi substituído por esta linha
    dados = formatar_registros(registros, Sinais)

    if not dados:
        flash(f'Sinal {sinal_number} não encontrado', 'warning')
        return redirect(url_for('sinais'))
    
    return render_template('sinal_detail.html',
                        sinal_id=sinal_number,
                        registros=dados)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)