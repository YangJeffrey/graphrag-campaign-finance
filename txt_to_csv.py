import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')

column_names = [
    'CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM',
    'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE',
    'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT',
    'OTHER_ID', 'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID'
]

input_file = os.path.join(data_dir, 'itcont.txt')
output_file = os.path.join(data_dir, 'itcont.csv')

print("Reading pipe-delimited file...")
df = pd.read_csv(input_file, sep='|', header=None, names=column_names)

print(f"\nSaving to {output_file}...")
df.to_csv(output_file, index=False)
