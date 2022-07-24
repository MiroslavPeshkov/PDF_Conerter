import tabula
import pandas as pd
pd.set_option('max_rows', None)
import streamlit as st
import openpyxl

st.title('MVP')
st.subheader("Upload PDF file finansial statment of company")
uploaded_file = st.file_uploader("Choose a file", "pdf")

if uploaded_file is not None:
    process = st.button("Run")
    st.write(process)
    if process:
        dfs = tabula.read_pdf(uploaded_file, pages = ['6-10'], multiple_tables= True)

        file_name = uploaded_file.name
        fime_name_to_excel = file_name.split('.')[0]

        name_1 = 'BILAN APRÈS RÉPARTITION'
        name_2 = 'COMPTE DE RÉSULTATS'
        name_3 = 'AFFECTATIONS ET PRÉLÈVEMENTS'

        df_1 = dfs[1]
        columns_1 = df_1.columns
        del df_1[f'{columns_1[1]}']
        df_1 = df_1.rename(columns={'Unnamed: 0': f'{name_1}'})
        df_1 = df_1.fillna('')
        df_1[f'{columns_1[-2]}'] = df_1[f'{columns_1[-2]}'].apply(lambda x: str(x).replace('.', ''))
        df_1[f'{columns_1[-1]}'] = df_1[f'{columns_1[-1]}'].apply(lambda x: str(x).replace('.', ''))

        df_2 = dfs[3]
        columns_2 = df_2.columns
        del df_2[f'{columns_2[1]}']
        del df_2[f'{columns_2[2]}']
        df_2 = df_2.rename(columns={'Unnamed: 0': f'{name_1}'})
        df_2 = df_2.fillna('')
        df_2[f'{columns_2[-2]}'] = df_2[f'{columns_2[-2]}'].apply(lambda x: str(x).replace('.', ''))
        df_2[f'{columns_2[-1]}'] = df_2[f'{columns_2[-1]}'].apply(lambda x: str(x).replace('.', ''))

        df_1_2 = pd.concat([df_1, df_2])

        df_3 = dfs[5]
        columns_3 = df_3.columns
        del df_3[f'{columns_3[1]}']
        df_3 = df_3.rename(columns={'Unnamed: 0': f'{name_2}'})
        df_3 = df_3.fillna('')
        df_3[f'{columns_3[-2]}'] = df_3[f'{columns_3[-2]}'].apply(lambda x: str(x).replace('.', ''))
        df_3[f'{columns_3[-1]}'] = df_3[f'{columns_3[-1]}'].apply(lambda x: str(x).replace('.', ''))

        df_4 = dfs[7]
        columns_4 = df_4.columns
        del df_4[f'{columns_4[1]}']
        df_4 = df_4.rename(columns={'Unnamed: 0': f'{name_3}'})
        df_4 = df_4.fillna('')
        df_4[f'{columns_4[-2]}'] = df_4[f'{columns_4[-2]}'].apply(lambda x: str(x).replace('.', ''))
        df_4[f'{columns_4[-1]}'] = df_4[f'{columns_4[-1]}'].apply(lambda x: str(x).replace('.', ''))


        with pd.ExcelWriter(f'{fime_name_to_excel}.xlsx') as writer:
            df_1_2.to_excel(writer, sheet_name=name_1,  index = False)
            df_3.to_excel(writer, sheet_name=name_2,  index = False)
            df_4.to_excel(writer, sheet_name=name_3, index = False)
        
        st.download_button('Download CSV', text_contents, 'text/xlsx')
        st.download_button('Download CSV', text_contents)
        
        with open(f'{fime_name_to_excel}.xlsx') as f:
            st.download_button('Download CSV', f)
            
        if st.download_button(...):
            st.write('Thanks for downloading!')
