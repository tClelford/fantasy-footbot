import os
import pandas as pd
import re
THIS_YEAR="2022-23"
# LAST_YEAR="2021-22"
def ewma_understats(player_name: str, weeks:int)-> float:
    path = f"./data/{THIS_YEAR}/understat"
    for f in os.listdir(path):
        # print(f)
        match = re.match(f"{player_name}_.*.csv", f)
        if not match:
            continue
        # print("!!!")
        df = pd.read_csv(f"{path}/{f}")
        ewma = df.ewm(span=10, min_periods=10)
        print(ewma.var().head())


ewma_understats("Alex_Iwobi", 10)