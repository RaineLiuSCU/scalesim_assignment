import pandas as pd

df = pd.read_csv("results_b1.csv")

df_calc = df[df['mode'] == 'CALC'].reset_index(drop=True)
df_user= df[df['mode'] == 'USER'].reset_index(drop=True)

new_names_calc = []
new_names_user = []
for column in df.columns:
    if column == "mode":
        continue
    new_name_calc = column + "_CALC"
    new_name_user = column + "_USER"
    new_names_calc.append(new_name_calc)
    new_names_user.append(new_name_user)
    df_calc[new_name_calc] = df_calc[column]
    df_user[new_name_user] = df_user[column]
df_calc = df_calc[new_names_calc]
df_user = df_user[new_names_user]

print(df_calc)
print(df_user)

df_user.to_csv("table_user.csv")
df_calc.to_csv("table_calc.csv")
# df_final = pd.concat([df_calc, df_user],axis=1)

# print(df_final)
# df_final.to_html('table.html')