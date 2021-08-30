import re
import xlrd
import datetime
import pandas as pd
#RFC
from twocaptchaapi import TwoCaptchaApi
import xml.etree.ElementTree as ET
from lxml.html import fromstring
import requests
from configparser import ConfigParser

#=====================================E.H=======================================
#Estas funciones estaban en donde_rips, pero se pasaron aqui para que sea mas eficiente tu lecttura del codigo

#Funcion general para determinar columnas de tipo string
#P. Ej. nombre, apellido, razon social....
def is_string(data):
    #Revisando que la columna no sea numerica
    for d in data:
        if is_number(d) or d == '':
            return False

    return True

#Funcion general para determinar columnas de fecha
def is_true_date(date):
    #Si los elementos no son numeros, eliminar los caracteres '-' y '/'
    #que normalmente acompanan a las fechas
    for i in range(len(date)):
        if not is_number(date[i]):
            date[i] = date[i].replace("-","")
            date[i] = date[i].replace("/","")
            date[i] = date[i].strip()

    #Verificando sea una columna de fecha
    return is_date(date, tipo_rep = 0)

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


def rep_type(tipo_reporte):
    '''
    Función que regresa el tipo de reporte enviado, el output es 1,2 o 3
    '''
    # Necesitamos que la columna 1 sea válida
    if is_col1(tipo_reporte):
        n_rep = [int(x) for x in tipo_rep]
        return min(n_rep)
    else:
        return None


def is_number(numbered_string):
    '''
    Function returns True if the string is made up of digits only
    and returns False if the string as at leaste one non-digit character
    '''
    return not any(not char.isdigit() for char in numbered_string)

def is_date(date, tipo_rep):
    '''
    Determina si es una fecha o no dependiendo del tipo de reporte y la
    estructura de cada elemento de la columna
    '''

    #If it is not a string of digits, return false
    if not is_number(date):
        return False
    # En caso de que se trate de un reporte relevante
    if tipo_rep == 1:
        # debe haber 6 elementos en el str
        if min(date.str.len()) != max(date.str.len()) or (min(date.str.len()) != 6):
            return False # No se cumple con la estructura numérica
        try:
            pd.to_datetime(date, format = '%Y%m')
            return True
        except:
            return False    # hay fallas al convertir el str
    else:
        # debe haber 8 elementos en el str
        if (min(date.str.len()) != max(date.str.len())) or (min(date.str.len()) != 8):
            return False # No se cumple con la estructura numérica
        try:
            pd.to_datetime(date, format = '%Y%m%d')
            return True
        except:
            return False # hay fallas al convertir el str


def open_txt(path):
    with open(path, 'r') as file:
        text = file.read()

    text = text.split(";")
    # eliminamos el último por ser vacío
    ytext = text[:-1]
    return text


def cat2list(datafile, col, sheet_index = 0):
    '''
    Takes an xl file as input and the column number with the desired values
    Returns a list with the values as a string so that it can be copy pasted
    '''

    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(sheet_index)

    lst = []

    for i in range(1,sheet.nrows):

        c_val = sheet.cell_value(i,col)
        if c_val == '':
            c_val = -1

        lst.append(int(c_val))

    return lst

def col_finder(col,num_col,reverse = False):

    col_idx = num_col - 1
    #Revisa desde la columna 1 hasta las 7 (potencialmente)
    if num_col < 4:
        #Revisa si la columna esta en el lugar correspondiente
        if col[col_idx]:
            return col_idx
        #Caso contrario la busca en la vecindad
        else:
            if reverse:
                col = list(reversed(col))
            for i in range(num_col + 3):
                if col[i]:
                    return i
                #Si no se encuentra, regresa -1
                elif i == (num_col + 2):
                    return -1

    #Revisa +/-3 columnas respecto a la columna a verificar
    else:
        #Revisa si la columna esta en el lugar correspondiente
        if col[col_idx]:
            return col_idx
        #Caso contrario la busca en la vecindad
        else:
            if reverse:
                col = list(reversed(col))
            for i in range(col_idx - 3,num_col + 3):
                if col[i]:
                    return i
                #Si no se encuentra, regresa -1
                elif i == (num_col + 2):
                    return -1
#==============================================================================


#========SIRVEN PARA is_col2==============================
def test_obj_str(objeto):
    if type(objeto) != str:
        print('NO ES UN STR')
        return 'NO ES UN STR'

def test_obj_re(objeto, regex):
    result = test_obj_str(objeto)
    if result:
        return result
    is_valid = re.match(regex, objeto)
    if not is_valid:
        return ' NO CUMPLE CON EL FORMATO DOF'

def test_obj_com(objeto, regex):
    result = test_obj_str(objeto)
    if result:
        return result
    is_valid = re.match(regex, objeto)
    if is_valid:
        return ' NO CUMPLE CON EL FORMATO DOF'

#is_col2,
#AAAAMM
def test_v_fecha(objeto):
    return test_obj_re(objeto, '(([2][0][1][5-9])(0[1-9]|1[0-2]))')

#is_col23
#AAAAMMDD
def test_v_nacimiento(objeto):
    return test_obj_re(objeto, '(([1][9][0-9]{2}|[2][0][0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))')
#is_col24
def test_v_dom(objeto):
    return test_obj_re(objeto, "[A-Z0-9Ñ.,:“”/'\s#-]{1,300}$")
#is_col25
def test_v_col(objeto):
    return test_obj_re(objeto, "[A-Z0-9Ñ.,:/'\s#-]{1,40}$")
#is_col26
def test_v_loc(objeto):
    return test_obj_re(objeto, "[0-9]{1,9}$")
#is_col19,20
def test_v_nom(objeto):
    return test_obj_re(objeto, "[XXXX]|[xxxx]")
#=====================================

def mes(col):

    T = []
    #col = col.astype(str)
    for i in range(len(col)):
        T.append(re.findall(r'^[\d]{6}',col[i]))
    col = T

    H = []
    for j in range(len(col)):
        H.append(''.join(col[j]))
    #col = pd.DataFrame(H)

    return col

#=============================================================
#==============Para validar RFC===============================
def parse_html_form(tree):
    '''
    Recibe el contenido de un html y regresa un diccionario con
    los campos del formulario
    '''
    #Inicializando diccionario para forma
    data = {}

    #Extrayendo formulario
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')

    return data

def rfc_validacion(rfc_emisor):
    '''
    Dados un RFC emisor, RFC receptor y el folio fiscal determina
    el estatus del CDFI

    '''

    #print('INGRESAR URL')
    #Url para verificacion de RFC
    RFC_url = 'https://portalsat.plataforma.sat.gob.mx/ConsultaRFC/'

    #Empezando sesion en pagina del SAT
    #print('entrando a página del SAT')
    session = requests.Session()
    html = session.get(RFC_url,headers={'Cache-Control': 'no-cache'})
    #print('extraer página del SAT')
    #Extrayendo el contenildo de la pagina
    tree = fromstring(html.content)
    #print('extraerformulario')
    #Extrayendo formulario
    formulario = parse_html_form(tree)

    formulario['ConsultaForm:rfc'] = rfc_emisor

    resp = session.post(html.url,formulario)

    result = fromstring(resp.content)
    Prer=result.text_content()
    respuesta=re.findall('Resultado.*', Prer)

    return respuesta
#============================================================
