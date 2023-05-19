#Librerias / modulos
import mysql.connector
import tkinter.ttk as ttk

from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import train_test_split 

#Interfaz
ws = Tk()
ws.geometry('800x650+351+24')
ws.title("Programa de analisis de genero")

#Conexion con la Base de Datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
db_cursor = conexion.cursor(buffered=True)

#Funciones
def analisis(): #Arbol de decision
    global estado
    l = longitud_tf.get()
    a = altura_tf.get()
    X = []
    Y = []

    if conexion.is_connected == False:
        conexion.connect()

    db_cursor.execute("use empleadoPredictivo")
    sql = "select * from data_genero"
    db_cursor.execute(sql)
    rows = db_cursor.fetchall()
    for row in rows:
        alt = row[1]
        long = row[2]
        gen = row[3]

        X.append([alt, long])
        Y.append([gen])

    X_train, X_test, Y_train, Y_test = train_test_split (X, Y, test_size=0.75, random_state=42)
    clf = tree.DecisionTreeClassifier() 
    clf = clf.fit(X, Y)
    
    #prediccion
    prediction = clf.predict([[a,l]]) 
    print(prediction)
    estado = prediction

    #Precision
    clf = clf.fit(X_train,Y_train)
    y_pred = clf.predict(X_test)
    print("Precisión:", metrics.accuracy_score(Y_test, y_pred))

    #Insercion de prediccion a la base de datos
    if prediction == 'femenino':
        estado = 'femenino'
    elif prediction == 'masculino':
        estado = 'masculino'
    
    msg_Box = messagebox.askquestion("Analisis", estado)
    if msg_Box == 'yes':
        try:
            query = "insert into data_genero(altura, long_cabello, genero) values(%s, %s, %s)"
            records = [int(a), int(l), str(estado)]
            db_cursor.execute(query, records)
            conexion.commit()
            print("Dato evaluado\n")
        except mysql.connector.Error as err:
            print("Mensaje de error:", err)
            conexion.rollback()
    elif msg_Box == 'no':
        if prediction == 'femenino':
            estado = 'masculino'
        elif prediction == 'masculino':
            estado = 'femenino'

        msg2_box = messagebox.askquestion("Analisis", estado)
        if msg2_box == 'yes':
            try:
                query = "insert into data_genero(altura, long_cabello, genero) values(%s, %s, %s)"
                records = [int(a), int(l), str(estado)]
                db_cursor.execute(query, records)
                conexion.commit()
                print("Dato evaluado\n")
            except mysql.connector.Error as err:
                print("Mensaje de error:", err)
                conexion.rollback()

    genero_lbl = Label(ws, text=estado).place(x=350, y=320, anchor="center")
    return genero_lbl

def registro():
    print("Registrar Datos")

    nombre = nombre_tf.get()
    apellido = apellido_tf.get()
    fecha = fecha_cal.get_date()
    direccion = direccion_tf.get()
    edad = edad_tf.get()
    cabello = longitud_tf.get()
    altura = altura_tf.get()
    genero = estado
    
    try:
        query = "insert into datos(nombre, apellido, fecha_nacimiento, direccion, edad, longitud_cabello, altura, genero) values(%s, %s, %s, %s, %s, %s, %s, %s)"
        records = [str(nombre), str(apellido), fecha, str(direccion), int(edad), int(cabello), int(altura), str(genero)]
        db_cursor.execute(query, records)
        conexion.commit()
    except mysql.connector.Error as err:
        print("Mensaje:", err)

def actualizar():
    print("Actualizar DataGrid")
    if conexion.is_connected() == False:
            conexion.connect()
        
    tvStudent.delete(*tvStudent.get_children())  # Limpiar el treeview tvStudent

    db_cursor.execute("use empleadoPredictivo")  # Interactuar con la base de datos
    sql = "SELECT * FROM datos"
    db_cursor.execute(sql)
    total = db_cursor.rowcount
            
    print("Entradas de datos totales:" + str(total))
    rows = db_cursor.fetchall()
    Numero = ""
    Nombre= ""
    Apellido = ""
    Fecha_nacimiento = ""
    Direccion = ""
    Edad = ""
    Long_cabello = ""
    Altura = ""
    Genero = ""
    for row in rows:
        Numero = row[0]
        Nombre= row[1]
        Apellido = row[2]
        Fecha_nacimiento = row[3]
        Direccion = row[4]
        Edad = row[5]
        Long_cabello = row[6]
        Altura = row[7]
        Genero = row[8]
        tvStudent.insert("", 'end', text=Numero, values=(Numero, Nombre, Apellido, Fecha_nacimiento, Direccion, Edad, Long_cabello, Altura, Genero))

def borrar():
    print("Borrar Registro")
    nombre_tf.delete(0, 'end')

def limpiar():
    print("Limpiar Datos")

