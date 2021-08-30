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


##Dicionarios
from act_eco import *
from SCIAN2008 import *
cat_loc = cat2list('Catalogos/LocalidadesRIPS.xlsx',2)
pais = pd.read_csv('Catalogos/Paises.txt', encoding="ISO-8859-1", sep=";", header=None, dtype=str)
cat_mon = open_txt('Catalogos/cat_mon')
cat_casfim = open_txt('Catalogos/casfim_claves.txt')
cat_suc = open_txt("Catalogos/donde_suc.txt")
#cat_suc_0 = open_txt("Catalogos/donde_suc_0.txt")
#Cat_suc = open_txt('/home/rvelez/Projects/RIPS/Catalogos/sucursales_donde_original.txt')
# El catalogo de paises me sirve en lista.
cat_nac = list(pais[1])


err = []


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


#==========================E.Heathcliff et Gestell==================================
#==========================VALIDACION DE CONTENIDO DE COLUMNAS======================

#======================Columna 1=================================
#======================TIPO DE REPORTE===========================
def is_col1(df):
    #err = []
    #Revisando si hay registros vacios
    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 1, fila ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[i])>1:
            err.append('Columna 1, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La longitud del campo de la columna excede lo dispuesto en el DOF ")

    #Chechando tipo de reporte
    print('¿Qué tipo de reporte es')
    rep = df[0][0]
    if rep == '1':
        print("Relevante")
    elif rep == '2':
        print("Inusual")

    for i in range(len(df[0])):
        if df[0][i] == rep:
                True
        else:
            err.append('Columna 1, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La informacion  de la columna  no corresponde al reporte correspondiente o no corresponde a un reporte.")
    return err
#======================Columna 2 RELEVANTES======================
#======================Perdiodo del reporte======================
def is_col2(df):
    #err = []
    c_2 = df[1]
    c_13 = df[12]
    NAN = c_2.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 2, fila ' + str(i+1) + ', registro ' + str(df[i]) + 'El registro se encuentra vacio o tiene punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    c_2 = c_2.fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(c_2)):
        if len(c_2[i])>6:
            err.append('Columna 2, fila ' + str(i+1) + ', registro ' + str(c_2[i]) + ": La longitud del campo de no mide seis caracteres, la longuitud del campo es menor a seis o excede lo dispuesto en el DOF ")


    for j in range(len(c_2)):
        #prueba=test_v_fecha(df[j])
        #print(df[j])
        if re.match('([2][0][1][5-9])(0[1-9]|1[0-2])((0[1-9]|1[0-9]|2[0-9]|3[0-1]))', c_2[j]):
            err.append('Columna 2, fila ' + str(i+1) + ', registro ' + str(c_2[i]) + ": La fecha no es correcta, la fila no es válida")
        elif not re.match('([2][0][1][5-9])(0[1-9]|1[0-2])',c_2[j]):
            err.append('Columna 2, fila ' + str(i+1) + ', registro ' + str(c_2[i]) +  ": La fecha no es correcta, la fila no es válida pues tiene informacion alfabetica y/o los numeros de año son inferiores a 2014 y/o los numeros del mes son distintos del uno al doce y/o no cumple con el formato AAAAMM")
        else:
            True

    return err

#======================Columna 3=================================
#======================FOLIO RELEVANTES==========================
def is_col3(folio):

    #err = []

    NAN = folio.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 3, fila ' + str(i+1) + ', registro ' + str(folio[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    folio = folio.fillna('000000')

    #Checando que la Longitud se correcta
    for i in range(len(folio)):
        if len(folio[i])>6:
            err.append('Columna 3, fila ' + str(i+1) + ', registro ' + str(folio[i]) +": La longitud del campo excede lo dispuesto en el DOF ")

    if folio[0] != '000001':
            err.append('Columna 3, fila ' + str(i+1) + ', registro ' + str(folio[0]) + ': El primer registro no contiene en la columna 3 0000001')


    h = folio
    h=pd.DataFrame(h)
    h=h.astype(int)
    #for i in range(len(h)-1):
        #fol_dif = h[2][i+1] - h[2][i]
        #if fol_dif != 1:

    for j in range(len(h)-1):
        if h[2][j+1]-h[2][j] == 1:
            True
        else:
            err.append('Columna 3, fila ' + str(i+1) + ', registro ' + str(h[2][j+1]) + ": El campo no continua el incremento de la serie numérica en la columna de acuerdo a lo que pide el formato ")
        #else:
        #    True
        #else:
        #    True
    return err

#======================Columna 4=================================
#======================ORGANO SUPERVISOR=========================
def is_col4(df):
    #err = []

    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 4, fila ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('000000')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[i])>6:
            err.append('Columna 4, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")


    for i in range(len(df)):
        if df[i] in cat_casfim:
            True
        else:
            err.append('Columna 4, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no comienza con un cero y/o no corresponde al catalogo  y/o no se suprimio el guion intermedio de la clave " )
    return err


#======================Columna 5=================================
#======================ORGANO SUPERVISOR=========================
def is_col5(df):

    #err = []
    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 5, fila ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('000000')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[i])>6:
            err.append('Columna 5, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La longitud del campo es mayor a seis digitos ")

    #Revisando que la columna sea numercia, considerando la posibilidad
    #de la presencia del caraceter '-'
    for i in range(len(df)):
        if df[i] in cat_casfim:
            True
        else:
            err.append('Columna 5, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": La clave no esta en el catalogo, no tiene los ceros a la izquierda adecuados, o no se suprimio el guion intermedio de la clave " )
    return err

#======================Columna 6=================================
#======================LOCALIDAD=================================
def is_col6(df):
    #err = []

    NAN = df[5].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 6, fila ' + str(i+1) + ', registro ' + str(df[5][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df[5] = df[5].fillna('00000000')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[5][i])>8:
            err.append('Columna 6, fila ' + str(i+1) + ', registro ' + str(df[5][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df[5])):
        if int(df[5][i]) in cat_loc:
            True
        elif int(df[5][i]) in cat_suc:
            True
        else:
            err.append('Columna 6, fila ' + str(i+1) + ', registro ' + str(df[5][i]) + ": La clave no corresponde al catalogo localidad o sucursales " )

    return err

#======================Columna 7=================================
#======================SUCURSALES================================
#======================PERSONALIZABLE============================
def is_col7(df):
    #err = []

    NAN = df[6].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 7, fila ' + str(i+1) + ', registro ' + str(df[6][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df[6] = df[6].fillna('000')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[6][i])>8:
            err.append('Columna 7, fila ' + str(i+1) + ', registro ' + str(df[6][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df)):
        if df[6][i] in cat_suc:
            True
        #elif int(df[i]) in cat_suc_0:
        #    True
        else:
            err.append('Columna 7, fila ' + str(i+1) + ', registro ' + str(df[6][i]) + ": El campo no contiene ninguna de las claves de sucursal entregadas por el cliente o el numero ceros " )

    return err

#======================Columna 8=================================
#======================TIPO DE OPERACION=========================
def is_col8(df):
    #err = []

    NAN = df[7].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 8, fila ' + str(i+1) + ', registro ' + str(df[7][i]) + ': El registro se encuentra vacio o ocn punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df[7] = df[7].fillna('00')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[7][i])>2:
            err.append('Columna 8, fila ' + str(i+1) + ', registro ' + str(df[7][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    cat_op = ['01', '02', '03', '04', '05', '06', '07', '08', '09',
                '10', '11', '12', '13','14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                '30', '31', '32', '33', '34', '35', '36']

    for i in range(len(df)):
        if df[7][i] in cat_op:
            True
        else:
            err.append('Columna 8, fila ' + str(i+1) + ', registro ' + str(df[7][i]) + ": El tipo de operación no corresponde al catalogo " )

    return err

#======================Columna 9=================================
#======================INSTRUMENTO MONETARIO=====================
def is_col9(df):
    #err = []
    NAN = df[8].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[8] = df[8].fillna('00')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[8][i])>2:
            err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    cat_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    for i in range(len(df)):
        if df[8][i] in cat_list:
            True
        else:
            err.append('Columna 9, fila ' + str(i+1) + ', registro ' + str(df[8][i]) + ": El tipo de operación no corresponde al catalogo  " )

    return err


#======================Columna 10=================================
#======================NUMERO DE CUENTA===========================
def is_col10(df):
    #err = []
    NAN = df[9].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 10, fila ' + str(i+1) + ', registro ' + str(df[9][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df[9] = df[9].fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(df[9])):
        if len(df[9][i])>16:
            err.append('Columna 10, fila ' + str(i+1) + ', registro ' + str(df[9][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")


    for j in range(len(df[9])):
        #prueba=test_v_fecha(df[j])[columns[27]]
        #print(df[j])
        if len(df[9][j]) == 1:
            err.append('Columna 10, fila ' + str(j+1) + ', registro ' + str(df[9][j]) + ": La longitud del campo contiene un solo carácter numérico diferente a cero")
        elif re.match('[A-Za-z\d]{17}', df[9][j]):
            err.append('Columna 10, fila ' + str(j+1) + ', registro ' + str(df[9][j]) +" : La longitud del campo  excede lo dispuesto en el DOF, la fila no es válida")
        else:
            True

    return err

#======================Columna 11=================================
#======================MONTO======================================
def is_col11(df):
    #err = []

    mon = df[10]
    ins = df[8]

    NAN_m = mon.isna()
    for i in range(len(NAN_m)):
        if NAN_m[i] == True:
            err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(mon[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True

    NAN_i = ins.isna()
    for i in range(len(NAN_i)):
        if NAN_i[i] == True:
            err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(ins[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    mon = mon.fillna('0')
    ins = ins.fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(ins)):
        if len(ins[i])>2:
            err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(ins[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    #Checando que la Longitud se correcta
    for i in range(len(mon)):
        if len(mon[i])>17:
            err.append('Columna 11, fila ' + str(i+1) + ', registro ' + str(mon[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for j in range(len(ins)):
        if ins[j] == '5':
            if float(mon[j]) % 1 == 0:
                True
            else:
                err.append('Columna 11, fila ' + str(j+1) + ', registro ' + str(mon[j]) + ": El registro es Oro, plata y platino amonedado no se indicaron con un numero de unidades del metal en cantidades enteras, la fila no es válida")
        elif re.match('[A-Za-z]{1,}', mon[j]):
            err.append('Columna 11, fila ' + str(j+1) + ', registro ' + str(mon[j]) + ": El registro contiene valores alfabeticos, la fila no es válida")
        else:
            True

    return err
#======================Columna 12=================================
#======================CATALOGO MONEDA============================
def is_col12(df):
    #err = []
    NAN = df[11].isna()
    for i in range(len(NAN)):
        #    True
        if NAN[i] == True:
            err.append('Columna 12, fila ' + str(i+1) + ', registro ' + str(df[11][i]) + ': El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df[11] = df[11].fillna('000')

    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[11][i])>3:
            err.append('Columna 12, fila ' + str(i+1) + ', registro ' + str(df[11][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df)):
        if df[11][i] in cat_mon:
            True
        else:
        #    True
            err.append('Columna 12, fila ' + str(i+1) + ', registro ' + str(df[11][i]) + ": La clave no corresponde al catalogo " )

    return err


#======================Columna 13=================================
#======================FECHA DE LA OPERACION======================
def is_col13(df):
    #err = []
    NAN = df[12].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 13, fila ' + str(i+1) + ', registro ' + str(df[12][i]) + ': El registro se encuentra vacio, y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[12] = df[12].fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(df[12])):
        if len((df[12][i]))>8:
            err.append('Columna 13, fila ' + str(i+1) + ', registro ' + str(df[12][i]) + ": La longitud del campo no es valida pues hay informacion alfabetica en el campo y/o los numeros de año son inferiores a 2014 y/o los numeros de mes son distintos de los numeros uno al doce y/o los numeros de dia son distintos del uno al treinta y uno ")

    for j in range(len(df[12])):
        #prueba=test_v_fecha(df[j])
        #print(df[j])
        if not re.match('([2][0][1][5-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[01])',df[12][j]):
            err.append('Columna 13, fila ' + str(j+1) + ', registro ' + str(df[12][j]) + ": La fecha no es valida pues hay informacion alfabetica en el campo y/o los numeros de año son inferiores a 2014 y/o los numeros de mes son distintos de los numeros uno al doce y/o los numeros de dia son distintos del uno al treinta y uno")
        else:
            True

    return err
#======================Columna 14================================
#======================RELEVANTES DEBE SER VACIA=================
def is_col14(df):
    #err = []
    NAN = df[13].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            True
        else:
            err.append('Columna 14, fila ' + str(i+1) + ', registro ' + str(df[13][i]) + ' La columna no se encuentra vacía y contiene caracteres numéricos o alfabéticos ')

    return err
#======================Columna 15=================================
#======================CATALOGO PAIS==============================
# B
def is_col15(df):
    #err = []

    NAN = df[14].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 15, fila ' + str(i+1) + ', registro ' + str(df[14][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    df = df.fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(df[14])):
        if len(df[14][i])>2:
            err.append('Columna 15, fila ' + str(i+1) + ', registro ' + str(df[14][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df)):
        if (df[14][i]) in cat_nac:
            True
        elif (df[14][i]) == '0':
            True
        #elif int(df[i]) in cat_suc_0:
        #    True
        else:
            err.append('Columna 15, fila ' + str(i+1) + ', registro ' + str(df[14][i]) + ": El campo no contiene una clave encontrada en el catalogo o un cero " )

    return err

#======================Columna 16=================================
#======================TIPO DE PERSONA============================
def is_col16(df):
    err = []
    per = df[15]
    NAN = per.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 16, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True

    #Convierto los NaN a ceros para que lo pueda leer
    per = per.fillna('0')

    #Checando que la Longitud se correcta
    for i in range(len(per)):
        if len(per[i])>1:
            err.append('Columna 16, fila ' + str(i+1) + ', registro ' + str(per[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(per)):
        if per[i] == '1':
            True
        elif per[i] == '2':
            True
        else:
            err.append('Columna 16, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El campo no se utilizaron las claves establecidas por el formato ')

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
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(razon[i]) == True:
                True
            else:
                err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro debe ir vacio, pues es una persona Fisica ')
        elif per[i] == '2':
            if pd.isna(razon[i]) == False:
                if pd.isna(curp[i]) == True:
                    True
                else:
                    err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro cuenta con caracteres alfanumérico pero la columna 22 ' + str(curp[i]) + ' cuenta con caracteres alfanuméricos indicando en el registro a una persona física y no una moral ')
            elif pd.isna(razon[i]) == False:
                if pd.isna(nombre[i]) == False:
                    True
            elif pd.isna(razon[i]) == False:
                if ((pd.isna(paterno[i]) == True) and (pd.isna(materno[i]) == True) ):
                    True
                else:
                    err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(razon[i]) + ': El campo cuenta con caracteres alfanumérico y las columnas 19 y 20 del registrocuentan con caracteres alfanuméricos o XXXX, indicando una persona física y no una moral')
            else:
                err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(razon[i]) + ': El registro no debe ir vacio, pues es una persona Moral ')
        else:
            err.append('Columna 17, fila ' + str(i+1) + ', registro ' + str(per[i]) +': El registro no es una persona Fisica o Moral')

    return err


#======================Columna 18=================================
#======================NOMBRE===============================
def is_col18(df):

    #err = []
    per = df[15]#col16
    razon = df[16]#col17
    nombre = df[17]#col18
    paterno = df[18]#col19
    materno = df[19]#col20

    for i in range(len(per)):
        if per[i] == '1':
            if len(str(nombre[i]))>60:
                err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(nombre[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
            elif pd.isna(nombre[i]) == False:
                True
            elif pd.isna(nombre[i]) == False:
                if pd.isna(razon[i]) == False:
                    err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(razon[i]) + ': El campo debe ir vacio pues es una persona fisica')
            else:
                err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(nombre[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')
        elif per[i] == '2':
            if pd.isna(nombre[i]) == True:
                True
            else:
                err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(nombre[i]) + ': El campo  es incorrecto pues las columnas 19 y 20 contienen caracteres alfanuméricos y el campo de la columna esta vacio ')
        else:
            err.append('Columna 18, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')

    return err

#======================Columna 19=================================
#======================APELLIDO PATERNO===========================
def is_col19(df):

    #err = []
    nac = df[14] #col15
    per = df[15]#col16
    nombre = df[17]#col18
    paterno = df[18]#col19
    materno = df[19]#col20
    rfc = df[20] #col21
    curp = df[21] #col22

    for i in range(len(per)):
        if per[i] == '1':
            if nac[i] == 'MX':
                if pd.isna(paterno[i]) == True:
                    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')
                    paterno = paterno.fillna('0')
                    if len(paterno[i])>30:
                        err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                elif pd.isna(paterno[i]) == False:
                    if pd.isna(materno[i]) == True:
                        err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El campo de la columna esta vacio pero la columna 20 contiene caracteres alfanuméricos ')
                    #elif pd.isna(curp[i]) == True:
                    #    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
            elif nac[i] != 'MX':
                if (pd.isna(df[18][i]) == True ):
                    if pd.isna(df[21][i]) == False:
                        if not re.match('[NA]|[NAN]',df[21][i]) :
                            err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')

        elif per[i] == '2':
            if pd.isna(df[18][i]) == False:
                err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(df[18][i]) + ': El registro debe ir vacio, pues es una persona Moral ')
            elif pd.isna(df[19][i]) == False:
                if pd.isna(curp[i]) == True:
                    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(df[19][i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
        else:
            err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')

    return err

#======================Columna 20=================================
#======================APELLIDO MATERNO===========================
def is_col20(df):

    err = []
    nac = df[14] #col15
    per = df[15]#col16
    nombre = df[17]#col18
    paterno = df[18]#col19
    materno = df[19]#col20
    rfc = df[20] #col21
    curp = df[21] #col22

    for i in range(len(per)):
        if per[i] == '1':
            if nac[i] == 'MX':
                if pd.isna(materno[i]) == True:
                    err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')
                    paterno = paterno.fillna('0')
                    if len(paterno[i])>30:
                        err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                elif pd.isna(materno[i]) == False:
                    if pd.isna(paterno[i]) == True:
                        err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ': El campo de la columna esta vacio pero la columna 19 contiene caracteres alfanuméricos ')
                    #elif pd.isna(curp[i]) == True:
                    #    err.append('Columna 19, fila ' + str(i+1) + ', registro ' + str(paterno[i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
            elif nac[i] != 'MX':
                if (pd.isna(materno[i]) == True ):
                    if pd.isna(curp[i]) == False:
                        if not re.match('[NA]|[NAN]',curp[i]) :
                            err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ': El registro no debe ir vacio, pues es una persona Fisica ')

        elif per[i] == '2':
            if pd.isna(paterno[i]) == False:
                err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ': El registro debe ir vacio, pues es una persona Moral ')
            elif pd.isna(materno[i]) == False:
                if pd.isna(curp[i]) == True:
                    err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(materno[i]) + ': El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos o XXXX ')
        else:
            err.append('Columna 20, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')

    return err



#======================Columna 21=================================
#======================RFC========================================
def is_col21(df):

    #err = []
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
                err.append( 'Columna 21, fila ' + str(i+1) + ', registro ' + str(df[20][i]) + ': El registro de las columnas 22 y 23 están vacias al igual que la columna 21 ')

        #Personas Morales, deben tener al menos una de dos
        elif df[15][i] == '2':
            if ( (pd.isna(df[20][i]) == False) and (pd.isna(df[22][i]) == False) ):
                True
            elif ( (pd.isna(df[20][i]) == False)  ):
                True
            elif ( (pd.isna(df[22][i]) == False)  ):
                True
            elif ( (pd.isna(df[20][i]) == True) and (pd.isna(df[22][i]) == True) ):
                err.append( 'Columna 21, fila ' + str(i+1) + ', registro ' + str(df[20][i]) + ': El registro de la columna 23 está vacia al igual que la columna 21 ')

    for j in range(len(df[20])):
        df[20] = df[20].fillna('0')
        if not re.match('([A-Z&]{3,4}[\d]{6}[\s]?(?:[A-Z\d]{3})?)|0$',df[20][j]):
            """rfc_valid = [rfc_validacion(list(df[20])) for i in range(len(df[20]))]
            #print("RFC")
            for i in range(len(rfc_valid)):
                if rfc_valid[i][1] == 'Resultado: Clave de RFC inválida':
                    for j in rfc_valid[i]:
                        #err.append(str(rfc_valid[i][1])+' '+l[i])
                        err.append( 'Columna 21, fila ' + str([i+1 for i in range(len(df[20]))]) + ', registro ' + str([df[20][i] for i in range(len(df[20]))]) + rfc_valid[i][1])
            print("RFC Leido")"""
            err.append( 'Columna 21, fila ' + str(i+1) + ', registro ' + str(df[20][i]) + ": El RFC no debe de utilizar guion , espacio o cualquier otro tipo de carácter que no forme parte de el.")
        else:
            True

    return err

#======================Columna 22=================================
#======================CURP=======================================


def is_col22(df):

    #err = []
    per = df[15]
    rfc = df[20]#Col21
    curp = df[21]#Col22
    date = df[22]#Col23
    #Reglas para el CURP
    for i in range(len(per)):
        if per[i] == '1':
            if pd.isna(curp[i]) == False:
                curp = curp.fillna('0')
                if len(curp[i])>18:
                    err.append('Columna 22, fila ' + str(i+1) + ', registro ' + str(curp[i]) + ": La longitud del campo excede lo dispuesto en el DOF ")
                    if not re.match('[A-Z]{4}[\d]{6}[A-Z]{6}[\d]{2}',curp[i]):
                        err.append('Columna 22, fila ' + str(i+1) + ', registro ' + str(curp[i]) + ": El CURP no se debe de utilizar guion , espacio o cualquier otro tipo de carácter que no forme parte de el ")
            elif pd.isna(curp[i]) == False:
                if  ( (pd.isna(rfc[i]) == False) and (pd.isna(date[i]) == False) ):
                    True
                elif pd.isna(rfc[i]) == False:
                    True
                elif pd.isna(date[i]) == False:
                    True
                elif ( (pd.isna(rfc[i]) == True) and (pd.isna(date[i]) == True) ):
                    err.append('Columna 22, fila ' + str(i+1) + ', registro ' + str(curp[i]) +': El campo de la col 22 se encuentra vacio al igual que la columna 21 y 23' )
            else:
                True

        elif per[i] == '2':
            if pd.isna(curp[i]) == True:
                True
                if pd.isna(rfc[i]) ==False:
                    True
                else:
                    err.append('Columna 22, fila ' + str(i+1) + ', registro ' + str(curp[i]) + ': El registro debe ir vacio, pues es una persona Moral ')
        else:
            err.append('Columna 22, fila ' + str(i+1) + ', registro ' + str(per[i]) + ': El registro no es una persona Fisica o Moral')

    return err


#======================Columna 23=================================
#=========FECHA DE NACIMIENTO O CONSTITUCIÓN======================
def is_col23(df):

    #err = []

    NAN = df[22].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 23, fila ' + str(i+1) + ', registro ' + str(df[22][i]) + ': El registro se encuentra vacio, y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[22] = df[22].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df[22])):
        if len(df[22][i])>8:
            err.append('Columna 23, fila ' + str(i+1) + ', registro ' + str(df[22][i]) +": La longitud del campo excede lo dispuesto en el DOF ")


    for j in range(len(df[22])):
        prueba=test_v_nacimiento(df[22][j])
        #print(df[j])
        if prueba:
            err.append('Columna 23, fila ' + str(i+1) + ', registro ' + str(df[22][i]) + ": La fecha no es correcta la fila no es válida")
        else:
            True
        #    return is_date(df[1], is_col1)

    return err

#======================Columna 24=================================
#======================DOMICILIO==================================
def is_col24(df):

    #err = []
    NAN = df[23].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 24, fila ' + str(i+1) + ', registro ' + str(df[23][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[23] = df[23].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df[23])):
        if len(df[23][i])>60:
            err.append('Columna 24, fila ' + str(i+1) + ', registro ' + str(df[23][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df)):
        if not re.match("[A-Z0-9Ñ.,:“”/'\s#-]{1,300}",df[23][i]):
            err.append('Columna 24, fila ' + str(i+1) + ', registro ' + str(df[23][i]) + ": El domicilio no es correcto La fila no es válida")
        else:
            True
        #    return is_date(df[1], is_col1)

    return err
#======================Columna 25=================================
#======================COLONIA====================================
def is_col25(df):

    #err = []
    NAN = df[24].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 25, fila ' + str(i+1) + ', registro ' + str(df[24][i]) + ': El registro se encuentra vacio o con punto y coma, y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[24] = df[24].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[24][i])>30:
            err.append('Columna 25, fila ' + str(i+1) + ', registro ' + str(df[24][i]) +": La longitud del campo excede lo dispuesto en el DOF ")

    for j in range(len(df[24])):
        if pd.isna(df[24][j]) == True:
            err.append('Columna 25, fila ' + str(i+1) + ', registro ' + str(df[24][i]) +": La colonia no es correcta La fila no es válida")
        else:
            True

    return err

#======================Columna 26=================================
#======================LOCALIDAD==================================
def is_col26(df):

    #err = []
    NAN = df[25].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 26, fila ' + str(i+1) + ', registro ' + str(df[25][i]) + ': El registro se encuentra vacio, y es obligatorio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[25] = df[25].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df[25])):
        if len(df[25][i])>8:
            err.append('Columna 26, fila ' + str(i+1) + ', registro ' + str(df[25][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for j in range(len(df)):
        prueba=test_v_loc(df[25][j])
        if prueba:
            err.append('Columna 26, fila ' + str(i+1) + ', registro ' + str(df[25][i]) + ": La localidad no es correcta, la fila no es válida")
        else:
            True

    return err

#======================Columna 27=================================
#======================TELEFONO==================================
def is_col27(df):
    #err = []
    '''NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ': El registro se encuentra vacio ')
        else:
            True'''
    #Convierto los NaN a ceros para que lo pueda leer
    df[26] = df[26].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[26][i])>40:
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[26][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    #is_col_null(df)27
    #Convierto los NaN a ceros para que lo pueda leer
    df[26] = df[26].fillna('0')
    '''for j in range(len(df)):
        if re.match('1[2-9]{1,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[0]{5,}',df[j]):
            err.append(" El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[1]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[2]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[3]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[4]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[5]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[6]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[7]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[8]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[9]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        elif re.match('[0]{5,}',df[j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[i]) + ": El telefono se encuentra llenado con numeros aleatorios")
        else:
            True'''


    for j in range(len(df[26])):
        if not re.match('(([\d]{10,12})$|([CELULAR\s0-9\s/FIJO]{1,}))',df[26][j]):
            err.append('Columna 27, fila ' + str(i+1) + ', registro ' + str(df[26][i]) + ": El telefono no es válido")
        else:
            True

    return err
#======================Columna 28=================================
#======================ACTIVIDAD==================================
def is_col28(df,act_eco):
    #err = []
    NAN = df[27].isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            err.append('Columna 28, fila ' + str(i+1) + ', registro ' + str(df[27][i]) + ': El registro se encuentra vacio ')
        else:
            True
    #Convierto los NaN a ceros para que lo pueda leer
    df[27] = df[27].fillna('0')
    #Checando que la Longitud se correcta
    for i in range(len(df)):
        if len(df[27][i])>7:
            err.append('Columna 28, fila ' + str(i+1) + ', registro ' + str(df[27][i]) + ": La longitud del campo excede lo dispuesto en el DOF ")

    for i in range(len(df)):
        if df[27][i] in act_eco:
            True
        else:
            err.append('Columna 28, fila ' + str(i+1) + ', registro ' + str(df[27][i]) + ": la clave  no es un tipo de operacion o no tine los ceros a la izquierda adecuados" )

    return err

#============================E.H=======================================
#===========LAS COLUMNAS SIGUIENTES DEBEN DE ESTAR VACIAS==============
#==========================Para relevantes=============================

#======================Columnas 29-41==============================
#======================VACIO=======================================
def is_col_vide(df):
    #err = []
    NAN = df.isna()
    for i in range(len(NAN)):
        if NAN[i] == True:
            return True
        else:
            err.append('El registro ' + str(i+1) + ' no se encuentra vacio y contiene caracteres numéricos o alfabéticos ')
    return err

#============================ END =====================================
#========================== MrR E.H. ==================================
