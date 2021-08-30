import re
import datetime
import pandas as pd
from RIPS_helper import *
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import re
import pandas as pd
import os
import datetime
import numpy as np
import pandas as pd
import math
from RIPS_content_checker_R import *

##Dicionarios
from act_eco import *
from SCIAN2008 import *
cat_loc = cat2list('Catalogos/LocalidadesRIPS.xlsx',2)
pais = pd.read_csv('Catalogos/Paises.txt', encoding="ISO-8859-1", sep=";", header=None, dtype=str)
cat_mon = open_txt('Catalogos/cat_mon')
cat_casfim = open_txt('Catalogos/casfim_claves.txt')
cat_suc=[]

#cat_suc = open_txt("Catalogos/donde_suc.txt") #Donde
#cat_suc = ['ED','KT','X','D','DY','EP','KP','GG','G','DO','PL','FV','T','J','H','M','MG','MD','MV','MS',
# 'MO','ME','EC','P','HC','EG','EE','EA','DU','FY','GJ','PF']#CI

#cat_suc_0 = open_txt("Catalogos/donde_suc_0.txt")
#Cat_suc = open_txt('/home/rvelez/Projects/RIPS/Catalogos/sucursales_donde_original.txt')
# El catalogo de paises me sirve en lista.
cat_nac = list(pais[1])
############################# DAVID ARTEAGA #############################
####################################
#Para el catalogo de localidades ver.2

cat = open('Catalogos/Localidades.csv',"r")
a=pd.DataFrame(cat)
a2=a.values.tolist()
cat_loc2=[]
for i in a2:
    for k in i:
        cat_loc2.append(k)
####################################

err = [] # Lista que contiene todos los errores
#Funcion general para deterimar si la columna es de localidades
def is_loc(localidad):
    if any(not is_number(loc) for loc in localidad):
        return False

    # determina si es localidadcat_suc
    for loc in localidad:
        try:
            ciudad = int(loc)
        except ValueError:
            return False # no es un entero
        if ciudad not in cat_loc:
            return False # localidad no encontrada en el catálogo

    return True


###################DEFINIENDO FUNCIONES PARA VALIDAR CONTENIDO
#DEfininendo diccionario de funciones
def is_col(col, col_num):

    if col_num < 1 or col_num > 41:
        return False

    switcher = {
                    1:is_col1, 2:is_col2, 3:is_col3, 4:is_col4,
                    5:is_col5, 6:is_col6, 7:is_col7, 8:is_col8,
                    9:is_col9, 10:is_col10, 11:is_col11, 12:is_col12,
                    13:is_col13, 14:is_col14, 15:is_col15, 16:is_col16,
                    17:is_col17, 18:is_col18, 19:is_col19, 20:is_col20,
                    21:is_col21, 22:is_col22, 23:is_col23, 24:is_col24,
                    25:is_col25, 26:is_col26, 27:is_col27, 28:is_col28,
                    29:is_col29, 30:is_col30, 31:is_col31, 32:is_col32,
                    33:is_col33, 34:is_col34, 35:is_col35, 36:is_col36,
                    37:is_col37, 38:is_col38, 39:is_col39, 40:is_col40,
                    41:is_col41
                }

    return switcher[col_num](col)

