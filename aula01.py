from tkinter import *
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatCliente(self):
        if not self.codigo_entry.get():  # Verifica se o código do cliente está vazio
            print("Selecione um Cliente")
            return
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, "Ficha do Cliente")

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, "Código: ")
        self.c.drawString(50, 675, "Nome: ")
        self.c.drawString(50, 650, "Telefone: ")
        self.c.drawString(50, 625, "Cidade: ")

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 675, self.nomeRel)
        self.c.drawString(150, 650, self.telefoneRel)
        self.c.drawString(150, 625, self.cidadeRel)

        self.c.rect(20,550, 550, 5, fill=True, stroke=False)




        self.c.showPage()
        self.c.save()
        self.printCliente()


root = Tk()

class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        try:
            self.conn = sqlite3.connect('clientes.db')
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados")
        except Exception as e:
            print("Não foi possível conectar-se ao banco, " + str(e))

    def desconecta_bd(self):
        try:
            self.conn.close()
            print(" Desconectado ao banco de dados")
        except Exception as e:
            print("Não foi possível desconectar-se ao banco, " + str(e))
    
    def montaTabelas(self):
        self.conecta_bd() 
        try:

            self.cursor.execute('''
                                CREATE TABLE  IF NOT EXISTS Clientes (cod INTEGER PRIMARY KEY,
                                                                        nome_cliente CHAR(40) NOT NULL,
                                                                        telefone CHAR(20),
                                                                        cidade CHAR(20))''')
            self.conn.commit(); print("Banco de dados criado")
        except Exception as e:
            print("Não foi possível criar uma nova tabela, " + str(e))
        finally:
            self.desconecta_bd()
    
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        try:
            self.cursor.execute('''INSERT INTO Clientes(nome_cliente, telefone, cidade) VALUES(?, ?, ?)''', (self.nome, self.telefone, self.cidade))
            self.conn.commit(); print('Dados adicionados com sucesso')
        except Exception as e:
            print("Não foi possível adicionar novo cliente, " + str(e))
        finally:
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()
    
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        try:
            lista = self.cursor.execute('''SELECT cod, nome_cliente, telefone, cidade FROM Clientes ORDER BY nome_cliente ASC; ''')
            for i in lista:
                self.listaCli.insert("", END, values=i)
        except Exception as e:
            print("Não foi possível listar clientes existentes, " + str(e))
        finally:
            self.desconecta_bd()

    def onDoubleClick(self, event):
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
        
    def deleta_cliente(self):
        self.variaveis()
        if not self.codigo_entry.get():  # Verifica se o código do cliente está vazio
            print("Selecione um Cliente")
            return
        self.conecta_bd()
        try:
            self.cursor.execute('''DELETE FROM Clientes WHERE cod = ? ''',(self.codigo))
            self.conn.commit()
        except Exception as e:
            print("Não foi possível deletar cliente selecionado, " + str(e))
        finally:
            self.desconecta_bd()
            self.limpa_tela()
            self.select_lista()
    
    def atualiza_cliente(self):
        self.variaveis()
        if not self.codigo_entry.get():  # Verifica se o código do cliente está vazio
            print("Selecione um Cliente")
            return
        self.conecta_bd()
        try:
            self.cursor.execute('''UPDATE Clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ?''', ( self.nome, self.telefone, self.cidade, self.codigo))
            self.conn.commit()
        except Exception as e:
            print("Não foi possível atualizar cliente selecionado, " + str(e))
        finally:
            self.desconecta_bd()
            self.limpa_tela()
            self.select_lista()
    
    def busca_cliente(self):
        self.conecta_bd()
        try:

            self.listaCli.delete(*self.listaCli.get_children())

            self.nome_entry.insert(END, "%")
            nome = self.nome_entry.get().strip()

            nome_completo = "%" + nome + "%"

            if nome_completo == "":
                print("Por favor, insira um nome para a busca.")
                return

            self.cursor.execute("""SELECT * FROM Clientes WHERE nome_cliente LIKE ? ORDER BY nome_cliente ASC""" ,(nome_completo,))
            buscanomeCli = self.cursor.fetchall()
            if not buscanomeCli:
                print("Resultados não obtidos")
            else:
                for i in buscanomeCli:
                    self.listaCli.insert("", END, values=i)
                    self.limpa_tela()

        except Exception as e:
            print("Não foi possível fazer a busca, " + str(e))
        finally:
            self.desconecta_bd()




class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='blue')
        self.root.geometry("720x500")
        self.root.resizable('True', 'True')
        self.root.maxsize(width= 900, height=700)
        self.root.minsize(width= 500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='black', highlightthickness=2)
        self.frame_1.place(relx=0.02 ,rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='black', highlightthickness=2)
        self.frame_2.place(relx=0.02 ,rely=0.5, relwidth=0.96, relheight=0.46)
    
    def widgets_frame1(self):
        self.btn_limpar = Button(self.frame_1, text='Limpar', bd=2, bg='#107db2', fg='white', font=('verdana',8,'bold'),command=self.limpa_tela)
        self.btn_limpar.place(relx= 0.2, rely= 0.1, relheight=0.15, relwidth=0.1)

        self.btn_buscar = Button(self.frame_1, text='Buscar', bd=2, bg='#107db2', fg='white', font=('verdana',8,'bold'), command= self.busca_cliente)
        self.btn_buscar.place(relx= 0.3, rely= 0.1, relheight=0.15, relwidth=0.1)

        self.btn_novo = Button(self.frame_1, text='Novo', bd=2, bg='#107db2', fg='white', font=('verdana',8,'bold'), command= self.add_cliente)
        self.btn_novo.place(relx= 0.6, rely= 0.1, relheight=0.15, relwidth=0.1)

        self.btn_alterar = Button(self.frame_1, text='Alterar', bd=2, bg='#107db2', fg='white', font=('verdana',8,'bold'), command=self.atualiza_cliente)
        self.btn_alterar.place(relx= 0.7, rely= 0.1, relheight=0.15, relwidth=0.1)

        self.btn_apagar = Button(self.frame_1, text='Apagar', bd=2, bg='#107db2', fg='white', font=('verdana',8,'bold'), command=self.deleta_cliente)
        self.btn_apagar.place(relx= 0.8, rely= 0.1, relheight=0.15, relwidth=0.1)

        ###Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1)

        self.lb_nome = Label(self.frame_1, text='Nome', bg='#dfe3ee' ,fg='#107db2')
        self.lb_nome.place(relx= 0.05, rely= 0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.5)

        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#dfe3ee', fg='#107db2')
        self.lb_telefone.place(relx= 0.05, rely= 0.6)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx= 0.5, rely= 0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2","col3","col4"))
        self.listaCli.heading('#0', text="")
        self.listaCli.heading('#1', text="Código")
        self.listaCli.heading('#2', text="Nome")
        self.listaCli.heading('#3', text="Telefone")
        self.listaCli.heading('#4', text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        
        self.listaCli.place(relx= 0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.onDoubleClick)
    
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu =  filemenu)
        menubar.add_cascade(label= "Relatórios", menu = filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente", command=self.gerarRelatCliente)



    


Application()
