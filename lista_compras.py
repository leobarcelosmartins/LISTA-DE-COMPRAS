# -*- coding: utf-8 python -*-
import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Guanabara Mensal - Casal", page_icon="🛒", layout="centered")

# Estilo Customizado (Tema Guanabara)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .total-box {
        background-color: #1e40af;
        color: #facc15;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .category-header {
        color: #1e40af;
        background-color: #eff6ff;
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
        font-weight: bold;
        border-left: 5px solid #facc15;
    }
    .active-list-info {
        background-color: #fffbeb;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #fef3c7;
        margin-bottom: 15px;
        text-align: center;
        color: #92400e;
        font-weight: bold;
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
            {"id": 7, "nome": "Molho de Tomate", "qtd": 6, "preco": 2.15, "checked": False},
            {"id": 8, "nome": "Sal Refinado (1kg)", "qtd": 1, "preco": 1.99, "checked": False},
        ]},
        {"categoria": "Açougue & Proteínas", "itens": [
            {"id": 11, "nome": "Frango (Peito kg)", "qtd": 5, "preco": 19.90, "checked": False},
            {"id": 12, "nome": "Carne Moída (kg)", "qtd": 3, "preco": 34.90, "checked": False},
            {"id": 13, "nome": "Ovos Brancos (30 un)", "qtd": 2, "preco": 17.50, "checked": False},
            {"id": 14, "nome": "Salsicha (kg)", "qtd": 1, "preco": 11.90, "checked": False},
        ]},
        {"categoria": "Higiene & Limpeza", "itens": [
            {"id": 31, "nome": "Papel Higiênico (12r)", "qtd": 2, "preco": 16.90, "checked": False},
            {"id": 32, "nome": "Sabão em Pó (1.6kg)", "qtd": 1, "preco": 18.50, "checked": False},
            {"id": 33, "nome": "Detergente Líquido", "qtd": 5, "preco": 2.39, "checked": False},
            {"id": 35, "nome": "Sabonete (un)", "qtd": 8, "preco": 2.45, "checked": False},
        ]}
    ]

# Persistência no Session State
if 'listas_compras' not in st.session_state:
    st.session_state.listas_compras = {
        "Lista Mensal Padrão": get_default_data()
    }

if 'lista_ativa' not in st.session_state:
    st.session_state.lista_ativa = "Lista Mensal Padrão"

if 'aba_selecionada' not in st.session_state:
    st.session_state.aba_selecionada = "📋 Lista de Compras"

# --- HEADER ---
st.markdown('<div class="total-box"><h1>🛒 Guanabara Digital</h1><p>Gestão de Listas de Compras</p></div>', unsafe_allow_html=True)

# --- NAVEGAÇÃO CUSTOMIZADA ---
col_n1, col_n2 = st.columns(2)
if col_n1.button("📋 Lista de Compras", type="primary" if st.session_state.aba_selecionada == "📋 Lista de Compras" else "secondary"):
    st.session_state.aba_selecionada = "📋 Lista de Compras"
    st.rerun()
if col_n2.button("⚙️ Gerenciar Listas", type="primary" if st.session_state.aba_selecionada == "⚙️ Gerenciar Listas" else "secondary"):
    st.session_state.aba_selecionada = "⚙️ Gerenciar Listas"
    st.rerun()

st.divider()

# --- CONTEÚDO DA ABA: LISTA DE COMPRAS ---
if st.session_state.aba_selecionada == "📋 Lista de Compras":
    current_list = st.session_state.listas_compras[st.session_state.lista_ativa]
    
    st.markdown(f'<div class="active-list-info">Visualizando: {st.session_state.lista_ativa}</div>', unsafe_allow_html=True)

    # Cadastro de Produtos e Categorias
    with st.expander("➕ Cadastrar Produto ou Categoria", expanded=False):
        subtab_prod, subtab_cat = st.tabs(["Produto", "Categoria"])
        
        with subtab_prod:
            with st.form("form_add_prod"):
                nome_p = st.text_input("Nome do Produto")
                cat_names = [c["categoria"] for c in current_list]
                
                if cat_names:
                    cat_idx = st.selectbox("Categoria", range(len(cat_names)), format_func=lambda x: cat_names[x])
                    c_col1, c_col2 = st.columns(2)
                    qtd_p = c_col1.number_input("Qtd", min_value=1, value=1, step=1)
                    prc_p = c_col2.number_input("Preço R$", min_value=0.0, value=0.0, step=0.01)
                    
                    if st.form_submit_button("Adicionar à Lista"):
                        if nome_p:
                            new_item = {
                                "id": int(pd.Timestamp.now().timestamp()),
                                "nome": nome_p,
                                "qtd": int(qtd_p),
                                "preco": float(prc_p),
                                "checked": False
                            }
                            current_list[cat_idx]["itens"].append(new_item)
                            st.success(f"{nome_p} adicionado!")
                            st.rerun()
                else:
                    st.warning("Crie uma categoria primeiro.")
        
        with subtab_cat:
            new_cat_name = st.text_input("Nome da Nova Categoria")
            if st.button("Criar Categoria"):
                if new_cat_name and new_cat_name not in [c["categoria"] for c in current_list]:
                    current_list.append({"categoria": new_cat_name, "itens": []})
                    st.success(f"Categoria {new_cat_name} criada!")
                    st.rerun()

    # Totais
    total_geral = 0
    total_no_carrinho = 0
    for cat in current_list:
        for item in cat["itens"]:
            sub = item["qtd"] * item["preco"]
            total_geral += sub
            if item["checked"]: total_no_carrinho += sub

    col_t1, col_t2 = st.columns(2)
    col_t1.metric("Total Estimado", f"R$ {total_geral:.2f}")
    col_t2.metric("No Carrinho", f"R$ {total_no_carrinho:.2f}", delta=f"R$ {total_geral - total_no_carrinho:.2f}", delta_color="inverse")
    
    st.progress(total_no_carrinho / total_geral if total_geral > 0 else 0)

    # Listagem
    for cat_idx, categoria in enumerate(current_list):
        if categoria["itens"] or len(current_list) > 0:
            with st.expander(f"📦 {categoria['categoria']}", expanded=True):
                items_to_del = []
                for item_idx, item in enumerate(categoria["itens"]):
                    c1, c2, c3, c4, c5 = st.columns([0.5, 3, 1.2, 1.5, 0.5])
                    with c1:
                        item["checked"] = st.checkbox("", value=item["checked"], key=f"chk_{st.session_state.lista_ativa}_{item['id']}")
                    with c2:
                        label = f"~~{item['nome']}~~" if item["checked"] else item["nome"]
                        st.markdown(f"**{label}**")
                    with c3:
                        item["qtd"] = st.number_input("Qtd", min_value=0, step=1, value=int(item["qtd"]), key=f"qtd_{st.session_state.lista_ativa}_{item['id']}", label_visibility="collapsed")
                    with c4:
                        item["preco"] = st.number_input("R$", min_value=0.0, step=0.01, value=float(item["preco"]), key=f"prc_{st.session_state.lista_ativa}_{item['id']}", label_visibility="collapsed")
                    with c5:
                        if st.button("🗑️", key=f"del_{st.session_state.lista_ativa}_{item['id']}"):
                            items_to_del.append(item_idx)
                
                if items_to_del:
                    for i in sorted(items_to_del, reverse=True):
                        categoria["itens"].pop(i)
                    st.rerun()

# --- CONTEÚDO DA ABA: GERENCIAR LISTAS ---
elif st.session_state.aba_selecionada == "⚙️ Gerenciar Listas":
    st.subheader("Minhas Listas")
    
    # Criar Nova Lista
    with st.expander("🆕 Criar Nova Lista do Zero", expanded=False):
        new_list_name = st.text_input("Nome da Nova Lista", placeholder="Ex: Churrasco de Domingo")
        if st.button("Confirmar Nova Lista"):
            if new_list_name and new_list_name not in st.session_state.listas_compras:
                st.session_state.listas_compras[new_list_name] = [{"categoria": "Geral", "itens": []}]
                st.session_state.lista_ativa = new_list_name
                st.session_state.aba_selecionada = "📋 Lista de Compras"
                st.rerun()
            else:
                st.error("Nome inválido ou já existente.")

    st.divider()

    # Tabela de Listas
    for nome_lista in list(st.session_state.listas_compras.keys()):
        col_n, col_v, col_e = st.columns([3, 1, 1])
        col_n.markdown(f"**{nome_lista}**")
        if col_v.button("Visualizar", key=f"view_{nome_lista}"):
            st.session_state.lista_ativa = nome_lista
            st.session_state.aba_selecionada = "📋 Lista de Compras"
            st.rerun()
        if nome_lista != "Lista Mensal Padrão":
            if col_e.button("Excluir", key=f"excluir_{nome_lista}"):
                del st.session_state.listas_compras[nome_lista]
                if st.session_state.lista_ativa == nome_lista:
                    st.session_state.lista_ativa = "Lista Mensal Padrão"
                st.rerun()
        else:
            col_e.button("Resetar", key="reset_padrao", on_click=lambda: st.session_state.listas_compras.update({"Lista Mensal Padrão": get_default_data()}))

    st.divider()
    
    # EXPORTAÇÃO PARA WHATSAPP
    if st.button("📥 Exportar Lista Ativa para WhatsApp"):
        total_export = 0
        lista_texto = f"*🛒 LISTA: {st.session_state.lista_ativa.upper()}*\n"
        lista_texto += "--------------------------------\n\n"
        
        for cat in st.session_state.listas_compras[st.session_state.lista_ativa]:
            if not cat["itens"]: continue
            
            lista_texto += f"*[{cat['categoria'].upper()}]*\n"
            for item in cat["itens"]:
                subtotal = item['qtd'] * item['preco']
                total_export += subtotal
                # Formatação solicitada: qtd - *descrição* - _preço_
                lista_texto += f"{item['qtd']} - *{item['nome']}* - _R$ {item['preco']:.2f}_\n"
            
            lista_texto += "--------------------------------\n"
        
        lista_texto += f"\n*💰 TOTAL GERAL: R$ {total_export:.2f}*"
        
        st.info("Texto formatado para WhatsApp abaixo. Copie e cole na conversa!")
        st.text_area("Texto para Copiar:", value=lista_texto, height=350)
