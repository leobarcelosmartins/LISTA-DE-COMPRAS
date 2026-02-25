import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Lista de Compras Mensal", page_icon="🛒", layout="centered")

# Estilo Customizado para as cores do Guanabara
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
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
        border-bottom: 2px solid #1e40af;
        padding-bottom: 5px;
        margin-top: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Dados Iniciais
if 'compras' not in st.session_state:
    st.session_state.compras = [
        {"categoria": "Mercearia & Despensa", "itens": [
            {"id": 1, "nome": "Arroz Branco (5kg)", "qtd": 2, "preco": 18.95, "checked": False},
            {"id": 2, "nome": "Feijão Preto (1kg)", "qtd": 4, "preco": 7.50, "checked": False},
            {"id": 3, "nome": "Açúcar (1kg)", "qtd": 3, "preco": 3.99, "checked": False},
            {"id": 4, "nome": "Café (500g)", "qtd": 3, "preco": 16.90, "checked": False},
            {"id": 5, "nome": "Óleo de Soja", "qtd": 4, "preco": 6.99, "checked": False}
        ]},
        {"categoria": "Açougue & Proteínas", "itens": [
            {"id": 11, "nome": "Frango (Peito kg)", "qtd": 4, "preco": 19.90, "checked": False},
            {"id": 12, "nome": "Carne Moída (kg)", "qtd": 2, "preco": 34.90, "checked": False},
            {"id": 14, "nome": "Ovos (30 un)", "qtd": 2, "preco": 17.50, "checked": False}
        ]},
        {"categoria": "Limpeza & Higiene", "itens": [
            {"id": 27, "nome": "Papel Higiênico (12r)", "qtd": 2, "preco": 16.90, "checked": False},
            {"id": 28, "nome": "Detergente", "qtd": 4, "preco": 2.39, "checked": False}
        ]}
    ]

# Título e Header
st.markdown('<div class="total-box"><h1>🛒 Lista de Compra Supermercado</h1><p>(30 dias)</p></div>', unsafe_allow_html=True)

# Funções de Lógica
def add_new_item(nome, cat_idx, qtd, preco):
    new_id = int(pd.Timestamp.now().timestamp())
    st.session_state.compras[cat_idx]["itens"].append({
        "id": new_id,
        "nome": nome,
        "qtd": int(qtd),
        "preco": float(preco),
        "checked": False
    })

# --- ÁREA DE ADIÇÃO ---
with st.expander("➕ Adicionar Novo Item"):
    with st.form("form_add"):
        col1, col2 = st.columns(2)
        with col1:
            nome_novo = st.text_input("Nome do Produto")
            cat_opcoes = [c["categoria"] for c in st.session_state.compras]
            cat_selecionada = st.selectbox("Categoria", range(len(cat_opcoes)), format_func=lambda x: cat_opcoes[x])
        with col2:
            qtd_nova = st.number_input("Quantidade", min_value=1, step=1, value=1)
            preco_novo = st.number_input("Preço Unitário R$", min_value=0.0, step=0.1, value=0.0)
        
        submitted = st.form_submit_button("Confirmar Adição")
        if submitted and nome_novo:
            add_new_item(nome_novo, cat_selecionada, qtd_nova, preco_novo)
            st.success(f"{nome_novo} adicionado!")
            st.rerun()

# --- CÁLCULO DE TOTAIS ---
total_geral = 0
total_no_carrinho = 0

for cat in st.session_state.compras:
    for item in cat["itens"]:
        subtotal = item["qtd"] * item["preco"]
        total_geral += subtotal
        if item["checked"]:
            total_no_carrinho += subtotal

# --- BARRA DE PROGRESSO ---
progresso = total_no_carrinho / total_geral if total_geral > 0 else 0
st.write(f"**Progresso no Carrinho: R$ {total_no_carrinho:.2f} / R$ {total_geral:.2f}**")
st.progress(progresso)

# --- LISTAGEM ---
for cat_idx, categoria in enumerate(st.session_state.compras):
    st.markdown(f'<div class="category-header">{categoria["categoria"]}</div>', unsafe_allow_html=True)
    
    # Lista de itens para remover
    indices_para_remover = []
    
    for item_idx, item in enumerate(categoria["itens"]):
        col_check, col_info, col_edit = st.columns([0.5, 3, 2])
        
        with col_check:
            # Checkbox para marcar como comprado
            item["checked"] = st.checkbox("", value=item["checked"], key=f"check_{item['id']}")
            
        with col_info:
            label = f"~~{item['nome']}~~" if item["checked"] else item["nome"]
            st.markdown(f"**{label}**")
            st.caption(f"Subtotal: R$ {(item['qtd'] * item['preco']):.2f}")
            
        with col_edit:
            sub_col1, sub_col2, sub_col3 = st.columns([1, 1.5, 0.5])
            with sub_col1:
                # Quantidade Inteira
                item["qtd"] = st.number_input("Qtd", min_value=0, step=1, value=item["qtd"], key=f"qtd_{item['id']}", label_visibility="collapsed")
            with sub_col2:
                # Preço Editável
                item["preco"] = st.number_input("R$", min_value=0.0, step=0.01, value=float(item["preco"]), key=f"prc_{item['id']}", label_visibility="collapsed")
            with sub_col3:
                if st.button("🗑️", key=f"del_{item['id']}"):
                    indices_para_remover.append(item_idx)

    # Remover itens marcados para exclusão
    if indices_para_remover:
        for idx in sorted(indices_para_remover, reverse=True):
            categoria["itens"].pop(idx)
        st.rerun()

# --- FOOTER FIXO (SIMULADO) ---
st.markdown("---")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.metric("Total Geral", f"R$ {total_geral:.2f}")
with col_f2:
    falta = total_geral - total_no_carrinho
    st.metric("Falta Comprar", f"R$ {falta:.2f}", delta_color="inverse")

if st.button("Limpar Tudo e Reiniciar"):
    del st.session_state.compras
    st.rerun()


