#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:04:39 2020

@author: jonathan
"""


from jinja2 import FileSystemLoader, Environment
from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
engine = create_engine('mysql+pymysql://nouveau_utilisateur:mot_de_passe@localhost:3306/netflix')

netflix = "/home/jonathan/netflix/template"
fichier = "rapport.jinja"

templateLoader = FileSystemLoader(searchpath=netflix)
templateEnv=Environment(loader = templateLoader)
template = templateEnv.get_template(fichier)

SQL_Query =pd.read_sql_query("select co_name ,count(`cast`.cast_name) as actor from country "  
"join catalogue_country on country.co_id = catalogue_country.co_id "
"join catalogue on catalogue.ca_id = catalogue_country.ca_id "
"join catalogue_cast on catalogue_cast.ca_id = catalogue.ca_id "
"join `cast` on `cast`.cast_id = catalogue_cast.cast_id "
"group by co_name order by actor     desc limit 10 ;",engine)
print(SQL_Query)

sns.catplot(
        data = SQL_Query,kind ='bar',
        x = 'actor',y = 'co_name'
    )
plt.savefig("/home/jonathan/netflix/template/nbr_acteur_pays.png")
img_path = "/home/jonathan/netflix/template/nbr_acteur_pays.png"

data ={
       'country': SQL_Query,
       'img src': img_path
       }



outputText = template.render(data)
html_file = open('/home/jonathan/netflix/index.html','w')
html_file.write(outputText)
html_file.close()