#======================Columna 1=================================
#======================TIPO DE REPORTE===========================
def is_col1(df):    
    ############################# DAVID ARTEAGA #############################
    c_2 = df[0]
    NAN = c_2.isna()
    # Contiene los numeros aceptables de filas que se extrageron de las filas principales
    lista_aceptable=[]
    for i in range(len(df[0])):
        a=df.iloc[i]
        b=a.isnull().sum()
        #print(b)
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    
    #print(lista_aceptable)
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[0]
        numeros.append(col)
   # print(lista)
        
    import math #PARA LA FUNCION ISNAN
    #print(numeros)
    ################################ E  
    contador2=0
    for e in range(len(numeros)):
        try:
            if math.isnan(numeros[e]):
                err.append('vacio, Columna 1, Tipo_de_reporte, registro ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
                #', Columna 7, sucursales, registro ' + str(i+1) + ', campo ' + str(df[6][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
                break
            else:
                True
                err.append("No vacio")
        except:
            break
        contador2+=1
    
    ############################################################
#C
    #Checando que la Longitud se correcta
    try:
        for i in range(len(c_2)):
            if len(c_2[i])>1:
                err.append('longitud, Columna 1, Tipo_de_reporte, registro ' + str(i+1) +  ", La longitud del campo excede lo dispuesto en el DOF")
                break
            else:
                if c_2[i] not in ['1','2']:
                    err.append('catalogo, Columna 1, Tipo_de_reporte, registro ' + str(i+1) + ', La informacion de la columna no se encuentra deacuerdo con el catalogo')

    except:
        True
        #err.append("Columna 2, fila"+str(i+1) + ' Se encuentra vacia')
    return err
#A




#======================Columna 2 INUSUALES======================
#======================Periodo del reporte======================
def is_col2_in(df):
    ############################# DAVID ARTEAGA #############################
    c_2 = df[1]
    NAN = c_2.isna()
    # Contiene los numeros aceptables de filas que se extrageron de las filas principales
    lista_aceptable=[]
    for i in range(len(df[1])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[1]
        numeros.append(col)
    import math #PARA LA FUNCION ISNAN
    #if math.isnan(numeros[0]):
    #    print("aaaaaaaa")
################################ E  
    contador2=0
    for e in range(len(numeros)):
        try:
            if math.isnan(numeros[e]):
                #err.append('Columna 2, fila ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
                err.append('vacio, Columna 2, periodo_del_reporte, registro ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
                break
            else:
                True
                err.append("No vacio")
        except:
            break
        contador2+=1
    #Convierto los NaN a ceros para que lo pueda leer
    #c_2 = c_2.fillna('0')
############################################################
#F y D
    #Checando que la Longitud se correcta
    try:
        for i in range(len(c_2)):
            if len(c_2[i])>8 or len(c_2[i])<8:
                #err.append('Columna 2, fila ' + str(i+1) + ', registro ' + str(c_2[i]) + ": La cadena de números es mayor o menor a una longitud de 8 y La longitud del campo excede lo dispuesto en el DOF")
                err.append('longitud, Columna 2, periodo_del_reporte, registro ' + str(i+1) + ', registro ' + str(c_2[i]) + " La cadena de números es mayor o menor a una longitud de 8 y La longitud del campo excede lo dispuesto en el DOF")
############################################################
#A  
        contador=0
        for i in c_2:   
            try:
                if int(i) == False:
                    False
            except:
                err.append('alfabetico, Columna 2, periodo_del_reporte, registro ' + str(contador+1) + ', registro ' + str(i) + ": Hay información alfabética en el campo")
            contador+=1
############################################################
#B  
        contador2=0
        for i in c_2:
            k=i[0:4]
            #print(k)
            if int(k) < 2014:
                err.append('fecha, Columna 2, periodo_del_reporte, registro ' + str(contador2+1) + ', registro ' + str(i) + ": Los números de año son inferiores a 2014")
            contador2+=1
############################################################
#C
        contador3=0
        for i in c_2:
            k=i[4:6]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                True
            else:
                err.append('fecha, Columna 2, periodo_del_reporte, registro ' + str(contador3+1) + ', registro ' + str(i) + ": Los números de mes son distintos a los números 1 al 12")
            contador3+=1
        ################################## D
        contador5=0
        for i in numeros:
            k=i[6:8]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'
                    ,'21','22','23','24','25','26','27','28','29','30','31']:
                True
            else:
                err.append('fecha, Columna 2, periodo_del_reporte, registro ' + str(contador5+1) + ', registro ' + str(i) + ": Los números del dia son distintos a los números 1 al 31")
            contador5+=1
    except:
        True
        #err.append("Columna 2, fila"+str(i+1) + ' Se encuentra vacia')
    return err
#======================Columna 3=================================
#======================FOLIO INUSUALES===========================

def is_col3_in(df):
    NAN = df[2].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 3, folio_inusuales, registro ' + str(i+1) + ', registro ' + str(df[2][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            break
        else:
            if df[2][0] != '000001':
                err.append('numerico, Columna 3, folio_inusuales, registro ' + str(1) + ', registro ' + str(df[2][0]) + ': El primer registro no contiene en la columna 3 0000001')
                break
    #Convierto los NaN a ceros para que lo pueda leer
    df[2] = df[2].fillna('000000')

    #Checando que la Longitud se correcta
    for i in range(len(df[2])):
        if len(df[2][i])>6:
            err.append('longitud, Columna 3, folio_inusuales, registro ' + str(i+1) + ', registro ' + str(df[2][i]) +": La longitud del campo excede lo dispuesto en el DOF ")
            break
    try:
        f = df[2].astype(int)
        F = df[33]
        F = df[33].astype(int)
        for i in range(len(F)-1):
            if F[i+1] - F[i] == 1:
                True
            elif F[i+1] - F[i] != 1:
                if f[i+1] - f[i] == 1:
                    True
                elif f[i+1] - f[i] != 1:
                    err.append('incremento, Columna 3, folio_inusuales, registro ' + str(i+1) + ', registro ' + str(F[i]) + ":  El campo no continua el incremento de la serie numerica del folio")
    except:
        True
        #err.append("¡ERROR PELIGROSO LA COLUMNA 33 SE ENCUENTRA VACIA Y AFECTA TODO EL DOCUMENTO!")
    return err
#======================Columna 4=================================
#======================ORGANO SUPERVISOR=========================
def is_col4(df):
#D
    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 4, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            if df[i][0] == '0':
                True                
            else:
                err.append('numerico, Columna 4, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no comienza con un 0" )
                break
    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('000000')
#E
    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[i])>6 and NAN[i] == False:
            err.append('longitud, Columna 4, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")         
#B
    for i in range(len(df)):
        if df[i] not in cat_casfim and NAN[i] != True and len(df[i]) == 6 and df[i][0] == '0':
            err.append('catalogo, Columna 4, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no corresponde al catalogo" )
        else:
            True
#c  
    for i in range(len(df)):
        if '-' in df[i] and NAN[i] != True:
            err.append('alfanumerico, Columna 4, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": No se suprimió el guion intermedio de la clave" )
        else:
            True
    return err
#======================Columna 5=================================
#======================ORGANO SUPERVISOR=========================
def is_col5(df):
    #err = []
    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 5, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            if df[i][0] == '0':
                True                
            else:
                err.append('numerico, Columna 5, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no comienza con un 0" )
                break
    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('000000')
    for i in range(len(df)):
        if len(df[i])>6:
            err.append('longitud, Columna 5, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La longitud del campo es mayor a seis digitos ")
    for i in range(len(df)):
        if df[i] not in cat_casfim and NAN[i] != True and len(df[i])==6 and df[i][0] == '0':
            err.append('catalogo, Columna 5, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no corresponde al catalogo" )
        else:
            True
    for i in range(len(df)):
        if '-' in df[i] and NAN[i] != True:
            err.append('alfanumerico, Columna 5, organo_supervisor, registro ' + str(i+1) + ', registro ' + str(df[i]) + ": No se suprimió el guion intermedio de la clave" )
        else:
            True
    return err
#======================Columna 6=================================
#======================LOCALIDAD=================================
def is_col6i(df):
    for i in range(len(df[5])):
        if df[33][i] == '00' :
            if pd.isna(df[5][i]) == True:
                err.append('vacio, Columna 6, localidad, registro ' + str(i+1) + ', registro ' + str(df[5][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
            elif len(df[5][i])>8:
                err.append('longitud, Columna 6, localidad, registro ' + str(i+1) + ', registro ' + str(df[5][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif int(df[5][i]) in cat_loc:
                True
            elif int(df[5][i]) in cat_suc:
                True
            else:
                err.append('catalogo, Columna 6, localidad, registro ' + str(i+1) + ', registro ' + str(df[5][i]) + ": La localidad señalada no corresponde al catalogo" )
#        elif df[33][i] != '00':
#            if pd.isna(df[5][i]) == False:
#                err.append('Columna 6, fila ' + str(i+1) + ', registro ' + str(df[5][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 7=================================
#======================SUCURSALES================================
#======================PERSONALIZABLE============================
def is_col7i(df):
    for i in range(len(df[6])):
        if df[33][i] == '00' :
            if pd.isna(df[6][i]) == True:
                err.append('vacio, Columna 7, sucursales, registro ' + str(i+1) + ', campo ' + str(df[6][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            elif len(df[6][i])>2:
                err.append('longitud, Columna 7, sucursales, registro ' + str(i+1) + ', campo ' + str(df[6][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif df[6][i] not in cat_suc and len(df[6][i]) == 2:
                err.append('catalogo, Columna 7, sucursales, registro ' + str(i+1) + ', campo ' + str(df[6][i]) + ": El campo no contiene ninguna de las claves de sucursal entregadas por el cliente o el numero ceros " )
#        elif df[33][i] != '00':
#            if pd.isna(df[6][i]) == True:
#                True
#            else:
#                err.append('Columna 7, fila ' + str(i+1) + ', registro ' + str(df[7][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 8=================================
#======================TIPO DE OPERACION=========================
def is_col8i(df):
    cat_op = ['01', '02', '03', '04', '05', '06', '07', '08', '09',
                '10', '11', '12', '13','14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                '30', '31', '32', '33', '34', '35', '36']
    for i in range(len(df[7])):
        if df[33][i] == '00' :
            if pd.isna(df[7][i]) == True:
                err.append('vacio, Columna 8, tipo_de_operacion, registro ' + str(i+1) + ', registro ' + str(df[7][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            elif len(df[7][i])>2:
                err.append('longitud, Columna 8, tipo_de_operacion, registro ' + str(i+1) + ', registro ' + str(df[7][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif df[7][i] not in cat_op:
                err.append('catalogo, Columna 8, tipo_de_operacion, registro ' + str(i+1) + ', registro ' + str(df[7][i]) + ": El tipo de operación no corresponde al catalogo " )
#        elif df[33][i] != '00':
#            if pd.isna(df[7][i]) == True:
#                True
#            else:
#                err.append('Columna 8, fila ' + str(i+1) + ', registro ' + str(df[7][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 9=================================
#======================INSTRUMENTO MONETARIO=====================
def is_col9(df):
    cat_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    for i in range(len(df[8])):
        if df[33][i] == '00':
            if pd.isna(df[8][i]) == True:
                err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            elif len(df[8][i])>2:
                err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif df[8][i] not in cat_list:
                err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ": El tipo de operación no corresponde al catalogo  " )
#        if df[33][i] != '00':
#            if pd.isna(df[8][i]) == True:
#                True
#            else:
#                err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 10=================================
#======================NUMERO DE CUENTA===========================
def is_col10(df):
    for i in range(len(df[9])):
        if df[33][i] == '00':
            if pd.isna(df[9][i]):
                err.append('vacio, Columna 10, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(df[9][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            elif len(df[9][i])>16:
                err.append('longitud, Columna 10, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(df[9][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif len(df[9][i]) == 1:
                err.append('longitud, Columna 10, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(df[9][i]) + ": La longitud del campo contiene un solo carácter numérico diferente a cero")
            elif re.match('[A-Za-z\d]{17}', df[9][i]):
                err.append('longitud, Columna 10, fila ' + str(i+1) + ', registro ' + str(df[9][i]) +" : La longitud del campo  excede lo dispuesto en el DOF, la fila no es válida")
            else:
                True
#        elif df[33][i] == '00':
#            if pd.isna(df[9][i]) == True:
#                True
#            else:
#                err.append('Columna 10, fila ' + str(i+1) + ', registro ' + str(df[9][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 11=================================
#======================MONTO======================================
def is_col11(df):
############################# DAVID ARTEAGA #############################
    mon = df[10]
    ins = df[8]
    #print(ins)
    c_2 = df[10]
    NAN = c_2.isna()
    # Contiene los numeros aceptables de filas que se extrageron de las filas principales
    lista_aceptable=[]
    for i in range(len(df[1])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[10]
        numeros.append(col)
    numeros2=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[8]
        numeros2.append(col)
    try:    
        contador2=0
        for i in range(len(lista_aceptable)):
            if numeros2[i]=='05' or numeros2[i]=='06':
                if float(numeros[i]) % 1 != 0:
                    err.append('catalogo, Columna 11, monto, registro ' + str(lista_aceptable[i]+1) + ', registro ' + str(numeros[i]) + ": El registro es Oro, plata y platino amonedado no se indicaron con un numero de unidades del metal en cantidades enteras, la fila no es válida")
            contador2+=1
    except:
        True
    try:    
        contador=0
        for i in numeros:
            #print(i)
            if re.search('[A-Za-z]',i):    
                err.append('alfanumerico, Columna 11, monto, registro ' + str(lista_aceptable[contador]+1) + ', registro ' + str(i) + ": Hay información alfabética en el campo")
            contador+=1
    except:
        True
    try:
        contador=0
        for i in range(len(df[10])):
            if df[33][i] == '00':
                
                if pd.isna(mon[i]) == True:
                    err.append('vacio, Columna 11, monto, registro ' + str(i+1) + ', registro ' + str(mon[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
               # if pd.isna(ins[i]) == True:
               #     err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(ins[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')c
                #elif len(ins[i])>2:
                #    err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(ins[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                if len(mon[i])>17:
                    err.append('longitud, Columna 11, monto, registro ' + str(i+1) + ', registro ' + str(mon[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                else:
                    err.append('alfanumerico, Columna 11, monto, registro ' + str(j+1) + ', registro ' + str(mon[j]) + ": El registro contiene valores alfabeticos, la fila no es válida")
 #           elif df[33][i] != '00':
 #                   if pd.isna(df[10][i]) == True:
 #                       True
 #                   else:
 #                       err.append('Columna 10, fila ' + str(i+1) + ', registro ' + str(df[10][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
            contador+=1
    except:
        True
    return err
#======================Columna 12=================================
#======================CATALOGO MONEDA============================
def is_col12(df):
    for i in range(len(df[11])):
        if df[33][i] == '00':
            if pd.isna(df[11][i]) == True:
                err.append('vacio, Columna 12, catalogo_moneda, registro ' + str(i+1) + ', registro ' + str(df[11][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
            elif len(df[11][i])>3:
                err.append('longitud, Columna 12, catalogo_moneda, registro ' + str(i+1) + ', registro ' + str(df[11][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif df[11][i] not in cat_mon:
                err.append('catalogo, Columna 12, catalogo_moneda, registro ' + str(i+1) + ', registro ' + str(df[11][i]) + ": La clave no corresponde al catalogo " )
#        elif df[33][i] != '00':
#                if pd.isna(df[11][i]) == True:
#                    True
#                else:
#                    err.append('Columna 12, fila ' + str(i+1) + ', registro ' + str(df[11][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 13=================================
#======================FECHA DE LA OPERACION======================
def is_col13(df):
############################# DAVID ARTEAGA #############################
    c_2 = df[12]
    NAN = c_2.isna()
    # Contiene los numeros aceptables de filas que se extrageron de las filas principales
    lista_aceptable=[]
    for i in range(len(df[12])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    #print(lista_aceptable)
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[12]
        numeros.append(col)
    #print(numeros)
    import math #PARA LA FUNCION ISNAN
    #if math.isnan(numeros[0]):
    #    print("aaaaaaaa")
    for i in range(len(df[12])):
        if df[33][i] == '00':
            if pd.isna(df[12][i]) == True:
                err.append('vacio, Columna 13, fecha_de_la_operacion, registro ' + str(i+1) + ', registro ' + str(df[11][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
################################ E  
    contador2=0
    for e in range(len(numeros)):
        try:
            if math.isnan(numeros[e]):
                #print(numeros[i])
                #err.append('Columna 13, fila ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
                break
            else:
                True
        except:
            True
        contador2+=1
    try:
    ################################### F y D
        #Checando que la Longitud se correcta
        contador3=0
        for i in range(len(numeros)):
            if len(numeros[i])>8 or len(numeros[i])<8:
                err.append('longitud, Columna 13, fecha_de_la_operacion, registro ' + str(lista_aceptable[contador3]+1) + ', registro ' + str(numeros[i]) + ": La longitud del campo excede lo dispuesto en el DOF")
    ################################# A  
        contador=0
        for i in numeros:
            try:
                if int(i) == False:
                    False
            except:
                if len(i)==8:
                    err.append('alfanumerico, Columna 13, fecha_de_la_operacion, registro ' + str(lista_aceptable[contador]+1) + ', registro ' + str(i) + ": Hay información alfabética en el campo")
                break
            contador+=1
    ################################## B  
    #    contador4=0
    #    for i in numeros:
    #        k=i[0:4]
    #        #print(k)
    #        if int(k) < 2014:
    #            err.append('fecha, Columna 13, fecha_de_la_operacion, registro ' + str(lista_aceptable[contador4]+1) + ', registro ' + str(i) + ": Los números de año son inferiores a 2014")
    #        contador4+=1
    ################################## C
        contador5=0
        for i in numeros:
            k=i[4:6]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                True
            else:
                err.append('fecha, Columna 13, fecha_de_la_operacion, registro ' + str(lista_aceptable[contador5]+1) + ', registro ' + str(i) + ": Los números de mes son distintos a los números 1 al 12")
            contador5+=1
    ################################## D
        contador5=0
        for i in numeros:
            k=i[6:8]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'
                    ,'21','22','23','24','25','26','27','28','29','30','31']:
                True
            else:
                err.append('fecha, Columna 13, fecha_de_la_operacion, registro ' + str(lista_aceptable[contador5]+1) + ', registro ' + str(i) + ": Los números de mes son distintos a los números 1 al 31")
            contador5+=1
    except:
        True
#======================Columna 14================================
#======================RELEVANTES DEBE SER VACIA=================
def is_col14(df):
############################# DAVID ARTEAGA #############################
    c_2 = df[13]
    NAN = c_2.isna()
    # Contiene los numeros aceptables de filas que se extrageron de las filas principales
    lista_aceptable=[]
    for i in range(len(df[13])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[13]
        numeros.append(col)
    import math #PARA LA FUNCION ISNAN
    #if math.isnan(numeros[0]):
    #    print("aaaaaaaa")
################################ E  
    contador2=0
    for e in range(len(numeros)):
        try:
            if math.isnan(numeros[e]):
                err.append('vacio, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
                break
            else:
                True
                #err.append("No vacio")
        except:
            break
        contador2+=1
    try:
    ################################# A  
        contador=0
        for i in numeros:
            try:
                if int(i) == False:
                    False
            except:
                if len(i)==8:
                    err.append('alfanumerico, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador]+1) + ', registro ' + str(i) + ": Hay información alfabética en el campo")
            contador+=1
    ################################### F y D
        #Checando que la Longitud se correcta
        contador3=0
        for i in range(len(numeros)):
            if len(numeros[i])>8 or len(numeros[i])<8:
                err.append('longitud, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador3]+1) + ', registro ' + str(numeros[i]) + ": La longitud del campo excede lo dispuesto en el DOF")
    ################################## B  
        contador4=0
        for i in numeros:
            k=i[0:4]
            #print(k)
            if int(k) < 2014 and len(i)==8:
                err.append('fecha, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador4]+1) + ', registro ' + str(i) + ": Los números de año son inferiores a 2014")
            contador4+=1
    ################################## C
        contador5=0
        for i in numeros:
            k=i[4:6]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                True
            else:
                err.append('fecha, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador5]+1) + ', registro ' + str(i) + ": Los números de mes son distintos a los números 1 al 12")
            contador5+=1
    ################################## D
        contador5=0
        for i in numeros:
            k=i[6:8]
            #print(k)
            if k in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'
                    ,'21','22','23','24','25','26','27','28','29','30','31']:
                True
            else:
                err.append('fecha, Columna 14, fecha_de_deteccion, registro ' + str(lista_aceptable[contador5]+1) + ', registro ' + str(i) + ": Los números del dia son distintos a los números 1 al 31")
            contador5+=1
    except:
        True
#======================Columna 15=================================
#======================CATALOGO PAIS==============================
# B
def is_col15(df):
    for i in range(len(df[14])):
        if df[33][i] == '00':
            if pd.isna(df[14][i]) == True:
                err.append('vacio, Columna 15, pais, registro ' + str(i+1) + ', registro ' + str(df[14][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
            elif len(df[14][i])>2:
                err.append('longitud, Columna 15, pais, registro ' + str(i+1) + ', registro ' + str(df[14][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif (df[14][i]) not in cat_nac and df[14][i] !='0':
                err.append('catalogo, Columna 15, pais, registro ' + str(i+1) + ', registro ' + str(df[14][i]) + ": El campo no contiene una clave encontrada en el catalogo o un cero " )
            elif (df[14][i]) == '0':
                True
                #err.append('Columna 15, fila ' + str(i+1) + ', registro ' + str(df[14][i]) + ": El campo de la columna contiene un 0" )
            else:
                True
#        elif df[33][i] != '00':
#                if pd.isna(df[14][i]) == True:
#                    True
#                else:
#                    err.append('Columna 15, fila ' + str(i+1) + ', registro ' + str(df[14][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 16=================================
#======================TIPO DE PERSONA============================
def is_col16(df):
############################# DAVID ARTEAGA #############################
    lista_aceptable=[]
    for i in range(len(df[15])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[15]
        numeros.append(col)
    per = df[15]
    for i in range(len(df[15])):
        if df[33][i] == '00':
            if pd.isna(df[15][i]) == True:
                err.append('vacio, Columna 16, tipo_de_persona, registro ' + str(i+1) + ', registro ' + str(numeros[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
    contador=0
    for i in numeros:
        try:
            int(i)
            if i == '1' or i=='2':
                True
            else:
                err.append('catalogo, Columna 16, tipo_de_persona, registro ' + str(lista_aceptable[contador]) + ', registro ' + str(numeros[contador]) + ': No se utilizaron las claves establecidas por el formato')
            contador=+1
        except:
            True
            #i == '1' or i=='2'
    try: 
        contador3=0
        for i in numeros:
            if len(i)==1:
                True
            else: 
                err.append('longitud, Columna 16, tipo_de_persona, registro ' + str(lista_aceptable[contador3]) + ', registro ' + str(numeros[contador3]) + ': La longitud del campo excede lo dispuesto en el DOF.')
            contador3=+1
    except:
        True
    return err
#======================Columna 17=================================
#======================RAZON SOCIAL===============================

def is_col17(df):
    per = df[15] #col16
    razon = df[16] #Columna de interes 17
    nombre = df[17]
    rfc = df[18]
    pat = df[19]
    curp = df[21]
    #err = []
    ############################# DAVID ARTEAGA #############################
    lista_aceptable=[]
    for i in range(len(df[16])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[16]
        numeros.append(col)
    #print(numeros)
    contador=0
    for i in numeros:
        try:
        #print(len(i))
            if len(i) >= 300:
                #print(i)
                err.append('longitud, Columna 17, razon_social, registro ' + str(lista_aceptable[contador]+1) + ', registro ' + str(i) + ': El registro supera lo establecido en el DOF')
                contador +=1
        except:
            True
        
    for i in range(len(df[16])):
        if df[33][i] == '00':
            for i in range(len(per)):
                if per[i] == '1':
                    
                    if pd.isna(razon[i]) == True:
                        True
                    else:
                        err.append('relacion, Columna 17, razon_social, registro ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro debe ir vacio, pues es una persona Fisica ')
                        break
                elif per[i] == '2':
                    if pd.isna(razon[i]) == False:
                        if pd.isna(curp[i]) == True:
                            True
                        else:
                            err.append('alfanumerico, Columna 17, razon_social, registro ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro cuenta con caracteres alfanumérico pero la columna 22 ' + str(curp[i]) + ' cuenta con caracteres alfanuméricos indicando en el registro a una persona física y no una moral ')
                    elif pd.isna(razon[i]) == False:
                        if pd.isna(nombre[i]) == False:
                            True
                    elif pd.isna(razon[i]) == False:
                        if ((pd.isna(paterno[i]) == True) and (pd.isna(materno[i]) == True) ):
                            True
                        else:
                            err.append('relacion, Columna 17, razon_social, registro ' + str(i+1) + ', registro ' + str(razon[i]) + ': El campo cuenta con caracteres alfanumérico y las columnas 19 y 20 del registrocuentan con caracteres alfanuméricos o XXXX, indicando una persona física y no una moral')
                    else:
                        err.append('relacion, Columna 17, razon_social, registro ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro no debe ir vacio, pues es una persona Moral ')
            break
                #else:
                #    err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(per[i]) +': El registro no es una persona Fisica o Moral')
#        elif df[33][i] != '00':
#                if pd.isna(df[16][i]) == True:
#                    True
#                else:
#                    err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(df[16][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 18=================================
#======================NOMBRE===============================
def is_col18(df):
    per = df[15]#col16
    razon = df[16]#col17
    nombre = df[17]#col18
    paterno = df[18]#col19
    materno = df[19]#col20
    for i in range(len(df[17])):
        if df[33][i] == '00':
            for i in range(len(per)):
                if per[i] == '1':
                    if len(str(nombre[i]))>60:
                        err.append('longitud, Columna 18, nombre, registro ' + str(i+1) + ', registro ' + str(nombre[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                    elif pd.isna(nombre[i]) == False:
                        True
                    elif pd.isna(nombre[i]) == False:
                        if pd.isna(razon[i]) == False:
                            err.append('vacio, Columna 18, nombre, registro ' + str(i+1) + ', registro ' + str(razon[i]) + ': El campo debe ir vacio pues es una persona fisica')
                    else:
                        err.append('vacio, Columna 18, nombre, registro ' + str(i+1) + ', registro ' + str(nombre[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')
               #elif per[i] == '2':
               #    if pd.isna(nombre[i]) == True:
               #        True
               #    else:
               #        err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(nombre[i]) + ': El campo  es incorrecto pues las columnas 19 y 20 contienen caracteres alfanuméricos y el campo de la columna esta vacio ')
                #else:
                #    err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')

#        elif df[33][i] != '00':
#                if pd.isna(df[17][i]) == True:
#                    True
#                else:
#                    err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(df[17][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 19=================================
#======================APELLIDO PATERNO===========================
def is_col19(df):
    nac = df[14] #col15
    per = df[15]#col16
    nombre = df[17]#col18
    paterno = df[18]#col19
    materno = df[19]#col20
    rfc = df[20] #col21
    curp = df[21] #col22
    for i in range(len(df[18])):
        if df[33][i] == '00':
            for i in range(len(per)):
                if per[i] == '1':
                    if nac[i] == 'MX':
                        try:
                            if pd.isna(paterno[i]) == True :
                                if pd.isna(materno[i]) == False:
                                    err.append('vacio, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(paterno[i]) + ': esta vacío, si no se conoce el apellido paterno colocar XXXX')

                            if pd.isna(nombre[i]) == True  or 'XXXX'in nombre[i]:
                                if pd.isna(curp[i]) == False:
                                    err.append('relacion, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos ')
                            paterno = paterno.fillna('0')
                            if len(paterno[i])>30:
                                err.append('longitud, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(paterno[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                        except:
                            True
                            #elif pd.isna(curp[i]) == True:
                            #    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
                    elif nac[i] != 'MX':
                        if (pd.isna(df[18][i]) == True ):
                            if pd.isna(df[21][i]) == False:
                                if not re.match('[NA]|[NAN]',df[21][i]) :
                                    err.append('vacio, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')
                elif per[i] == '2':
                    if pd.isna(df[18][i]) == False:
                        err.append('vacio, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(df[18][i]) + ': El registro debe ir vacio, pues es una persona Moral ')
                    elif pd.isna(df[19][i]) == False:
                        if pd.isna(curp[i]) == True:
                            err.append('relacion, Columna 19, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(df[19][i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
                #else:
                #    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')
        #elif df[33][i] != '00':
        #        if pd.isna(df[18][i]) == True:
        #            True
        #        else:
        #            err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(df[18][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")

    return err

#======================Columna 20=================================
#======================APELLIDO MATERNO===========================
def is_col20(df):
    # David Arteaga
   #nac = df[14] #col15
   #per = df[15]#col16
   #nombre = df[17]#col18
   #paterno = df[18]#col19
   #materno = df[19]#col20
   #rfc = df[20] #col21
   #curp = df[21] #col22
    lista_aceptable=[]
    for i in range(len(df[19])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    materno=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[19]
        materno.append(col)
    per=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[15]
        per.append(col)
    curp=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[21]
        curp.append(col)
    paterno=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[18]
        paterno.append(col)
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(materno[i]) == True and pd.isna(paterno[i]) == False and pd.isna(curp[i]) == False:
                err.append("relacion, Columna 19, apellido_materno, registro "+ str(lista_aceptable[i]+1) +", registro "+materno[i]+" el campo esta vacio pero la columna 19 contiene XXXX y la columna 22 contiene caracteres alfanuméricos")
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(materno[i]) == False:
                if len(materno[i]) > 30:
                    err.append("longitud, Columna 19, apellido_materno, registro "+ str(lista_aceptable[i]+1) +", registro "+materno[i]+" La longitud del campo excede lo dispuesto en el DOF")
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(materno[i]) == True:
                if re.match('[NA]|[NAN]',str(materno[i])) != None:
                    err.append("relacion, Columna 19, apellido_materno, registro "+ str(lista_aceptable[i]+1) +", registro "+str(materno[i])+" el campo esta vacío si no se conoce el apellido materno colocar XXXX")
                

    #print(materno)
    return err
#======================Columna 21=================================
#======================RFC========================================
def is_col21(df):
############################# DAVID ARTEAGA #############################
    lista_aceptable=[]
    for i in range(len(df[20])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    numeros=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[20]
        numeros.append(col)
##########################################################################        
    contador2=0
    for e in range(len(numeros)):
        try:
            if math.isnan(numeros[e]):
                True
                #err.append('Columna 21, fila ' + str(lista_aceptable[contador2]+1) + ', registro ' + str(numeros[e]) + ' El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
            else:
                True 
        except:
            True
        contador2+=1
#########################################################################  
    contador=0
    for i in numeros:
        try:
            if '-' in i:
                print('alfanumerico, Columna 21, rfc, registro '+str(lista_aceptable[contador]+1) + ', registro '+str(i)+': La columna contiene un campo alfanumérico con un guion o espacio')
        except:
            True
        contador+=1
##########################################################################
    for i in range(len(df[20])):
        if df[33][i] == '00':
            #Reglas para el RFC
            for i in range(len(df)):
                #Personas Fisicas, deben tener al menos una de tres
                if df[15][i] == '1':
                    if ( (pd.isna(df[20][i]) == False) and (pd.isna(df[21][i]) == False) and (pd.isna(df[22][i]) == False) ):
                        True
                    elif ( (pd.isna(df[20][i]) == False) and (pd.isna(df[21][i]) == False) ):
                        True
                    elif ( (pd.isna(df[20][i]) == False) and (pd.isna(df[22][i]) == False) ):
                        True
                    elif ( (pd.isna(df[21][i]) == False) and (pd.isna(df[22][i]) == False) ):
                        True
                    elif ( (pd.isna(df[20][i]) == True) and (pd.isna(df[21][i]) == True) and (pd.isna(df[22][i]) == True) ):
                        err.append( 'relacion, Columna 21, rfc, registro ' + str(i+1) + ', registro ' + str(df[20][i]) + ': El registro de las columnas 22 y 23 están vacias al igual que la columna 21 ')
                #Personas Morales, deben tener al menos una de dos
                elif df[15][i] == '2':
                    if ( (pd.isna(df[20][i]) == False) and (pd.isna(df[22][i]) == False) ):
                        True
                    elif ( (pd.isna(df[20][i]) == False)  ):
                        True
                    elif ( (pd.isna(df[22][i]) == False)  ):
                        True
                    elif ( (pd.isna(df[20][i]) == True) and (pd.isna(df[22][i]) == True) ):
                        err.append( 'relacion, Columna 21, rfc, registro ' + str(i+1) + ', registro ' + str(df[20][i]) + ': El registro de la columna 23 está vacia al igual que la columna 21 ')
            for j in range(len(df[20])):
                if pd.isna(df[20][i]) == False:
                    if not re.match('([A-Z&]{3,4}[\d]{6}[\s]?(?:[A-Z\d]{3})?)|0$',df[20][i]):
                        """rfc_valid = [rfc_validacion(list(df[20])) for i in range(len(df[20]))]
                        #print("RFC")
                        for i in range(len(rfc_valid)):
                            if rfc_valid[i][1] == 'Resultado: Clave de RFC inválida':
                                for j in rfc_valid[i]:
                                    #err.append(str(rfc_valid[i][1])+' '+l[i])
                                    err.append( 'Columna 21, fila ' + str([i+1 for i in range(len(df[20]))]) + ', registro ' + str([df[20][i] for i in range(len(df[20]))]) + rfc_valid[i][1])
                        print("RFC Leido")"""
                        err.append('alfanumerico, Columna 21, rfc, registro ' + str(i+1) + ', registro ' + str(df[20][i]) + ": El RFC no debe de utilizar guion , espacio o cualquier otro tipo de carácter que no forme parte de el.")
                    else:
                        True
            for k in range(len(df[20])):
                    if len(str(df[20][k])) > 15:
                        err.append('longitud, Columna 21, rfc, registro ' + str(k+1) + ', registro ' + str(df[20][k]) + ": La longitud del campo excede lo dispuesto en el DOF")
            break
#        elif df[33][i] != '00':
#            if pd.isna(df[20][i]) == True:
#                True
#            else:
#                err.append('Columna 21, fila ' + str(i+1) + ', registro ' + str(df[20][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 22=================================
#======================CURP=======================================

def is_col22(df):
    # David Arteaga
   #nac = df[14] #col15
   #per = df[15]#col16
   #nombre = df[17]#col18
   #paterno = df[18]#col19
   #materno = df[19]#col20
   #rfc = df[20] #col21
   #curp = df[21] #col22
    lista_aceptable=[]
    for i in range(len(df[22])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    rfc=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[20]
        rfc.append(col)
    per=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[15]
        per.append(col)
    curp=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[21]
        curp.append(col)
    fecha=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[22]
        fecha.append(col)
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(rfc[i]) == True and pd.isna(fecha[i]) == True and pd.isna(curp[i]) == True:
                err.append("vacio, Columna 21 y 23, curp, registro "+ str(lista_aceptable[i]+1) +", registro "+curp[i]+" se encuentran vacias al igual que la columna 22")
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(curp[i]) == False:
                if len(curp[i]) > 18:
                    err.append("longitud, Columna 22, curp, registro "+ str(lista_aceptable[i]+1) +", registro "+curp[i]+" La longitud del campo excede lo dispuesto en el DOF")
    return err
#======================Columna 23=================================
#=========FECHA DE NACIMIENTO O CONSTITUCIÓN======================
def is_col23(df):
    lista_aceptable=[]
    for i in range(len(df[22])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    fecha=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[22]
        fecha.append(col)
    for i in range(len(df[22])):
        if df[33][i] == '00':
            if pd.isna(df[22][i]) == True and pd.isna(df[20][i]) == True:
                err.append('relacion, Columna 23, fecha_de_nacimiento, registro ' + str(i+1) + ', registro ' + str(df[22][i]) + ': La columna esta vacia al igual que la columna 21')
            if pd.isna(df[22][i]) == True and pd.isna(df[21][i]) == True:
                err.append('relacion, Columna 23, fecha_de_nacimiento, registro ' + str(i+1) + ', registro ' + str(df[22][i]) + ': La columna esta vacia al igual que la columna 22')
            if pd.isna(df[20][i]) == True and pd.isna(df[21][i]) == True:
                err.append('relacion, Columna 23, fecha_de_nacimiento, registro ' + str(i+1) + ', registro ' + str(df[22][i]) + ': La columna 21 y la Columna 22 están vacías al igual que la Columna 23')
            if len(str(df[22][i]))>8:
                err.append('longitud, Columna 23, fecha_de_nacimiento, registro ' + str(i+1) + ', registro ' + str(df[22][i]) +": La longitud del campo excede lo dispuesto en el DOF ")
            else:
                True
    for i in range(len(fecha)):
        #print(fecha[i][4:6])
        try:
            if (pd.isna(fecha[i]) == False) and (fecha[i][0] !='1' or fecha[i][0] !='2') and (fecha[i][1] !='0' and fecha[i][1] !='9'):
                err.append("fecha, Columna 23, fecha_de_nacimiento, registro "+str(lista_aceptable[i])+" registro "+fecha[i]+ " El formato de fecha no es AAAAMMDD")
            elif fecha[i][4:6] not in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                err.append("fecha, Columna 23, fecha_de_nacimiento, registro "+str(lista_aceptable[i])+" registro "+fecha[i]+ " El formato de fecha no es AAAAMMDD")
            elif fecha[i][6:8] not in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'
                        ,'21','22','23','24','25','26','27','28','29','30','31']:
                err.append("fecha, Columna 23, fecha_de_nacimiento, registro "+str(lista_aceptable[i])+" registro "+fecha[i]+ " El formato de fecha no es AAAAMMDD")
        except:
            True
#        elif df[33][i] != '00':
#            if pd.isna(df[22][i]) == True:
#                True
#            else:
#                err.append('Columna 23, fila ' + str(i+1) + ', registro ' + str(df[22][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 24=================================
#======================DOMICILIO==================================
def is_col24(df):
    for i in range(len(df[23])):
        if df[33][i] == '00':
            if pd.isna(df[23][i])== True:
                err.append('vacio, Columna 24, domicilio, registro ' + str(i+1) + ', registro ' + str(df[23][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
            elif len(df[23][i])>60:
                err.append('longitud, Columna 24, domicilio, registro ' + str(i+1) + ', registro ' + str(df[23][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif not re.match("[A-Z0-9Ñ.,:“”/'\s#-]{1,300}",df[23][i]):
                err.append('alfanumerico, Columna 24, domicilio, registro ' + str(i+1) + ', registro ' + str(df[23][i]) + ": El domicilio no es correcto La fila no es válida")
            else:
                True
        #    return is_date(df[1], is_col1)
 #       elif df[33][i] != '00':
 #           if pd.isna(df[23][i]) == True:
 #               True
 #           else:
 #               err.append('Columna 24, fila ' + str(i+1) + ', registro ' + str(df[23][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 25=================================
#======================COLONIA====================================
def is_col25(df):
    for i in range(len(df[24])):
        if df[33][i] == '00':
            if pd.isna(df[24][i]) == True:
                err.append('vacio, Columna 25, colonia, registro ' + str(i+1) + ', registro ' + str(df[24][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
            elif len(df[24][i])>30:
                err.append('longitud, Columna 25, colonia, registro ' + str(i+1) + ', registro ' + str(df[24][i]) +": La longitud del campo excede lo dispuesto en el DOF ")
            elif len(df[24][i]) == 1 and df[24][i] != '0':
                err.append('alfabetico, Columna 25, colonia, registro ' + str(i+1) + ', registro ' + str(df[24][i]) +": El campo contiene un solo carácter numérico o alfabetico distinto a 0")
 #       elif df[33][i] != '00':
 #               if pd.isna(df[24][i]) == True:
 #                   True
 #               else:
 #                   err.append('Columna 25, fila ' + str(i+1) + ', registro ' + str(df[24][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 26=================================
#======================LOCALIDAD==================================
def is_col26(df):
    x2=str(cat_loc2)
    x="".join(x2)
    for i in range(len(df[25])):
        if df[33][i] == '00':
            try:
                if pd.isna(df[25][i]) == True:
                    err.append('vacio, Columna 26, localidad, registro ' + str(i+1) + ', registro ' + str(df[25][i]) + ': El registro se encuentra vacio, y es obligatorio ')
                elif len(df[25][i])>8:
                    err.append('longitud, Columna 26, localidad, registro ' + str(i+1) + ', registro ' + str(df[25][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                elif not re.match('[0-9]{1,9}$',df[25][i]):
                    err.append('vacio, Columna 26, localidad, registro ' + str(i+1) + ', registro ' + str(df[25][i]) + ": La localidad no es correcta, la fila no es válida")
                # ESTA PARTE ME COSTO MUCHO TRABAJO POR EL TEMA DEL CATALOGO NO BORRAR! - David Arteaga
                elif not df[25][i] in x:
                    err.append('alfanumerico, Columna 26, localidad, registro ' + str(i+1) + ', registro ' + str(df[25][i]) + ": El campo es alfanumérico pero no coincide con el catalogo")

                else:
                    True
            except:
                err.append('vacio, Columna 26, localidad, registro ' + str(i+1) + ', registro ' + str(df[25][i]) + ': El registro se encuentra vacio, y es obligatorio ')
#        elif df[33][i] != '00':
#            if pd.isna(df[25][i]) == True:
#                True
#            else:
#                err.append('Columna 26, fila ' + str(i+1) + ', registro ' + str(df[25][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 27=================================
#======================TELEFONO==================================
def is_col27(df):
    for i in range(len(df[26])):
        if df[33][i] == '00':
            if pd.isna(df[26][i]) == False:
                if len(df[26][i])>40:
                    err.append('longitud, Columna 27, telefono, registro ' + str(i+1) + ', registro ' + str(df[26][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                elif not re.match('(([\d]{10,12})$|([CELULAR\s0-9\s/FIJO]{1,}))',df[26][i]):
                    err.append('alfanumerico, Columna 27, telefono, registro ' + str(i+1) + ', registro ' + str(df[26][i]) + ": El telefono no es válido")
            elif pd.isna(df[26][i]) == True:
                True
#        elif df[33][i] != '00':
#            if pd.isna(df[26][i]) == True:
#                True
#            else:
#                err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[26][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#======================Columna 28=================================
#======================ACTIVIDAD==================================
def is_col28(df,act_eco):
    for i in range(len(df[27])):
        if df[33][i] == '00':
            if pd.isna(df[27][i])== True:
                True #No es necesariamente esta porque no es obligatorio
                #err.append('Columna 28, fila ' + str(i+1) + ', registro ' + str(df[27][i]) + ': El registro se encuentra vacio ')
            elif len(df[27][i])>7:
                err.append('longitud, Columna 28, actividad, registro ' + str(i+1) + ', registro ' + str(df[27][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif df[27][i] not in act_eco:
                err.append('alfanumerico, Columna 28, actividad, registro ' + str(i+1) + ', registro ' + str(df[27][i]) + ": El campo contiene caracteres alfanuméricos que no corresponden al catalogo" )
            else:
                True
#        elif df[33][i] != '00':
#            if pd.isna(df[27][i]) == True:
#                True
#            else:
#                err.append('Columna 28, fila ' + str(i+1) + ', registro ' + str(df[27][i]) + ": El registro debe ir vacio, ya que se trata de un reporte Inusual.")
    return err
#============================E.H=======================================
#===========LAS COLUMNAS SIGUIENTES DEBEN DE ESTAR VACIAS==============
#==========================Para relevantes=============================

#======================Columnas 29-41==============================
#======================VACIO=======================================
def is_col29(df):
    lista_aceptable=[]
    for i in range(len(df[28])):
        a=df.iloc[i]
        b=a.isna().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    vacio=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[28]
        vacio.append(col)
    
    for i in range(len(vacio)):
        if pd.isna(vacio[i]) == False:
            err.append("Columna 29, registro "+str(lista_aceptable[i]+1)+", registro "+str(vacio[i])+ " tiene caracteres alfanumericos")
    return err
def is_col30(df):
    #err = []
    #print(df)
    lista_aceptable=[]
    for i in range(len(df[29])):
        a=df.iloc[i]
        b=a.isna().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    vacio=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[29]
        vacio.append(col)
    
    for i in range(len(vacio)):
        if pd.isna(vacio[i]) == False:
            err.append("vacio, Columna 30, vacio, registro "+str(lista_aceptable[i]+1)+", registro "+str(vacio[i])+ " tiene caracteres alfanumericos")
    return err
def is_col31(df):
    #err = []
    #print(df)
    lista_aceptable=[]
    for i in range(len(df[30])):
        a=df.iloc[i]
        b=a.isna().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    vacio=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[30]
        vacio.append(col)
    
    for i in range(len(vacio)):
        if pd.isna(vacio[i]) == False:
            err.append("vacio, Columna 31, vacio ,registro "+str(lista_aceptable[i]+1)+", registro "+str(vacio[i])+ " tiene caracteres alfanumericos")
    return err
def is_col32(df):
    #err = []
    #print(df)
    lista_aceptable=[]
    for i in range(len(df[31])):
        a=df.iloc[i]
        b=a.isna().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    vacio=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[31]
        vacio.append(col)
    
    for i in range(len(vacio)):
        if pd.isna(vacio[i]) == False:
            err.append("vacio, Columna 32, vacio, registro "+str(lista_aceptable[i]+1)+", registro "+str(vacio[i])+ " tiene caracteres alfanumericos")
    return err
def is_col33(df):
    #err = []
    #print(df)
    lista_aceptable=[]
    for i in range(len(df[32])):
        a=df.iloc[i]
        b=a.isna().sum()
        if b in [29,31]:
            True
            #err.append("Fila NO aceptable")
        else:
            lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    vacio=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[32]
        vacio.append(col)
    
    for i in range(len(vacio)):
        if pd.isna(vacio[i]) == False:
            err.append("vacio, Columna 33, vacio, registro "+str(lista_aceptable[i]+1)+", registro "+str(vacio[i])+ " tiene caracteres alfanumericos")
    return err
#============================E.H=======================================
#===========LAS COLUMNAS SIGUIENTES SON PARA INUSUALES=================
#======================================================================

#======================Columna 34=================================
#===============Consecutivo de cuentas============================

def is_col34(df):
    f = df[2].astype(int)
    F = df[33]
    NAN = F.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 34, consecutivo_de_cuentas, registro ' + str(i+1) + ', registro ' + str(F[i]) + ': El campo del registro principal esta vacio pero existen registros de consecutivos de cuentas/ personas relacionadas en los renglones subsecuentes')
            #err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    F = F.fillna('00')
    #Checando que la Longitud se correcta
    for i in range(len(F)):
        if len(F[i])>2:
            err.append('longitud, Columna 34, consecutivo_de_cuentas, registro ' + str(i+1) + ', registro ' + str(i) +": La longitud del campo excede lo dispuesto en el DOF ")
            #err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
    if F[0] != '00' and len(F[0])==2:
            err.append('relacion, Columna 34, consecutivo_de_cuentas, registro ' + str(i+1) + ', registro ' + str(i) + ': El campo de la columna 34 del registro de la operacion principal cuenta con un valor distinto a 00')
            #err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
#    try:
#        F = df[33].astype(int)
#        for i in range(len(F)-1):
#            if F[i+1] - F[i] == 1:
#                True
#            elif F[i+1] - F[i] != 1:
#                if f[i+1] - f[i] == 1:
#                    True
#                elif f[i+1] - f[i] != 1:
#                    err.append('Columna 3 folio ' + str(i+1) + ', registro ' + str(F[i]) + ":  El folio principal no es consecutivo")
#                    err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
#                elif F[i] != 0 :
#                    err.append('Columna 34, fila ' + str(i+1) + ', registro ' + str(F[i]) + ": B. El campo de la columna 34 del registro de la operacion principal cuenta con un valor distinto a 00 ")
#                   # err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
#                elif pd.isna(F[i]) == True:
#                    err.append('Columna 34, fila ' + str(i+1) + ', registro ' + str(c[i]) + ": C. El campo del registro principal esta vacio pero existen registros de consecutivos de cuentas/ personas relacionadas en los renglones subsecuentes")
#                    #err.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
#            else:
#                err.append('Columna 34' + registro + str(i+1) + 'Hay un error')
#                #errr.append("¡ERROR PELIGROSO AFECTA TODO EL DOCUMENTO!")
#    except:
#        True
        #err.append("¡ERROR PELIGROSO LA COLUMNA 33 SE ENCUENTRA VACIA Y AFECTA TODO EL DOCUMENTO!")
    return err
#======================Columna 35=================================
#============Num_cuneta personas relaciona========================

def is_col35(df):
    cta = df[34]
    F = df[33]
    NAN = F.isna()
    for i in range(len(cta)):
        if F[i] == '00':
            if pd.isna(cta[i]) == False:
                err.append('vacio, Columna 35, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(F[i]) + ': El registro debe ir vacio pues es una cuenta principal ')
            else:
                True
    for i in range(len(cta)):
        if F[i] != '00':
            #Convierto los NaN a ceros para que lo pueda leer
            cta = cta.fillna('0')
            #Checando que la Longitud se correcta
            if len(cta[i])>16:
                err.append('longitud, Columna 35, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(cta[i]) + ": La longitud del campo de la columna excede lo dispuesto en el DOF ")
    ########################## DA: Parte de diferencia ######################
    lista_aceptable2=[]
    lista_no=[]
    for i in range(len(df[40])):
        try:
            if len(df[40][i]) > 5:
                lista_aceptable2.append(i)
        except:
            lista_no.append(i)
    #print(lista_no) # Filas no principales
    #print(lista_aceptable2) #Filas principales
    for i in lista_no:
        #print(df[35])
        if df[33][i] != '00' :
            if pd.isna(df[34][i]) == True and pd.isna(df[35][i]) == False:
                err.append('vacio, Columna 35, numero_de_cuenta, registro ' + str(i+1) + ', registro ' + str(df[34][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio  toda vez que exista informacion alfanumerica en los campos subsecuentes')
    return err
#======================Columna 36================================= 
#================CLAVE DEL SUJETO OBLIGADO========================
def is_col36(df):
    lista_aceptable=[]
    for i in range(len(df[36])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            lista_aceptable.append(i)
            #err.append("Fila NO aceptable")
        else:
            True
            #lista_aceptable.append(i)
            #err.append("Fila Aceptable")
    clave=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[35]
        clave.append(col)
    #print(clave)
    ########################## DA: Parte de diferencia ######################
    lista_aceptable2=[]
    lista_no=[]
    for i in range(len(df[40])):
        try:
            if len(df[40][i]) > 5:
                lista_aceptable2.append(i)
        except:
            lista_no.append(i)
    #print(lista_no) # Filas no principales
    #print(lista_aceptable2) #Filas principales
    for i in lista_no:
        #print(df[35])
        if df[33][i] != '00' :
            if pd.isna(df[35][i]) == True:
                err.append('vacio, Columna 36, clave_del_sujeto_obligado, registro ' + str(i+1) + ', registro ' + str(df[35][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
    for i in range(len(clave)):
        if pd.isna(clave[i]) == True:
            err.append('vacio, Columna 36, clave_del_sujeto_obligado, registro ' + str(i+1) + ', registro ' + str(df[35][i]) + ': se encuentran vacia o con punto y coma')
    for i in range(len(clave)):
        #print(clave[i])
        if pd.isna(clave[i]) == False:
            if len(clave[i]) > 6:
                err.append("longitud, Columna 36, clave_del_sujeto_obligado, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" La longitud del campo excede lo dispuesto en el DOF")
    for i in range(len(clave)):
        if pd.isna(clave[i]) == False:
            if clave[i][0] != '0':
                err.append("numerico, Columna 36, clave_del_sujeto_obligado, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" La clave no comienza con 0")
    for i in range(len(clave)):
        if pd.isna(clave[i]) == False:
            if '-' in clave[i]:
                err.append("alfanumerico, Columna 36, clave_del_sujeto_obligado, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" No se suprimio el gion intermedio")
    for i in range(len(clave)):
        if pd.isna(clave[i]) == False and len(clave[i])==6:
            if clave[i] not in cat_casfim:
                err.append("catalogo, Columna 36, clave_del_sujeto_obligado, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" No se encuentra en el catalogo")
    return err
#======================Columna 37=================================
#===NOMBRE DEL TITULAR DE LA CUENTA O DE LA PERSONA RELACIONADA===

def is_col37(df):
    lista_aceptable=[]
    for i in range(len(df[37])):
        a=df.iloc[i]
        b=a.isnull().sum()
        #print(b)
        if b in [29,31]:
            lista_aceptable.append(i)
            #err.append("Fila NO aceptable")
        else:
            True
            #err.append("Fila Aceptable")
    clave=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[36]
        clave.append(col)
    ########################## DA: Parte de diferencia ######################
    lista_aceptable2=[]
    lista_no=[]
    for i in range(len(df[40])):
        try:
            if len(df[40][i]) > 5:
                lista_aceptable2.append(i)
        except:
            lista_no.append(i)
    #print(lista_no) # Filas no principales
    #print(lista_aceptable2) #Filas principales
    for i in lista_no:
        if df[33][i] != '00':
            if pd.isna(df[36][i]) == True:
                err.append('vacio, Columna 37, nombre_del_titular_de_la_cuenta, registro ' + str(i+1) + ', registro ' + str(df[11][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
    for i in range(len(clave)):
        if pd.isna(clave[i]) == False:
            if len(clave[i]) > 60:
                err.append("longitud, Columna 37, nombre_del_titular_de_la_cuenta, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" La longitud del campo excede lo dispuesto en el DOF")
# David: No se si esta parte funcione, es mejor seguir mi logica
        
#    #Checando que la Longitud se correcta
#    for i in range(len(df[36])):
#        if len(str(df[36][i]))>60:
#            err.append('Columna 37, fila ' + str(i+1) + ', registro ' + str(df[36][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
#        '''elif pd.isna(df[37][i]) == False:
#            err.append('Columna 37, fila ' + str(i+1) + ', registro ' + str(df[36][i]) + ": La columna 38 del registro contiene xxxx o información alfanumérica pero el campo de la columna 37 tiene un separador ; ")
#        elif pd.isna(df[37][i]) == False and pd.isna(df[38][i]) == False:
#            err.append('Columna 37, fila ' + str(i+1) + ', registro ' + str(df[36][i]) + ": La columna 38 del registro contiene XXXX o información alfanumérica, a su vez la columna 39 contiene información alfanumerica pero el campo de la columna 37 tiene un separador ; ")
#'''
        return err
#======================Columna 38=================================
#====================APELLIDO PATERNO=============================
def is_col38(df):
    lista_aceptable=[]
    for i in range(len(df[38])):
        a=df.iloc[i]
        b=a.isnull().sum()
        if b in [29,31]:
            lista_aceptable.append(i)
            #err.append("Fila NO aceptable")
        else:
            True
            #err.append("Fila Aceptable")
    clave=[] 
    for i in lista_aceptable:
        colums=df.iloc[i]
        col=colums[37]
        clave.append(col)
    #print(clave)
    for i in range(len(clave)):
        if pd.isna(clave[i]) == False:
            if len(clave[i]) > 60:
                err.append("longitud, Columna 38, apellido_paterno, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" La longitud del campo excede lo dispuesto en el DOF")
    for i in range(len(clave)):
        if pd.isna(clave[i]) == True and clave[i]=='XXXX':
            err.append("relacion, Columna 38, apellido_paterno, registro "+ str(lista_aceptable[i]+1) +", registro "+clave[i]+" Este campo no puede estar vacio toda vez que exista informacion en la columna 38 y/o 39")
            break
    for i in range(len(df[37])):
        if len(str(df[37][i]))>60:
            err.append('longitud, Columna 38, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(df[37][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
        elif pd.isna(df[37][i]) == True:
            if pd.isna(df[36][i]) == False and pd.isna(df[38][i]) == False:
                err.append('alfanumerico, Columna 38, apellido_paterno, registro ' + str(i+1) + ', registro ' + str(df[37][i]) + ": El campo cuenta con un separador ; pero la columna 39 y 37 cuentan con campos alfanuméricos ")
        #elif pd.isna(df[37][i]) == False and pd.isna(df[38][i]) == False:
        #    err.append('Columna 38, fila ' + str(i+1) + ', registro ' + str(df[37][i]) + ": La columna 38 del registro contiene XXXX o información alfanumérica, a su vez la columna 39 contiene información alfanumerica pero el campo de la columna 37 tiene un separador ; ")
        return err
#======================Columna 39=================================
#====================APELLIDO MATERNO=============================
def is_col39(df):
    for i in range(len(df[38])):
        if len(str(df[38][i]))>30:
            err.append('longitud, Columna 39, apellido_materno, registro ' + str(i+1) + ', registro ' + str(df[38][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
        elif pd.isna(df[38][i]) == True:
            if pd.isna(df[37][i]) == False:
                err.append('alfanumerico, Columna 39, apellido_materno, registro ' + str(i+1) + ', registro ' + str(df[38][i]) + ": El campo cuenta con un separador ; pero la columna 38 cuenta con campo alfanumérico o xxxx ")
    return err
#======================Columna 40=================================
#====================DESCRIPCIÓN DE LA OPERACIÓN==================
def is_col40(df):
    NAN = df[39].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 40, descripcion_de_la_operacio, registro ' + str(i+1) + ', registro ' + str(df[39][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True
        return err
#======================Columna 41=================================
#====================RAZONES INUSUAL==============================
def is_col41(df):
    NAN = df[40].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('vacio, Columna 41, razones_inusual, registro ' + str(i+1) + ', registro ' + str(df[40][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True
        return err