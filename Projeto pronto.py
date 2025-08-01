import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def query_database(filter_column, filter_value):
    conn = sqlite3.connect('projeto1.db')
    cursor = conn.cursor()
    if filter_value:
        query = f'SELECT * from EquipamentosTI WHERE {filter_column} = ?'
        cursor.execute(query, (filter_value,))
    else:
        query = f'SELECT * from EquipamentosTI'
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_distinct_values(column_name):
    conn = sqlite3.connect('projeto1.db')
    cursor = conn.cursor()
    query = f'SELECT DISTINCT {column_name} FROM EquipamentosTI'
    cursor.execute(query)
    values = [row[0] for row in cursor.fetchall()]
    conn.close()
    return values


def update_filter_values(*args):
    selected_column = filter_column_var.get()
    filter_entry['values'] = get_distinct_values(selected_column)


def login():
    global login_attempts
    # Verifica as credenciais do administrador
    username = admin_user_entry.get()
    password = admin_password_entry.get()

    if username == "admin" and password == "admin":
        # Habilita os elementos de filtro e o botão de consulta
        filter_column_dropdown.config(state='readonly')
        filter_entry.config(state='readonly')
        query_button.config(state='enabled')
        add_button.config(state='enabled')  # Habilita o botão de adicionar
        update_button.config(state='enabled')  # Habilita o botão de atualizar
        delete_button.config(state='enabled')  # Habilita o botão de deletar
        login_button.config(state='disabled')  # Desabilita o botão de login após o login bem-sucedido
        admin_user_entry.config(state='disabled')  # Desabilita a entrada de usuário após o login bem-sucedido
        admin_password_entry.config(state='disabled')  # Desabilita a entrada de senha após o login bem-sucedido
        # Exibir uma mensagem de confirmação
        tk.messagebox.showinfo("Login bem-sucedido", "Login como administrador bem-sucedido!")
    else:
        # Incrementa o contador de tentativas de login
        login_attempts += 1
        if login_attempts >= 3:
            # Exibir uma mensagem de erro e fechar a janela após três tentativas incorretas
            tk.messagebox.showerror("Erro de login", "Número máximo de tentativas excedido. Fechando o programa.")
            root.destroy()
        else:
            # Exibir uma mensagem de erro
            tk.messagebox.showerror("Erro de login", "Credenciais inválidas. Tente novamente.")


def open_add_equipment_window():
    # Esta função será chamada quando o botão "Adicionar Equipamento" for pressionado
    # Cria uma nova janela para inserir os dados do novo equipamento
    add_window = tk.Toplevel(root)
    add_window.title("Adicionar Equipamento")
    add_window.geometry("300x200")

    # Labels e entry fields para inserir os dados do equipamento
    processador_label = ttk.Label(add_window, text="Processador:")
    processador_label.grid(row=0, column=0, padx=5, pady=5)
    processador_entry = ttk.Entry(add_window)
    processador_entry.grid(row=0, column=1, padx=5, pady=5)

    ram_label = ttk.Label(add_window, text="Memória RAM:")
    ram_label.grid(row=1, column=0, padx=5, pady=5)
    ram_entry = ttk.Entry(add_window)
    ram_entry.grid(row=1, column=1, padx=5, pady=5)

    armazenamento_label = ttk.Label(add_window, text="Armazenamento:")
    armazenamento_label.grid(row=2, column=0, padx=5, pady=5)
    armazenamento_entry = ttk.Entry(add_window)
    armazenamento_entry.grid(row=2, column=1, padx=5, pady=5)

    usuario_label = ttk.Label(add_window, text="Usuário:")
    usuario_label.grid(row=3, column=0, padx=5, pady=5)
    usuario_entry = ttk.Entry(add_window)
    usuario_entry.grid(row=3, column=1, padx=5, pady=5)

    so_label = ttk.Label(add_window, text="Sistema Operacional:")
    so_label.grid(row=4, column=0, padx=5, pady=5)
    so_entry = ttk.Entry(add_window)
    so_entry.grid(row=4, column=1, padx=5, pady=5)

    # Botão para adicionar o equipamento ao banco de dados
    add_button = ttk.Button(add_window, text="Adicionar",
                            command=lambda: add_equipment(processador_entry.get(), ram_entry.get(),
                                                          armazenamento_entry.get(), usuario_entry.get(),
                                                          so_entry.get()))
    add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


