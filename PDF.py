import tabula
import pandas as pd
import streamlit as st
import openpyxl
from io import BytesIO
import base64
from langdetect import detect
import re


def convert_df(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    writer = pd.ExcelWriter(f'{fime_name_to_excel}.xlsx')
    df_balance.to_excel(writer, sheet_name=name_1, index=False)
    df_income_statement.to_excel(writer, sheet_name=name_2, index=False)
    st.write()

    writer.save()


def download(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement):
    csv = convert_df(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement)
    with open(f'{fime_name_to_excel}.xlsx', "rb") as file:
        st.download_button(
            label="Download data as CSV",
            data=file,
            file_name=f'{fime_name_to_excel}.xlsx',
            mime='text/xlsx',
        )


def to_excel_nitherland():
    s = []
    for i in range(len(dfs)):
        df = pd.DataFrame(dfs[i])
        columns = df.columns
        df = df.dropna(axis='columns', how='all')
        if 'Boekjaar' in columns:
            try:
                if 'Codes' in columns:
                    del df['Codes']
                if 'Toel.' in columns:
                    del df['Toel.']
                s.append(df)
            except:
                pass
        else:
            continue
    s1 = []
    pattern = re.compile('\B\+.-\B')
    for j in range(len(s)):
        df = pd.DataFrame(s[j])
        df = df.fillna('')
        columns = df.columns
        for col in columns:
            df[col] = df[col].apply(lambda x: str(x).replace('.', ''))
            df[col] = df[col].apply(lambda x: str(x).replace('(', ''))
            df[col] = df[col].apply(lambda x: str(x).replace(')', ''))
            val = df[col].str.match(pattern)
            if True in list(val):
                print(df[col])
                del df[col]
            else:
                continue
        s1.append(df)
    list1 = []
    for item in s1:
        for info in item.values:
            list1.append(info)
    df = pd.DataFrame(list1)
    df = df.fillna('')
    a = df.iloc[:, 0].str.contains('TOTAAL VAN DE PASSIVA', regex=False)
    b = df.iloc[:, 0].str.contains('Te bestemmen winst verlies van het boekjaar', regex=False)
    index = a[a == True].index[0]
    index_1 = b[b == True].index[0]
    df_balance = df.iloc[:index + 1]
    df_income_statement = df.iloc[index + 1:index_1 + 1]
    print(download(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement))


def to_excel_france():
    s = []
    for i in range(len(dfs)):
        df = pd.DataFrame(dfs[i])
        columns = df.columns
        df = df.dropna(axis='columns', how='all')
        if 'Exercice' in columns:
            if 'Codes' in columns:
                del df['Codes']
            if 'Ann.' in columns:
                del df['Ann.']
            s.append(df)
        else:
            continue
    s1 = []
    pattern = re.compile('\B\+.-\B')
    for j in range(len(s)):
        df = pd.DataFrame(s[j])
        df = df.fillna('')
        columns = df.columns
        for col in columns:
            df[col] = df[col].apply(lambda x: str(x).replace('.', ''))
            df[col] = df[col].apply(lambda x: str(x).replace('(', ''))
            df[col] = df[col].apply(lambda x: str(x).replace(')', ''))
            val = df[col].str.match(pattern)
            if True in list(val):
                del df[col]
            else:
                continue
        s1.append(df)

    list1 = []
    for item in s1:
        for info in item.values:
            list1.append(info)
    df = pd.DataFrame(list1)
    df = df.fillna('')

    a = df.iloc[:, 0].str.contains('TOTAL DU PASSIF', regex=False)
    b = df.iloc[:, 0].str.contains("Bénéfice Perte de l'exercice à affecter", regex=False)
    index = a[a == True].index[0]
    index_1 = b[b == True].index[0]
    df_balance = df.iloc[:index + 1]
    df_income_statement = df.iloc[index + 1:index_1 + 1]
    print(download(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement))


def to_excel_english():
    s = []
    for i in range(len(dfs)):
        df = pd.DataFrame(dfs[i])
        columns = df.columns
        df = df.dropna(axis='columns', how='all')
        if 'Period' in columns:
            if 'Codes' in columns:
                del df['Codes']
            if 'Discl.' in columns:
                del df['Discl.']
            s.append(df)
        else:
            continue
    s1 = []
    pattern = re.compile('\B\+.-\B')
    for j in range(len(s)):
        df = pd.DataFrame(s[j])
        df = df.fillna('')
        columns = df.columns
        for col in columns:
            df[col] = df[col].apply(lambda x: str(x).replace('.', ''))
            df[col] = df[col].apply(lambda x: str(x).replace('(', ''))
            df[col] = df[col].apply(lambda x: str(x).replace(')', ''))
            val = df[col].str.match(pattern)
            if True in list(val):
                del df[col]
            else:
                continue
        s1.append(df)

    list1 = []
    for item in s1:
        for info in item.values:
            list1.append(info)
    df = pd.DataFrame(list1)
    df = df.fillna('')

    a = df.iloc[:, 0].str.contains('TOTAL ASSETS', regex=False)
    b = df.iloc[:, 0].str.contains("Gain loss of the period available for appropriation", regex=False)
    index = a[a == True].index[0]
    index_1 = b[b == True].index[0]
    df_balance = df.iloc[:index + 1]
    df_income_statement = df.iloc[index + 1:index_1 + 1]
    print(download(fime_name_to_excel, name_1, name_2, df_balance, df_income_statement))


st.title('MVP')
st.subheader("Upload PDF file finansial statment of company")
uploaded_file = st.file_uploader("Choose a file", "pdf")
if uploaded_file is not None:
    process = st.button("Run")
    if process:
        dfs = tabula.read_pdf(uploaded_file, pages=['1-18'], multiple_tables=True, stream=True)
        file_name = uploaded_file.name
        fime_name_to_excel = file_name.split('.')[0]
        name_1 = 'Balance'
        name_2 = 'Income statement'
        text = ''
        for i in dfs:
            for j in i.values:
                j = str(j)
                text += " " + j
        text_detections = detect(text)
        st.write('language - ', text_detections)
        if text_detections == 'nl':
            to_excel_nitherland()
        if text_detections == 'fr':
            to_excel_france()
        if text_detections == 'en':
            to_excel_english()
