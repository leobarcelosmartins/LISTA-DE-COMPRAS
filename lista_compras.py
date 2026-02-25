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
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS (LISTA COMPLETA 30 DIAS) ---
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
        {"categoria": "Laticínios & Frios", "itens": [
            {"id": 21, "nome": "Leite Integral (1L)", "qtd": 12, "preco": 4.95, "checked": False},
            {"id": 22, "nome": "Manteiga (500g)", "qtd": 1, "preco": 22.90, "checked": False},
            {"id": 23, "nome": "Queijo Muçarela (500g)", "qtd": 2, "preco": 24.00, "checked": False},
            {"id": 24, "nome": "Presunto (500g)", "qtd": 2, "preco": 16.00, "checked": False},
        ]},
        {"categoria": "Higiene & Limpeza", "itens": [
            {"id": 31, "nome": "Papel Higiênico (12r)", "qtd": 2, "preco": 16.90, "checked": False},
            {"id": 32, "nome": "Sabão em Pó (1.6kg)", "qtd": 1, "preco": 18.50, "checked": False},
            {"id": 33, "nome": "Detergente Líquido", "qtd": 5, "preco": 2.39, "checked": False},
            {"id": 34, "nome": "Amaciante (2L)", "qtd": 1, "preco": 14.90, "checked": False},
            {"id": 35, "nome": "Sabonete (un)", "qtd": 8, "preco": 2.45, "checked": False},
            {"id": 36, "nome": "Creme Dental", "qtd": 3, "preco": 4.50, "checked": False},
        ]},
        {"categoria": "Hortifruti", "itens": [
            {"id": 41, "nome": "Batata Inglesa (kg)", "qtd": 3, "preco": 6.50, "checked": False},
            {"id": 42, "nome": "Cebola (kg)", "qtd": 2, "preco": 5.90, "checked": False},
            {"id": 43, "nome": "Alho (200g)", "qtd": 2, "preco": 8.50, "checked": False},
            {"id": 44, "nome": "Tomate (kg)", "qtd": 3, "preco": 7.90, "checked": False},
        ]}
    ]

if 'compras' not in st.session_state:
    st.session_state.compras = get_default_data()

# --- HEADER ---
st.markdown('<div class="total-box"><h1>🛒 Guanabara Digital</h1><p>Gestão de Compras para Casal</p></div>', unsafe_allow_html=True)

# --- NAVEGAÇÃO POR ABAS ---
tab_lista, tab_cadastro, tab_gestao = st.tabs(["📋 Minha Lista", "➕ Cadastrar Produtos", "⚙️ Gerenciar Listas"])

# --- ABA 1: MINHA LISTA ---
with tab_lista:
    # Cálculo de Totais
    total_geral = 0
    total_no_carrinho = 0
    for cat in st.session_state.compras:
        for item in cat["itens"]:
            sub = item["qtd"] * item["preco"]
            total_geral += sub
            if item["checked"]: total_no_carrinho += sub

    col_t1, col_t2 = st.columns(2)
    col_t1.metric("Total Estimado", f"R$ {total_geral:.2f}")
    col_t2.metric("No Carrinho", f"R$ {total_no_carrinho:.2f}", delta=f"R$ {total_geral - total_no_carrinho:.2f}", delta_color="inverse")
    
    st.progress(total_no_carrinho / total_geral if total_geral > 0 else 0)

    for cat_idx, categoria in enumerate(st.session_state.compras):
        with st.expander(f"📦 {categoria['categoria']}", expanded=True):
            items_to_del = []
            for item_idx, item in enumerate(categoria["itens"]):
                c1, c2, c3, c4, c5 = st.columns([0.5, 3, 1.2, 1.5, 0.5])
                
                with c1:
                    item["checked"] = st.checkbox("", value=item["checked"], key=f"chk_{item['id']}")
                
                with c2:
                    label = f"~~{item['nome']}~~" if item["checked"] else item["nome"]
                    st.markdown(f"**{label}**")
                
                with c3:
                    item["qtd"] = st.number_input("Qtd", min_value=0, step=1, value=int(item["qtd"]), key=f"qtd_{item['id']}", label_visibility="collapsed")
                
                with c4:
                    item["preco"] = st.number_input("R$", min_value=0.0, step=0.01, value=float(item["preco"]), key=f"prc_{item['id']}", label_visibility="collapsed")
                
                with c5:
                    if st.button("🗑️", key=f"del_{item['id']}"):
                        items_to_del.append(item_idx)
            
            if items_to_del:
                for i in sorted(items_to_del, reverse=True):
                    categoria["itens"].pop(i)
                st.rerun()

# --- ABA 2: CADASTRAR PRODUTOS & CATEGORIAS ---
with tab_cadastro:
    st.subheader("Novos Itens")
    with st.form("add_product"):
        nome_prod = st.text_input("Nome do Produto")
        cat_nomes = [c["categoria"] for c in st.session_state.compras]
        cat_sel = st.selectbox("Selecione a Categoria", range(len(cat_nomes)), format_func=lambda x: cat_nomes[x])
        c_p1, c_p2 = st.columns(2)
        qtd_p = c_p1.number_input("Quantidade Inicial", min_value=1, step=1)
        prc_p = c_p2.number_input("Preço Unitário R$", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Adicionar à Lista"):
            if nome_prod:
                new_item = {
                    "id": int(pd.Timestamp.now().timestamp()),
                    "nome": nome_prod,
                    "qtd": int(qtd_p),
                    "preco": float(prc_p),
                    "checked": False
                }
                st.session_state.compras[cat_sel]["itens"].append(new_item)
                st.success(f"{nome_prod} adicionado!")
                st.rerun()

    st.divider()
    st.subheader("Nova Categoria")
    new_cat_name = st.text_input("Nome da Categoria")
    if st.button("Criar Categoria"):
        if new_cat_name and new_cat_name not in [c["categoria"] for c in st.session_state.compras]:
            st.session_state.compras.append({"categoria": new_cat_name, "itens": []})
            st.success(f"Categoria {new_cat_name} criada!")
            st.rerun()

# --- ABA 3: GERENCIAR LISTAS ---
with tab_gestao:
    st.subheader("Controle de Listas")
    
    col_g1, col_g2 = st.columns(2)
    
    if col_g1.button("🔥 Criar Nova Lista do Zero"):
        st.session_state.compras = [{"categoria": "Mercearia", "itens": []}]
        st.warning("Todas as categorias e itens foram removidos. Comece a cadastrar!")
        st.rerun()
        
    if col_g2.button("🔄 Restaurar Padrão (30 dias)"):
        st.session_state.compras = get_default_data()
        st.info("Lista padrão carregada com sucesso.")
        st.rerun()

    st.divider()
    st.markdown("### 📝 Instruções de Edição")
    st.write("1. Na aba **Minha Lista**, você pode editar quantidades e preços diretamente nos campos.")
    st.write("2. Itens marcados com 🗑️ serão removidos permanentemente.")
    st.write("3. O progresso é salvo enquanto a aba do navegador estiver aberta.")
    
    if st.button("📥 Exportar para Texto (Copiar)"):
        lista_texto = "LISTA DE COMPRAS GUANABARA\n\n"
        for cat in st.session_state.compras:
            lista_texto += f"[{cat['categoria']}]\n"
            for item in cat["itens"]:
                status = "[X]" if item["checked"] else "[ ]"
                lista_texto += f"{status} {item['nome']} - Qtd: {item['qtd']} - R$ {item['preco']:.2f}\n"
            lista_texto += "\n"
        st.text_area("Copie o texto abaixo:", value=lista_texto, height=300)