def add_equipment(processador, ram, armazenamento, usuario, so):
    # Esta função será chamada quando o botão "Adicionar" na janela de adicionar equipamento for pressionado
    # Adiciona os dados do novo equipamento ao banco de dados
    conn = sqlite3.connect('projeto1.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO EquipamentosTI (Processador, MemoriaRAM, MemoriaArmazenamento, Usuario, SistemaOperacional) VALUES (?, ?, ?, ?, ?)",
        (processador, ram, armazenamento, usuario, so))
    conn.commit()
    conn.close()
    # Exibir uma mensagem de confirmação
    tk.messagebox.showinfo("Sucesso", "Equipamento adicionado com sucesso!")


def update_equipment():
    # Esta função será chamada quando o botão "Atualizar Equipamento" for pressionado
    # Cria uma nova janela para selecionar o equipamento a ser atualizado
    update_window = tk.Toplevel(root)
    update_window.title("Atualizar Equipamento")
    update_window.geometry("300x200")

    # Labels e combobox para selecionar o ID do equipamento a ser atualizado
    id_label = ttk.Label(update_window, text="Selecione o ID do Equipamento:")
    id_label.grid(row=0, column=0, padx=5, pady=5)

    selected_id_var = tk.StringVar()
    id_dropdown = ttk.Combobox(update_window, textvariable=selected_id_var)
    id_dropdown['values'] = get_distinct_values('ID')
    id_dropdown.grid(row=0, column=1, padx=5, pady=5)

    # Botão para abrir a janela de alterar dados do equipamento selecionado
    update_button = ttk.Button(update_window, text="Alterar Dados",
                               command=lambda: open_update_equipment_window(selected_id_var.get()))
    update_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def open_update_equipment_window(equipment_id):
    # Esta função será chamada quando o botão "Alterar Dados" na janela de atualizar equipamento for pressionado
    # Cria uma nova janela para alterar os dados do equipamento selecionado
    update_window = tk.Toplevel(root)
    update_window.title("Alterar Dados do Equipamento")
    update_window.geometry("300x200")

    # Labels e entry fields para alterar os dados do equipamento
    processador_label = ttk.Label(update_window, text="Novo Processador:")
    processador_label.grid(row=0, column=0, padx=5, pady=5)
    processador_entry = ttk.Entry(update_window)
    processador_entry.grid(row=0, column=1, padx=5, pady=5)

    ram_label = ttk.Label(update_window, text="Nova Memória RAM:")
    ram_label.grid(row=1, column=0, padx=5, pady=5)
    ram_entry = ttk.Entry(update_window)
    ram_entry.grid(row=1, column=1, padx=5, pady=5)

    armazenamento_label = ttk.Label(update_window, text="Novo Armazenamento:")
    armazenamento_label.grid(row=2, column=0, padx=5, pady=5)
    armazenamento_entry = ttk.Entry(update_window)
    armazenamento_entry.grid(row=2, column=1, padx=5, pady=5)

    usuario_label = ttk.Label(update_window, text="Novo Usuário:")
    usuario_label.grid(row=3, column=0, padx=5, pady=5)
    usuario_entry = ttk.Entry(update_window)
    usuario_entry.grid(row=3, column=1, padx=5, pady=5)

    so_label = ttk.Label(update_window, text="Novo Sistema Operacional:")
    so_label.grid(row=4, column=0, padx=5, pady=5)
    so_entry = ttk.Entry(update_window)
    so_entry.grid(row=4, column=1, padx=5, pady=5)

    # Botão para atualizar os dados do equipamento
    update_button = ttk.Button(update_window, text="Atualizar",
                               command=lambda: update_selected_equipment(equipment_id, processador_entry.get(),
                                                                         ram_entry.get(), armazenamento_entry.get(),
                                                                         usuario_entry.get(), so_entry.get()))
    update_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


def update_selected_equipment(equipment_id, processador, ram, armazenamento, usuario, so):
    # Esta função será chamada quando o botão "Atualizar" na janela de alterar dados do equipamento for pressionado
    # Atualiza os dados do equipamento selecionado no banco de dados
    conn = sqlite3.connect('projeto1.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE EquipamentosTI SET Processador=?, MemoriaRAM=?, MemoriaArmazenamento=?, Usuario=?, SistemaOperacional=? WHERE ID=?",
        (processador, ram, armazenamento, usuario, so, equipment_id))
    conn.commit()
    conn.close()
    # Exibir uma mensagem de confirmação
    tk.messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso!")


