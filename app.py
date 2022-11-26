import os
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__, template_folder='template')
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='imvital'
mysql.init_app(app)

#---------------------------------------------------------#
#----------------Plantilla inicio-------------------------#

@app.route('/')
def inicio():
    return render_template('plantilla/index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('plantilla/nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('plantilla/contacto.html')

@app.route('/login')
def admin_login():
    return render_template('plantilla/login.html')

@app.route('/login', methods=['POST'])
def admin_login_post():
     
     _usuario=request.form['txtusuario']
     _password=request.form['txtcontraseña']

     print(_usuario)
     print(_password)
     return render_template("administrador/index_admin.html")

#-------------------------------------------------------#
#----------------administrador--------------------------#

@app.route('/imgs/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('template/administrador/imgs'), imagen)

@app.route('/administrador')
def admin_index():
   #----conexion a base de datos-------#  
    conexion=mysql.connect()
    Cursor=conexion.cursor()
    Cursor.execute("SELECT * FROM `informaciontercero`")
    informacion=Cursor.fetchall()
    conexion.commit()



    print(informacion)
   

    return render_template('administrador/index_admin.html', index_admin=informacion)





@app.route('/administrador/informacion/guardar', methods=['GET','POST'])
def admin_guardar_datos():
    if request.method=='POST':
    
        _tipodocumento=request.form['txttipodocumento']
        _identificacion=request.form['txtid']
        _nombre=request.form['txtnombre']
        _apellido=request.form['txtapellido']
        _celular=request.form['txttelefono']
        _direccion=request.form['txtdireccion']
        _eps=request.form['txteps']
        _factor=request.form['txtgruposanguineo']
        _imagen=request.files['txtimagen']
        _fechanacimiento=request.form['txtfechanacimiento']

        
        tiempo= datetime.now()
        horaActual=tiempo.strftime('%Y%H%M%S')

        if _imagen.filename!="":
            nuevoNombre=horaActual+"_"+_imagen.filename
            _imagen.save("template/administrador/imgs/"+nuevoNombre)

    sql="INSERT INTO `informaciontercero`(`id`, `Tipo_documento`, `Identificacion`, `Nombres`, `Apellidos`, `Telefono`, `Direccion`, `eps`, `Tipo_de_sangre`, `Imagen`, `Fecha_Nacimiento`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"        
    datos=(_tipodocumento, _identificacion, _nombre, _apellido, _celular, _direccion, _eps, _factor, nuevoNombre, _fechanacimiento)


    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()



    print(_tipodocumento)
    print(_identificacion)
    print(_nombre)
    print(_apellido)
    print(_celular)
    print(_direccion)
    print(_eps)
    print(_factor)
    print(_imagen)
    print(_fechanacimiento)

    return redirect('/administrador/informacion' )


@app.route('/administrador/informacion/patologia', methods=['POST'])
def admin_patologia():

    _patologias=request.form['txtpatologia']
    _obspatologias=request.form['txtobspatologias']

    sql="INSERT INTO `patologias_temp`(`Id`, `patologia`, `observacion`) VALUES (NULL,%s,%s)"
    datos1=(_patologias,_obspatologias)

    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos1)
    conexion.commit()

    print(_patologias)
    print(_obspatologias)

    return redirect('/administrador/informacion')

@app.route('/administrador/informacion/alergias', methods=['POST'])
def admin_alergia():

    _alergias=request.form['txtalergias']
    _obsalergias=request.form['txtobsalergias']

    sql="INSERT INTO `alergias_temp`(`Id`, `alergias`, `observacion`) VALUES (NULL,%s,%s)"
    datos2=(_alergias,_obsalergias)

    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos2)
    conexion.commit()

    print(_alergias)
    print(_obsalergias)

    return redirect('/administrador/informacion')

@app.route('/administrador/informacion/borrarpatologia', methods=['POST'])
def admin_borrar_patologias():
        _id=request.form['eliminarpatologia']
        print(_id)

        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("SELECT * FROM `patologias_temp` where Id=%s", (_id) )
        borrarpatologias=Cursor.fetchall()
        conexion.commit()
        print(borrarpatologias)

        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("DELETE FROM `patologias_temp` WHERE Id=%s", (_id) )
        conexion.commit()


        return redirect('/administrador/informacion')


@app.route('/administrador/informacion/borraralergia', methods=['POST'])
def admin_borrar_alergias():
        _id=request.form['eliminaralergia']
        print(_id)

        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("SELECT * FROM `alergias_temp` where Id=%s", (_id) )
        borraralergias=Cursor.fetchall()
        conexion.commit()
        print(borraralergias)

        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("DELETE FROM `alergias_temp` WHERE Id=%s", (_id) )
        conexion.commit()


        return redirect('/administrador/informacion')


@app.route('/administrador/informacion')
def admin_infomedica():

    conexion=mysql.connect()
    Cursor=conexion.cursor()
    Cursor.execute("SELECT * FROM `patologias_temp`")
    patologia2=Cursor.fetchall()
    conexion.commit()  

    conexion=mysql.connect() 
    Cursor=conexion.cursor()
    Cursor.execute("SELECT `Nombre_Eps` FROM `directorio_eps`")
    eps=Cursor.fetchall()
    conexion.commit()

    print(eps)     
    print(patologia2)

    return render_template('administrador/informacion.html', informacion=patologia2 and eps)



  
     
      
#--------------------------------------------------------------------------------------------------#
#-------------------------------------------master-------------------------------------------------#

@app.route('/master/index_master')
def master():
   #----conexion a base de datos-------#  
    conexion=mysql.connect()
    Cursor=conexion.cursor()
    Cursor.execute("SELECT * FROM `informaciontercero`")
    datostercero=Cursor.fetchall()
    conexion.commit
    print(datostercero)
    return render_template('/master/index_master.html', index_master=datostercero)  

    

@app.route('/master/index_master/borrar', methods=['POST'])
def master_borrar():
        _id=request.form['txteliminar']
        print(_id)
        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("SELECT imagen FROM `informaciontercero` WHERE Identificacion=%s", (_id) )
        informacion=Cursor.fetchall()
        conexion.commit()
        print(informacion)

        if os.path.exists("template/administrador/imgs/"+str(informacion[0][0])):
            os.unlink("template/administrador/imgs/"+str(informacion[0][0]))

        conexion=mysql.connect()
        Cursor=conexion.cursor()
        Cursor.execute("DELETE FROM `informaciontercero` WHERE Identificacion=%s", (_id) )
        conexion.commit()


        return redirect('/master/index_master')
@app.route('/master/eps')
def master_eps():

    return render_template('/master/eps.html')

@app.route('/master/admin_info')
def master_info():

    return render_template('/master/admin_info.html')


if __name__=='__main__':
    app.run(debug=True)


    