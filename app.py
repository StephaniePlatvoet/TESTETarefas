# source venv/bin/activate

#flask import-csv
#flask import-csv-birthdays

# export DATABASE_URL=postgresql://tarefas:7odhP4yn7ZT8YWWd5KiR6bXoLgxdBe7v@dpg-co6337m3e1ms73bet640-a.frankfurt-postgres.render.com/tarefas_tbhr
# export FLASK_APP=app.py
# flask run

# conda deactivate #
# pip freeze > requirements.txt #

# git init                            
# git commit -m "4 commit"
# git branch -M main
# git remote add origint https://github.com/StephaniePlatvoet/tarefa1.git
# git push -u origint main
# git add . 
# python3 app.py


from adiar import adiar
from BDcriar import create_db
from criar import criar
from editar import editar
from eliminar import eliminar
from feita import feita
from filtro import exibirFiltroCustom
from importCSV import criar_tarefas
from refresh import refresh
from datetime import datetime

from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

app = Flask(__name__)
app.secret_key = 'chave'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)
app.config["DEBUG"] = True

Tarefa = create_db(app,db)

@app.route('/')
def go_home():
    return exibirFiltroCustom(Tarefa, db)

# refresh

@app.route('/refresh')
def call_refresh():
    return refresh(Tarefa,db)

@app.route('/refresh0')
def call_refresh0():
    return refresh(Tarefa,db,classe_filter=0)


@app.route('/refreshAniversarios')
def call_refreshAniversarios():
    return refresh(Tarefa,db,classe_filter='aniversarios')


# filtros date
@app.route('/exibir_filtro_steph_min', methods=['GET'])
def exibirFiltroStephmin():
    return exibirFiltroCustom(Tarefa, db, owner='steph', filtrar_data_mais_proxima=True)


@app.route('/exibir_filtro_steph', methods=['GET'])
def exibirFiltroSteph():
    return exibirFiltroCustom(Tarefa, db, owner='steph')

@app.route('/exibir_filtro', methods=['GET'])
def do_filter():
    return exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=True)


@app.route('/exibir_todas', methods=['GET'])
def exibir_todas():
    return exibirFiltroCustom(Tarefa, db)

# edit tarefa
@app.route('/tarefa-feita/<id>')
def tarefa_feita(id):
    return feita(Tarefa,db,id)

@app.route('/tarefa-adiar/<id>')
def tarefa_adiar(id):
    return adiar(Tarefa,db,id)


@app.route('/atualizar_tarefa/<int:id>', methods=['POST'])
def atualizar_tarefa(id):
    return editar(Tarefa,db,id)


@app.route('/editar_tarefa/<int:id>', methods=['GET'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return render_template('editar_tarefa.html', tarefa=tarefa)

# calendario
@app.route('/calendario', methods=['GET'])
def calendario():
    # Número total de tarefas a mostrar no calendário
    total_tarefas = 35
    hoje = datetime.utcnow().date()

    # Query das tarefas ordenadas por data_proxima
    tarefas_query = Tarefa.query.filter(or_(Tarefa.owner == 'steph', Tarefa.owner == 'ambos'),Tarefa.classe == 0).order_by(Tarefa.data_proxima.asc()).limit(total_tarefas).all()

    # Inicializar estrutura dos dias da semana
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    calendario_semanal = {dia: [] for dia in dias_da_semana}

    # Distribuir tarefas pelos dias da semana
    for i, tarefa in enumerate(tarefas_query):
        dia_index = i % 7  # Isso garante a distribuição uniforme
        dia_nome = dias_da_semana[dia_index]
        calendario_semanal[dia_nome].append(tarefa)

    # Passa o calendário_semanal para o template
    return render_template('calendario.html', calendario_semanal=calendario_semanal, datetime=datetime)

# eliminar tarefa

@app.route('/eliminar-tarefa/<id>')
def eliminar_tarefa(id):
    return eliminar(Tarefa,db,id)


# criar tarefas
    
@app.route('/criar-tarefa', methods=['POST'])
def criar_tarefa():
    return criar(Tarefa,db)

nome_pasta = 'projeto tarefas oficial - cópia 4'
caminho_pasta = '/Users/stephanietrabalho/Desktop/projetos codigo recentes/' + nome_pasta + '/database'


@app.cli.command("import-csv-birthdays") #flask import-csv-birthdays
def import_csv():
    name_csv_file = caminho_pasta + '/Livro6.csv'
    criar_tarefas(Tarefa, db,name_csv_file)

@app.cli.command("import-csv") #flask import-csv
def import_csv():
    name_csv_file = caminho_pasta + '/Livro4.csv'
    criar_tarefas(Tarefa, db,name_csv_file)

if __name__ == "__main__":
    app.run(debug=True)