def val_letras(valid):
    for letter in valid:
        if not letter.isalpha() and letter not in "'-":
            return False
    return True

#Widgets Labels, Entry
Label(ws, text="Nombre:").place(x=200, y=40, anchor="e")
nombre_tf = StringVar()
Entry(ws, textvariable=nombre_tf).place(x=350, y=40, anchor="center")

Label(ws, text="Apellidos:").place(x=200, y=80, anchor="e")
apellido_tf = StringVar()
Entry(ws, textvariable=apellido_tf).place(x=350, y=80, anchor="center")

Label(ws, text="Fecha de nacimiento:").place(x=200, y=120, anchor="e")
fecha_cal = DateEntry(ws, width=12, background='darkblue',foreground='white', borderwidth=2, year=1970, locale='en_US', date_pattern='y-mm-dd')
fecha_cal.place(x=350, y=120, anchor="center")

Label(ws, text="Direccion:").place(x=200, y=160, anchor="e")
direccion_tf = StringVar()
Entry(ws, textvariable=direccion_tf).place(x=350, y=160, anchor="center")

Label(ws, text="Edad:").place(x=200, y=200, anchor="e")
edad_tf = StringVar()
Entry(ws, textvariable=edad_tf).place(x=350, y=200, anchor="center")

Label(ws, text="Longitud de cabello:").place(x=200, y=240, anchor="e")
longitud_tf = StringVar()
Entry(ws, textvariable=longitud_tf).place(x=350, y=240, anchor="center")

Label(ws, text="Altura:").place(x=200, y=280, anchor="e")
altura_tf = StringVar()
Entry(ws, textvariable=altura_tf).place(x=350, y=280, anchor="center")

Label(ws, text="Genero:").place(x=200, y=320, anchor="e")

button_Fr = LabelFrame(ws, text="Acciones")
button_Fr.place(x=650, y=110, anchor="center")

#Botones
Button(button_Fr, text="Analizar", width=15, command=analisis).pack()
Button(button_Fr, text="Registrar", width=15, command=registro).pack()
Button(button_Fr, text="Actualizar", width=15, command=actualizar).pack()
Button(button_Fr, text="Borrar", width=15, command=borrar).pack()
Button(button_Fr, text="Limpiar", width=15, command=limpiar).pack()

#Data Grid View
columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7","#8","#9")
tvStudent = ttk.Treeview(ws, show="headings",height="5", columns=columns)
tvStudent.heading('#1', text='Codigo', anchor='center')
tvStudent.column('#1', width=60, anchor='center', stretch=False)
tvStudent.heading('#2', text='Nombres', anchor='center')
tvStudent.column('#2', width=15, anchor='center', stretch=True)
tvStudent.heading('#3', text='Apellidos', anchor='center')
tvStudent.column('#3',width=15, anchor='center', stretch=True)
tvStudent.heading('#4', text='Fecha_Na', anchor='center')
tvStudent.column('#4',width=15, anchor='center', stretch=True)
tvStudent.heading('#5', text='Direccion', anchor='center')
tvStudent.column('#5',width=15, anchor='center', stretch=True)
tvStudent.heading('#6', text='Edad', anchor='center')
tvStudent.column('#6', width=15, anchor='center', stretch=True)
tvStudent.heading('#7', text='long_Cabello', anchor='center')
tvStudent.column('#7', width=15, anchor='center', stretch=True)
tvStudent.heading('#8', text='Altura', anchor='center')
tvStudent.column('#8', width=15, anchor='center', stretch=True)
tvStudent.heading('#9', text='Sexo', anchor='center')
tvStudent.column('#9', width=15, anchor='center', stretch=True)

tvStudent.place(x=40, y=400, height=200, width=640)

if conexion.is_connected() == False:
            conexion.connect()
        
tvStudent.delete(*tvStudent.get_children())  # Limpiar el treeview tvStudent
        # Insertar registro en la tabla student_master de la base de datos de estudiantes
db_cursor.execute("use empleadoPredictivo")  # Interactuar con la base de datos
sql = "SELECT * FROM datos"
db_cursor.execute(sql)
total = db_cursor.rowcount
        
print("Entradas de datos totales:" + str(total))
rows = db_cursor.fetchall()
Numero = ""
Nombre= ""
Apellido = ""
Fecha_nacimiento = ""
Direccion = ""
Edad = ""
Long_cabello = ""
Altura = ""
Genero = ""
for row in rows:
    Numero = row[0]
    Nombre= row[1]
    Apellido = row[2]
    Fecha_nacimiento = row[3]
    Direccion = row[4]
    Edad = row[5]
    Long_cabello = row[6]
    Altura = row[7]
    Genero = row[8]
    tvStudent.insert("", 'end', text=Numero, values=(Numero, Nombre, Apellido, Fecha_nacimiento, Direccion, Edad, Long_cabello, Altura, Genero))

ws.mainloop()
