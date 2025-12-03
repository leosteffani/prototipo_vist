import streamlit as st
import pandas as pd
import re

texto2 = """1.2. Sub 2: Estado: Bom / Slot 02: NALT-C 3FE27289 AAbd04 / Slot 03: NALT-C 3FE27289 AAbd04 / Slot 04: NALT-C 3FE27289 AAbd04 / Slot 05: NALT-J 3FE61438 BAbf01 / Slot 06: NALT-C 3FE27289 AAbd04 / Slot 07: NALT-J 3FE61438 BAbf01 / Slot 08: NALT-C 3FE27289 AAbd04 / Slot 09: NALT-C 3FE27289 AAbd04 / Slot 10: NALT-C 3FE27289 AAbd04 / Slot 11: Vazio / Slot 12: Vazio / Slot 13: Vazio / Slot 14: Vazio / Slot 15: Vazio / Slot 16: Vazio / Slot 01: NALT-C 3FE27289 AAbd04 / Slot NTA: NANT-A 3FE26698 ABbc06 / Slot NTIO/17: Vazio / Slot NTB/18: Vazio"""
texto = """1.1. Sub 1: Estado: Bom / Slot 01: 3FE27944 ABaa02 / Slot 02: 3FE27944 ABaa02 / Slot 03: 3FE27944 ABaa02 / Slot 04: 3FE27944 ABaa02 / Slot 05: 3FE27944 ABaa02 / Slot 06: 3FE27944 ABaa02 / Slot 07: 3FE27944 ABaa02 / Slot 08: 3FE27944 ABaa02 / Slot NPIO: Vazio / Slot TAUS/17: Vazio / Slot 18: Vazio / Slot 09: 3FE27944 ABaa02 / Slot 10: 3FE27944 ABaa02 / Slot 11: 3FE27944 ABaa02 / Slot 12: Vazio / Slot 13: Vazio / Slot 14: Vazio / Slot 15: Vazio / Slot 16: Vazio"""
texto3 = """2.2. Sub 1 – DTC 1 DTC 20: Estado: Bom / Slot 01: Vazio / Slot 02: Vazio / Slot 03: Vazio / Slot 04: Vazio / Slot 05: Vazio / Slot 06: Vazio / Slot 07: R10 979.3909 CAIXA ECONÔMICA 512K / Slot 08: Vazio / Slot 09: Vazio / Slot 10: Vazio / Slot 11: Vazio / Slot 12: RJO 7104551 VM 64KB BRADESCO / Slot 13: Vazio / Slot 14: Vazio / Slot 15: rjo8001105 Telemar Nort Lest frame 64kbps mux01 slot porta 2 modem 14ctb/b67 a2 / Slot 16: Vazio / Slot 17: Vazio / Slot 18: Vazio / Slot 19: Vazio / Slot 20: Vazio / Slot 21: Vazio / Fabricante: DATACOM / Modelo: DM-SBT MP-20 / Slot 00: DM-SBT FAL DC F512/20 CC"""
texto4 = """2.3. Sub 2 – C1 PRI. C2 RED. IP31.21.2.62: Estado: Bom / Fabricante: DATACOM / Modelo: DM705 SUB HW2 / Slot HS1: Vazio / Slot HS2: Vazio / Slot C1: DM705-CPU64 HW2 / Slot C2: DM705-CPU64 HW2 / Slot A: DM705-E1Q / Slot B: Vazio / Slot C: DM705-6V35 / Slot D: DM705-6V35 / Slot E: DM705-DSL8 / Slot F: DM705-DSL8 / Slot G: DM705-DSL8 / Slot H: Vazio / Slot PW1: DM705 SUB FAL / Slot PW2: DM705 SUB FAL"""
texto5 = """2.4. Sub 3 - RJO_PRA-02 IP31.21.3.54: Estado: Bom / Fabricante: DATACOM / Modelo: DM705 SUB HW2 / Slot HS1: Vazio / Slot HS2: Vazio / Slot C1: DM705-CPU64 HW2 / Slot C2: DM705-CPU64 HW2 / Slot A: DM705-E1Q / Slot B: Vazio / Slot C: DM705-6V35 / Slot D: Vazio / Slot E: DM705-DSL8 / Slot F: Vazio / Slot G: Vazio / Slot PW1: DM705 SUB FAL / Slot PW2: DM705 SUB FAL"""
texto6 = """2.5. Sub 4: Estado: Bom / Fabricante: DATACOM / Modelo: DM-SBT SMP-20 / Slot 00: DM-SBT FAL DC F51220 CC / Slot 01: Vazio / Slot 02: Vazio / Slot 03: Vazio / Slot 04: Vazio / Slot 05: Vazio / Slot 06: Vazio / Slot 07: Vazio / Slot 08: Vazio / Slot 09: Vazio / Slot 10: Vazio / Slot 11: Vazio / Slot 12: Vazio / Slot 13: Vazio / Slot 14: Vazio / Slot 15: Vazio / Slot 16: Vazio / Slot 17: Vazio / Slot 18: Vazio / Slot 19: Vazio / Slot 20: Vazio / Slot 21: Vazio"""
# separa as partes
def mostrar_lista_formatada(titulo, itens, max_por_linha=3):
    st.subheader(titulo)

    # cria linhas com no máximo 3 elementos
    if len(itens) > 0:
        for i in range(0, len(itens), max_por_linha):
            cols = st.columns(max_por_linha)
            linha = itens[i:i + max_por_linha]

            for col, item in zip(cols, linha):
                col.write(f"- {item}")

