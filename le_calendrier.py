# -*- coding: utf-8 -*-

import requests
import zipfile
import StringIO
import xlrd
import csv
import os
import glob
import pandas as pd
import html5lib

###############################################################################
# Vacances scolaires et jours feries en France
# Source:
# http://www.lecalendrier.fr/
###############################################################################

path_common = './data'
output_folder = 'lecalendrier'
path = os.path.join(path_common, output_folder)

# verify if output_folder exists
if not os.path.exists(os.path.join(path_common, output_folder)):
    os.makedirs(os.path.join(path_common, output_folder))

# VACANCES SCOLAIRES

years_vacances = range(1991, 2019)

# Avant la rentrée scolaire 2015:
#
# Zone A:
# Seules les villes (et villes voisines) de
# Caen, Clermont-Ferrand, Grenoble, Lyon, Montpellier, Nancy-Metz, Nantes,
# Rennes et Toulouse
# sont concernées par ces dates.
zoneA1 = {'ville': ['Caen', 'Clermont-Ferrand', 'Grenoble',
                    'Lyon', 'Montpellier', 'Nancy-Metz', 'Nantes',
                    'Rennes', 'Toulouse']}
df_zoneA1 = pd.DataFrame(zoneA1)
df_zoneA1['zone'] = 'A1'

# Zone B:
# Seules les villes (et villes voisines) de
# Aix-Marseille, Amiens, Besançon, Dijon, Lille, Limoges, Nice, Orléans-Tours,
# Poitiers, Reims, Rouen et Strasbourg
# sont concernées par ces dates.
zoneB1 = {'ville': ['Aix-Marseille', 'Amiens', 'Besançon', 'Dijon', 'Lille',
                    'Limoges', 'Nice', 'Orléans-Tours', 'Poitiers', 'Reims',
                    'Rouen', 'Strasbourg']}
df_zoneB1 = pd.DataFrame(zoneB1)
df_zoneB1['zone'] = 'B1'

# Zone C:
# Seules les villes (et villes voisines) de
# Bordeaux, Créteil, Paris et Versailles
# sont concernées par ces dates.
zoneC1 = {'ville': ['Bordeaux', 'Créteil', 'Paris', 'Versailles']}
df_zoneC1 = pd.DataFrame(zoneC1)
df_zoneC1['zone'] = 'C1'

# A partir de la rentrée scolaire 2015:
#
# Zone A:
# Seules les villes (et villes voisines) de
# Besançon, Bordeaux, Clermont-Ferrand, Dijon, Grenoble, Limoges, Lyon
# et Poitiers
# sont concernées par ces dates.
zoneA2 = {'ville': ['Besançon', 'Bordeaux', 'Clermont-Ferrand', 'Dijon',
                    'Grenoble', 'Limoges', 'Lyon', 'Poitiers']}
df_zoneA2 = pd.DataFrame(zoneA2)
df_zoneA2['zone'] = 'A2'

# Zone B:
# Seules les villes (et villes voisines) de
# Aix-Marseille, Amiens, Caen, Lille, Nancy-Metz, Nantes, Nice, Orléans-Tours,
# Reims, Rennes, Rouen et Strasbourg
# sont concernées par ces dates.
zoneB2 = {'ville': ['Aix-Marseille', 'Amiens', 'Caen', 'Lille', 'Nancy-Metz',
                    'Nantes', 'Nice', 'Orléans-Tours', 'Reims', 'Rennes',
                    'Rouen', 'Strasbourg']}
df_zoneB2 = pd.DataFrame(zoneB2)
df_zoneB2['zone'] = 'B2'

# Zone C:
# Seules les villes (et villes voisines) de
# Créteil, Montpellier, Paris, Toulouse et Versailles
# sont concernées par ces dates.
zoneC2 = {'ville': ['Créteil', 'Montpellier', 'Paris', 'Toulouse',
                    'Versailles']}
df_zoneC2 = pd.DataFrame(zoneC2)
df_zoneC2['zone'] = 'C2'

df_zones = pd.concat([df_zoneA1, df_zoneB1, df_zoneC1,
                      df_zoneA2, df_zoneB2, df_zoneC2], axis=0)
df_zones.to_csv(os.path.join(path, 'zones.csv'))


url_vacances = 'http://www.lecalendrier.fr/vacances-scolaires-'

df_vacances = pd.DataFrame()
Zone = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2']

for year in years_vacances:
    url = url_vacances + str(year)

    for i in range(0, 3):
        df = pd.read_html(url, match='.+', header=0)[i] \
               .drop([0]) \
               .drop('Nombre de jours', axis=1)
        if year < 2015:
            df['Zone'] = Zone[i]
        else:
            df['Zone'] = Zone[i+3]
        df_vacances = pd.concat([df_vacances, df])
df_vacances.to_csv(os.path.join(path, 'vacances_scolaires.csv'),
                   encoding='utf-8')
df_vacances.reset_index(drop=True, inplace=True)

# JOURS FERIES

url_feries = 'http://www.lecalendrier.fr/jours-feries-'
years_feries = range(1970, 2037)

df_feries = pd.DataFrame()
for year in years_feries:
    url = url_feries + str(year)
    df = pd.read_html(url, match='.+', header=0)[0] \
           .drop('Jours restants', axis=1)
    df_feries = pd.concat([df_feries, df])

df_feries.to_csv(os.path.join(path, 'jours_feries.csv'), encoding='utf-8')
df_feries.reset_index(drop=True, inplace=True)
