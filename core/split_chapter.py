import pandas as pd
from sqlalchemy import create_engine

MS_INFO = {
    'host': '192.168.152.133',
    'port': 1433,
    'user': 'sa',
    'password': '5cHC*J6x2B',
    'database': 'MacsDB'
}

engine = create_engine(
    f"mssql+pymssql://{MS_INFO['user']}:{MS_INFO['password']}@{MS_INFO['host']}:{MS_INFO['port']}/{MS_INFO['database']}"
)

df = pd.read_sql(
    sql="select * from MacsDB.Novel.tab_novel",
    con=engine
)

for _, row in df.iterrows():
    if len(row['novel_context']) < 10:
        continue

    for m in ['第一部', '第二部', '第三部', '第四部', '第五部', '第六部', '番外']:
        if m in row['novel_name']:
            print(f"../txt/{m}/{row['novel_name'].replace(' ', '')}.txt")
            with open(f"../txt/{m}/{row['novel_name'].replace(' ', '')}.txt", "w", encoding='utf-8') as f:
                f.write(row['novel_context'])