def delete_equipment():
    # Esta função será chamada quando o botão "Deletar Equipamento" for pressionado
    # Cria uma nova janela para selecionar o equipamento a ser deletado
    delete_window = tk.Toplevel(root)
    delete_window.title("Deletar Equipamento")
    delete_window.geometry("300x200")

    # Dropdown menu para selecionar o equipamento a ser deletado
    selected_equipment_var = tk.StringVar()
    equipment_dropdown = ttk.Combobox(delete_window, textvariable=selected_equipment_var)
    equipment_dropdown['values'] = get_distinct_values('ID')
    equipment_dropdown.grid(row=0, column=0, padx=5, pady=5)

    # Botão para deletar o equipamento selecionado
    delete_button = ttk.Button(delete_window, text="Deletar",
                               command=lambda: confirm_delete(selected_equipment_var.get()))
    delete_button.grid(row=1, column=0, padx=5, pady=5)


def confirm_delete(equipment_id):
    # Esta função será chamada quando o botão "Deletar" na janela de deletar equipamento for pressionado
    # Exibe uma mensagem de confirmação antes de deletar o equipamento
    confirm = tk.messagebox.askyesno("Confirmar", "Tem certeza que deseja remover a linha de dados?")
    if confirm:
        # Deleta o equipamento selecionado do banco de dados
        conn = sqlite3.connect('projeto1.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EquipamentosTI WHERE ID=?", (equipment_id,))
        conn.commit()
        conn.close()
        # Exibir uma mensagem de confirmação
        tk.messagebox.showinfo("Sucesso", "Equipamento removido com sucesso!")


# Create the main application window
root = tk.Tk()
root.title("Consulta de Equipamentos TI")

# Configurações da janela do GUI
filter_frame = ttk.Frame(root)
filter_frame.pack(padx=500, pady=5, fill=tk.BOTH, expand=False)

# Create a label para o usúario administrador
admin_label = ttk.Label(filter_frame, text="Credenciais do Administrador:")
admin_label.grid(row=0, column=0, padx=5, pady=5)

# Create an entry field para o nome do usuário administrador
admin_user_entry = ttk.Entry(filter_frame)
admin_user_entry.grid(row=0, column=1, padx=5, pady=5)

# Create an entry field para a senha do usuário administrador
admin_password_entry = ttk.Entry(filter_frame, show="*")  # Show '*' characters para esconder a senha
admin_password_entry.grid(row=0, column=2, padx=5, pady=5)

# Create a login button
login_button = ttk.Button(filter_frame, text="Login", command=login)
login_button.grid(row=0, column=3, padx=5, pady=5)

# Create a label for the filter criteria
filter_label = ttk.Label(filter_frame, text="Filtrar por:")
filter_label.grid(row=1, column=0, padx=5, pady=5)

# Create a dropdown menu for selecting filter criteria
filter_column_var = tk.StringVar()
filter_column_dropdown = ttk.Combobox(filter_frame, textvariable=filter_column_var, state='disabled')
filter_column_dropdown['values'] = ('ID', 'Processador', 'MemoriaRAM', 'MemoriaArmazenamento', 'Usuario',
                                    'SistemaOperacional',)  # Add more column names as needed
filter_column_dropdown.grid(row=1, column=1, padx=5, pady=5)
filter_column_dropdown.current(0)
filter_column_var.trace('w', update_filter_values)

# Create an entry field for providing filter values
filter_entry = ttk.Combobox(filter_frame, state='disabled')
filter_entry.grid(row=1, column=2, padx=5, pady=5)

# Create a button to execute the query
query_button = ttk.Button(filter_frame, text="Consultar Equipamentos", state='disabled',
                          command=lambda: show_results(filter_column_var.get(), filter_entry.get()))
query_button.grid(row=1, column=3, padx=5, pady=5)

# Create a button to add equipment
add_button = ttk.Button(filter_frame, text="Adicionar Equipamento", state='disabled', command=open_add_equipment_window)
add_button.grid(row=2, column=0, padx=5, pady=5)

# Create a button to update equipment
update_button = ttk.Button(filter_frame, text="Atualizar Equipamento", state='disabled', command=update_equipment)
update_button.grid(row=2, column=1, padx=5, pady=5)

# Create a button to delete equipment
delete_button = ttk.Button(filter_frame, text="Deletar Equipamento", state='disabled', command=delete_equipment)
delete_button.grid(row=2, column=2, padx=5, pady=5)

# Create a frame for the results
results_frame = ttk.Frame(root)
results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a text widget to display the results
results_text = tk.Text(results_frame, wrap=tk.WORD)
results_text.pack(fill=tk.BOTH, expand=True)


def show_results(filter_column, filter_value):
    data = query_database(filter_column, filter_value)
    results_text.delete(1.0, tk.END)  # Clear previous results
    for row in data:
        results_text.insert(tk.END, row)
        results_text.insert(tk.END, '\n')


# Run the Tkinter event loop
root.mainloop()