def adicionar_slots(df, texto):
    # separa as partes por "/"
    partes = [p.strip() for p in texto.split(" / ")]

    slots = {}

    linha_raw = partes[0]

    # extrai tudo antes de "Estado:"
    if "Estado:" in linha_raw:
        nome_linha = linha_raw.split("Estado:")[0].strip()
    else:
        # fallback: até o primeiro ":"
        nome_linha = linha_raw.split(":")[0].strip()

    slots["Linha"] = nome_linha[:-1]
    # regex para capturar "Slot X: valor"
    regex = r"^Slot\s+([^:]+):\s*(.*)$"

    for p in partes:
        match = re.match(regex, p)
        if match:
            nome = match.group(1)   # ex: "01", "NTA", "NTIO/17"
            valor = match.group(2)
            if valor.strip().lower() == "vazio":
                slots[f"Slot_{nome}"] = "Vazio"
            else:
                slots[f"Slot_{nome}"] = valor

    # adiciona ao dataframe
    df = pd.concat([df, pd.DataFrame([slots])], ignore_index=True)

    # valores faltantes viram "Vazio"
    return df

def lista_slots_preenchidos(df, nome_linha):
    # localizar a linha
    linha_df = df[df["Linha"] == nome_linha]

    # caso não exista essa linha
    if linha_df.empty:
        return []
    # extrair a linha como dicionário
    linha = linha_df.iloc[0].to_dict()
    # coletar slots preenchidos
    resultado = []
    for coluna, valor in linha.items():
        if coluna.startswith("Slot_"):
            if isinstance(valor, str) and valor.strip().lower() == "vazio":
                continue
            if pd.isna(valor):
                continue
            if isinstance(valor, str) and valor.strip() == "":
                continue
            resultado.append(coluna)
    return resultado

def lista_slots_vazios(df, nome_linha):
    # localizar a linha
    linha_df = df[df["Linha"] == nome_linha]

    # caso não exista essa linha
    if linha_df.empty:
        return []
    # extrair a linha como dicionário
    linha = linha_df.iloc[0].to_dict()
    # coletar slots preenchidos
    resultado = []
    for coluna, valor in linha.items():
        if coluna.startswith("Slot_"):
            if isinstance(valor, str) and valor.strip().lower() != "vazio":
                continue
            if pd.isna(valor):
                continue
            if isinstance(valor, str) and valor.strip() == "":
                continue
            resultado.append(coluna)
    return resultado

st.set_page_config(
    page_title="Dashboard vistorias prototipo",
    page_icon="📊",
    layout="wide",
)

df = pd.DataFrame()
df = adicionar_slots(df,texto)
df = adicionar_slots(df,texto2)
df = adicionar_slots(df,texto3)
df = adicionar_slots(df,texto4)
df = adicionar_slots(df,texto5)
df = adicionar_slots(df,texto6)
df["item"] = df["Linha"].apply(lambda x: "Hack FL 204A-BT 11 - PRA-08" if x.startswith("1") else "Hack FL3B BT9")

st.sidebar.header("🔍 Filtros")

vistorias_disponiveis = ['PIEVT.344.1144916','PIEVT.344.1144917','PIEVT.344.1144918']
vistoria_selecionada = st.sidebar.selectbox("Vistoria", vistorias_disponiveis, index=0)
df["vistoria"] = 'PIEVT.344.1144916'

meses_disponiveis = ['25-01','25-02','25-03','25-04','25-05','25-06','25-07','25-08','25-09','25-10','25-11','25-12']
meses_selecionados = st.sidebar.select_slider(
    "intervalo de meses",
    options=meses_disponiveis,
    value=(meses_disponiveis[0], meses_disponiveis[-1])
)

df_meio = df[
    (df['vistoria'] == vistoria_selecionada)
]

itens_disponiveis =  sorted(df_meio['item'].unique())
itens_selecionados = st.sidebar.multiselect("itens", itens_disponiveis)

subitens_disponiveis =  sorted(df_meio['Linha'].unique())
subitens_selecionados = st.sidebar.multiselect("subitens", subitens_disponiveis)

df_filtrado = df_meio.copy()
df_filtrado = df_meio[
    (df_meio['item'].isin(itens_selecionados) if itens_selecionados else pd.Series([True] * len(df_meio))) &
    (df_meio['Linha'].isin(subitens_selecionados) if subitens_selecionados else pd.Series([True] * len(df_meio)))
]
st.title("Vistoria: " + vistoria_selecionada)

for item in df_filtrado['item'].unique():
    st.markdown("---")
    st.header(item)
    for linha in df_filtrado['Linha'].unique():
        df_temp = df_filtrado[(df_filtrado['item'] == item) & (df_filtrado['Linha'] == linha)]
        if df_temp.empty:
            continue
        st.markdown("")
        st.subheader(linha)
        col1, col2 = st.columns(2)
        with col1:
            mostrar_lista_formatada("Slots preenchidos:", lista_slots_preenchidos(df_temp, linha))
        with col2:
            mostrar_lista_formatada("Slots vazios:", lista_slots_vazios(df_temp, linha))
