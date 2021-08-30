#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import datetime
import numpy as np
import pandas as pd
from RIPS_helper import *
from RIPS_content_checker_R import *
from RIPS_content_checker_I import *
import warnings
from act_eco import *
import sqlite3
import flask
from flask import send_file
from flask import request,jsonify, Response,Flask


# In[8]:


warnings.filterwarnings("ignore")


# In[10]:


app = flask.Flask(__name__)
app.config["DEBUG"] = True
@app.route('/inusuales', methods = ['GET'])
def read_txt():

    errors = []

    df = pd.read_csv('inusuales.txt', encoding="ISO-8859-1", sep=";", header=None, dtype=str)
    if df.shape[1] == 1:
        print("Mal uso de separadores de columnas")

    if len(df.columns) is not 41:
        diff = len(df.columns) - 41
        if diff > 0:
            errors.append("Reporte tiene "+str(diff)+" columnas extra")
        elif diff < 0:
            errors.append("Reporte sin "+str(-diff)+" columnas")

    total_col = len(df.columns)

    valid_col = []

    columns = df.columns

    if 0 < total_col:
        valid_col.append(is_col1(df))
    else:
        errors.append('No existe la columna 1')

    if 1 < total_col:
        valid_col.append(is_col2_in(df))
    else:
        errors.append('No existe la columna 2')

    if 2 < total_col:
        valid_col.append(is_col3_in(df))
    else:
        errors.append('No existe la columna 3')

    if 3 < total_col:
        valid_col.append(is_col4(df[columns[3]]))
    else:
        errors.append('No existe la columna 4')

    if 4 < total_col:
        valid_col.append(is_col5(df[columns[4]]))
    else:
        errors.append('No existe la columna 5')

    if 5 < total_col:
        valid_col.append(is_col6i(df))
    else:
        errors.append('No existe la columna 6')

    if 6 < total_col:
        valid_col.append(is_col7i(df))
    else:
        errors.append('No existe la columna 7')

    if 7 < total_col:
        valid_col.append(is_col8i(df))
    else:
        errors.append('No existe la columna 8')

    if 8 < total_col:
        valid_col.append(is_col9(df))
    else:
        errors.append('No existe la columna 9')

    if 9 < total_col:
        valid_col.append(is_col10(df))
    else:
        errors.append('No existe la columna 10')

    if 10 < total_col:
        valid_col.append(is_col11(df))
    else:
        errors.append('No existe la columna 11')

    if 11 < total_col:
        valid_col.append(is_col12(df))
    else:
        errors.append('No existe la columna 12')

    if 12 < total_col:
        valid_col.append(is_col13(df))
    else:
        errors.append('No existe la columna 13')

    # Columna válida solo para reportes inusuales y preocupantes
    if 13 < total_col:
        valid_col.append(is_col14(df))
    else:
        errors.append('No existe la columna 14')

    if 14 < total_col:
        valid_col.append(is_col15(df))
    else:
        errors.append('No existe la columna 15')

    if 15 < total_col:
        valid_col.append(is_col16(df))
    else:
        errors.append('No existe la columna 16')

    if 16 < total_col:
        valid_col.append(is_col17(df))
    else:
        errors.append('No existe la columna 17')

    if 17 < total_col:
        valid_col.append(is_col18(df))
    else:
        errors.append('No existe la columna 18')

    if 18 < total_col:
        valid_col.append(is_col19(df))
    else:
        errors.append('No existe la columna 19')

    if 19 < total_col:
        valid_col.append(is_col20(df))
    else:
        errors.append('No existe la columna 20')

    if 20 < total_col:
        valid_col.append(is_col21(df))
    else:
        errors.append('No existe la columna 21')

    if 21 < total_col:
        valid_col.append(is_col22(df))
    else:
        errors.append('No existe la columna 22')

    if 22 < total_col:
        valid_col.append(is_col23(df))
    else:
        errors.append('No existe la columna 23')

    #RoCpD = is_RoCoD(df[columns[20]], df[columns[21]], df[columns[22]])

    if 23 < total_col:
        valid_col.append(is_col24(df))
    else:
        errors.append('No e0000001xiste la columna 24')

    if 24 < total_col:
        valid_col.append(is_col25(df))
    else:
        errors.append('No existe la columna 25')

    if 25 < total_col:
        valid_col.append(is_col26(df))
    else:
        errors.append('No existe la columna 26')

    if 26 < total_col:
        valid_col.append(is_col27(df))
    else:
        errors.append('No existe la columna 27')

    if 27 < total_col:
        valid_col.append(is_col28(df,dic_act))
    else:
        errors.append('No existe la columna 28')

    if 28 < total_col:
        valid_col.append(is_col29(df)) #29
    else:
        errors.append('No existe la columna 29')

    if 29 < total_col:
        valid_col.append(is_col30(df)) #30
    else:
        errors.append('No existe la columna 30')

    if 30 < total_col:
        valid_col.append(is_col31(df)) #31
    else:
        errors.append('No existe la columna 31')

    if 31 < total_col:
        valid_col.append(is_col32(df)) #32
    else:
        errors.append('No existe la columna 32')

    if 32 < total_col:
        valid_col.append(is_col33(df)) #33
    else:
        errors.append('No existe la columna 33')

    if 33 < total_col:
        valid_col.append(is_col34(df)) #34
    else:
        errors.append('No existe la columna 34')

    if 34 < total_col:
        valid_col.append(is_col35(df)) #35
    else:
        errors.append('No existe la columna 35')

    if 35 < total_col:
        valid_col.append(is_col36(df))    
    else:
        errors.append('No existe la columna 36')

    if 36 < total_col:
        valid_col.append(is_col37(df))
    else:
        errors.append('No existe la columna 37')

    if 37 < total_col:
        valid_col.append(is_col38(df))
    else:
        errors.append('No existe la columna 38')

    if 38 < total_col:
        valid_col.append(is_col39(df))
    else:
        errors.append('No existe la columna 39')

    if 39 < total_col:
        valid_col.append(is_col40(df))
    else:
        errors.append('No existe la columna 40')

    if 40 < total_col:
        valid_col.append(is_col41(df))
    else:
        errors.append('No hay información en la columna 41')

    #errors1=pd.DataFrame(err)
    #reporte = errors1.to_csv("errres.csv")
    #return Response(reporte,mimetype = "text/csv")
    
    reporte_inusuales = pd.DataFrame(err).to_csv("err_in.csv")
    #return Response(reporte_inusuales,mimetype="text/csv",headers={"Content-disposition":"attachment; filename=err_in.csv"})
    return send_file('err_in.csv',
                     mimetype='text/csv',
                     attachment_filename='err_in.csv',
                     as_attachment=True)

app.run()


# In[ ]:




