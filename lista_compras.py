# -*- coding: utf-8 python -*-
import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Guanabara Mensal - Casal", page_icon="🛒", layout="centered")

# Estilo Customizado para replicar o layout da imagem
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* Banner de visualização */
    .active-list-info {
        background-color: #fffbeb;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #fef3c7;
        margin-bottom: 20px;
        text-align: center;
        color: #92400e;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Ajuste de métricas */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
    }
    
    /* Remover padding excessivo das colunas para mobile */
    [data-testid="column"] {
        padding: 0 5px !important;
    }

    /* Estilização dos inputs para ficarem mais compactos como na imagem */
    .stNumberInput div div input {
        padding: 5px !important;
        text-align: center !important;
    }

    /* Botão de lixeira vermelho ao passar o mouse */
    .stButton>button:hover {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
    }
    
    /* Linha divisória sutil */
    hr {
        margin: 1rem 0 !important;
    }

    /* Títulos de categoria com ícones */
    .category-header {
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS ---
def get_default_data():
    return [
        {"categoria": "Mercearia & Despensa", "itens": [
            {"id": 1, "nome": "Arroz Branco (5kg)", "qtd": 2, "preco": 18.95, "checked": False},
            {"id": 2, "nome": "Feijão Preto (1kg)", "qtd": 4, "preco": 7.50, "checked": False},
            {"id": 3, "nome": "Açúcar Refinado (1kg)", "qtd": 3, "preco": 3.99, "checked": False},
            {"id": 4, "nome": "Café Torrado (500g)", "qtd": 3, "preco": 16.90, "checked": False},
            {"id": 5, "nome": "Óleo de Soja (900ml)", "qtd": 4, "preco": 6.99, "checked": False},
            {"id": 6, "nome": "Macarrão Espaguete", "qtd": 5, "preco": 3.49, "checked": False},
        ]},
        {"categoria": "Açougue & Proteínas", "itens": [
            {"id": 11, "nome": "Frango (Peito kg)", "qtd": 5, "preco": 19.90, "checked": False},
            {"id": 12, "nome": "Carne Moída (kg)", "qtd": 3, "preco": 34.90, "checked": False},
        ]}
    ]

if 'listas_compras' not in st.session_state:
    st.session_state.listas_compras = {
        "Lista Mensal Padrão": get_default_data()
    }

if 'lista_ativa' not in st.session_state:
    st.session_state.lista_ativa = "Lista Mensal Padrão"

if 'aba_selecionada' not in st.session_state:
    st.session_state.aba_selecionada = "📋 Lista de Compras"

# --- NAVEGAÇÃO SUPERIOR ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📋 Lista de Compras", type="primary" if st.session_state.aba_selecionada == "📋 Lista de Compras" else "secondary"):
        st.session_state.aba_selecionada = "📋 Lista de Compras"
        st.rerun()
with col_nav2:
    if st.button("⚙️ Gerenciar Listas", type="primary" if st.session_state.aba_selecionada == "⚙️ Gerenciar Listas" else "secondary"):
        st.session_state.aba_selecionada = "⚙️ Gerenciar Listas"
        st.rerun()

st.divider()

# --- ABA: LISTA DE COMPRAS ---
if st.session_state.aba_selecionada == "📋 Lista de Compras":
    current_list = st.session_state.listas_compras[st.session_state.lista_ativa]
    
    # Banner de status da lista ativa
    st.markdown(f'<div class="active-list-info">Visualizando: {st.session_state.lista_ativa}</div>', unsafe_allow_html=True)

    # Cadastro Expansível
    with st.expander("➕ Cadastrar Produto ou Categoria", expanded=False):
        c_prod, c_cat = st.tabs(["Produto", "Categoria"])
        with c_prod:
            with st.form("add_p"):
                n = st.text_input("Nome")
                cat_opt = [c["categoria"] for c in current_list]
                sel_c = st.selectbox("Categoria", range(len(cat_opt)), format_func=lambda x: cat_opt[x])
                col_p1, col_p2 = st.columns(2)
                q = col_p1.number_input("Qtd", min_value=1, value=1)
                p = col_p2.number_input("Preço R$", min_value=0.0, value=0.0, step=0.01)
                if st.form_submit_button("Adicionar"):
                    current_list[sel_c]["itens"].append({"id": int(pd.Timestamp.now().timestamp()), "nome": n, "qtd": int(q), "preco": float(p), "checked": False})
                    st.rerun()
        with c_cat:
            new_c = st.text_input("Nova Categoria")
            if st.button("Criar"):
                current_list.append({"categoria": new_c, "itens": []})
                st.rerun()

    # Totais (Exatamente como na imagem)
    total_geral = 0
    total_carrinho = 0
    for cat in current_list:
        for item in cat["itens"]:
            total_geral += item["qtd"] * item["preco"]
            if item["checked"]: total_carrinho += item["qtd"] * item["preco"]

    col_met1, col_met2 = st.columns(2)
    col_met1.metric("Total Estimado", f"R$ {total_geral:.2f}")
    col_met2.metric("No Carrinho", f"R$ {total_carrinho:.2f}", delta=f"R$ {total_geral - total_carrinho:.2f}", delta_color="inverse")
    
    st.divider()

    # Renderização da Lista (Layout de linha idêntico à imagem)
    for cat_idx, categoria in enumerate(current_list):
        with st.expander(f"📦 {categoria['categoria']}", expanded=True):
            to_delete = []
            for item_idx, item in enumerate(categoria["itens"]):
                # Proporções otimizadas para manter horizontal em telas menores
                c_chk, c_name, c_qtd, c_prc, c_del = st.columns([0.2, 2.5, 0.7, 1.2, 0.4])
                
                with c_chk:
                    item["checked"] = st.checkbox("", value=item["checked"], key=f"c_{item['id']}")
                
                with c_name:
                    text_style = "text-decoration: line-through; color: gray;" if item["checked"] else "font-weight: 500;"
                    st.markdown(f'<p style="margin-top: 5px; {text_style}">{item["nome"]}</p>', unsafe_allow_html=True)
                
                with c_qtd:
                    item["qtd"] = st.number_input("Qtd", min_value=0, step=1, value=int(item["qtd"]), key=f"q_{item['id']}", label_visibility="collapsed")
                
                with c_prc:
                    # Formatação de preço como na imagem (ex: 18,95)
                    item["preco"] = st.number_input("R$", min_value=0.0, step=0.01, value=float(item["preco"]), key=f"p_{item['id']}", label_visibility="collapsed")
                
                with c_del:
                    if st.button("🗑️", key=f"d_{item['id']}"):
                        to_delete.append(item_idx)
            
            if to_delete:
                for i in sorted(to_delete, reverse=True):
                    categoria["itens"].pop(i)
                st.rerun()

# --- ABA: GERENCIAR LISTAS ---
elif st.session_state.aba_selecionada == "⚙️ Gerenciar Listas":
    st.subheader("Minhas Listas")
    
    with st.expander("🆕 Criar Nova Lista do Zero"):
        new_name = st.text_input("Nome da Lista")
        if st.button("Confirmar"):
            st.session_state.listas_compras[new_name] = [{"categoria": "Geral", "itens": []}]
            st.session_state.lista_ativa = new_name
            st.session_state.aba_selecionada = "📋 Lista de Compras"
            st.rerun()

    st.divider()
    for nome in list(st.session_state.listas_compras.keys()):
        c_n, c_v, c_e = st.columns([3, 1, 1])
        c_n.markdown(f"**{nome}**")
        if c_v.button("Visualizar", key=f"v_{nome}"):
            st.session_state.lista_ativa = nome
            st.session_state.aba_selecionada = "📋 Lista de Compras"
            st.rerun()
        if nome != "Lista Mensal Padrão":
            if c_e.button("Excluir", key=f"e_{nome}"):
                del st.session_state.listas_compras[nome]
                if st.session_state.lista_ativa == nome: st.session_state.lista_ativa = "Lista Mensal Padrão"
                st.rerun()
        else:
            if c_e.button("Resetar", key="r_pad"):
                st.session_state.listas_compras["Lista Mensal Padrão"] = get_default_data()
                st.rerun()

    st.divider()
    if st.button("📥 Exportar para WhatsApp"):
        active = st.session_state.listas_compras[st.session_state.lista_ativa]
        total = 0
        txt = f"*🛒 LISTA: {st.session_state.lista_ativa.upper()}*\n"
        txt += "--------------------------------\n\n"
        for cat in active:
            if not cat["itens"]: continue
            txt += f"*[{cat['categoria'].upper()}]*\n"
            for it in cat["itens"]:
                total += it['qtd'] * it['preco']
                txt += f"{it['qtd']} - *{it['nome']}* - _R$ {it['preco']:.2f}_\n"
            txt += "--------------------------------\n"
        txt += f"\n*💰 TOTAL GERAL: R$ {total:.2f}*"
        st.text_area("Copie o texto:", value=txt, height=200)
