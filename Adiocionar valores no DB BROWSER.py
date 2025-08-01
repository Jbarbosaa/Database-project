import sqlite3

# Conectando ao banco de dados existente
conn = sqlite3.connect('projeto1.db')
cursor = conn.cursor()

# Cadastro de equipamentos
vProcessador = input("Insira o processador: ")
vRAM = input("Insira o número de RAM: ")
vCap_armazenamento = input("Insira a capacidade armazenamento: ")
vUsers = input("Insira o nome do usuário da máquina: ")
VSO = input("Insira o sistema operacional da máquina: ")

# Inserindo valores na tabela
cursor.execute("INSERT INTO EquipamentosTI (Processador, MemoriaRAM, MemoriaArmazenamento, Usuario, SistemaOperacional) VALUES (?, ?, ?, ?, ?)",
               (vProcessador, vRAM, vCap_armazenamento, vUsers, VSO))

conn.commit()
conn.close()

print("Valor inserido com sucesso!")