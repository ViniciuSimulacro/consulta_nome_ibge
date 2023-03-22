from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

nome = ''

@app.route('/', methods=['GET','POST'])
def index():
    global nome
    if request.method == 'POST':
        nome = request.form['nome']   
        return redirect(url_for('resposta',nome=nome))
    else:
        return render_template('index.html', nome=nome)

@app.route('/resposta')
def resposta():
    lista =[]
    request = requests.get(f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}')
    request = request.json()
    if request == []:
        return render_template('erro.html', nome=nome)
    else:
        periodos = (request[0]['res'])
        total = len(periodos)
        for n in range(0,total):
            data = (periodos[n]['periodo'])
            inicio = data[1:5]
            fim = data[6:10]
            quantidade = (periodos[n]['frequencia'])
            if inicio == '930[':
                resultado = f'No ano de 1930 nome {nome} teve {quantidade} registros!'
                lista.append(resultado)
            else:
                resultado = f'Na década de {inicio} até {fim} o nome {nome} teve {quantidade} registros!'
                lista.append(resultado)
    return render_template('resultado.html', nome=nome, lista=lista)


if __name__ == '__main__':
    app.run(debug=True)
