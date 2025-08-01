import sqlite3

# Conectando ao banco de dados existente
conn = sqlite3.connect('projeto1.db')
cursor = conn.cursor()

# Exemplo de operações: selecionar dados da tabela
cursor.execute('SELECT * from EquipamentosTI where SistemaOperacional = "Windows 10"')
dados = cursor.fetchall()
for row in dados:
    print(row)

# Exemplo de operações: fechar a conexão com o banco de dados
conn.close()
