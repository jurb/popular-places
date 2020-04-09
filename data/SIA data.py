# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.4
# ---

import pandas as pd
import numpy as np

df_alles = pd.read_csv('SIA_FLAT.csv')

# meldingen met 'test' erin weghalen
df = df_alles[~df_alles['text'].str.contains('test')]
df = df[~df_alles['source'].str.contains('Eigen organisatie')]

df


