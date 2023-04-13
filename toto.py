from datetime import datetime
import random

date_prod = []
prix = []

for j in range(1, 4):
    for i in range(1, 32):
        date_str = f'{str(i).zfill(2)}/{str(j).zfill(2)}/2023'
        if date_str not in ("29/02/2023", "30/02/2023", "31/02/2023", "31/04/2023", "31/06/2023", "31/09/2023", "31/11/2023"):
            date_prod.append(date_str)
            prix.append(round(random.uniform(1, 400), 2))

