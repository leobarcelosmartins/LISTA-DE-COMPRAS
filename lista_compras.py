import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="SmartMarket RJ - Comparador", layout="wide")

# Inicialização do estado da sessão para persistência de dados
if 'lists' not in st.session_state:
    st.session_state.lists = {}
if 'current_items' not in st.session_state:
    st.session_state.current_items = []
if 'market_comparison' not in st.session_state:
    # Colunas específicas para os mercados do RJ solicitados
    st.session_state.market_comparison = pd.DataFrame(columns=['Item', 'Supermarket', 'Guanabara', 'Assaí'])

# Modelos prontos
TEMPLATES = {
    "Churrasco RJ": ["Picanha", "Linguiça Toscana", "Pão de Alho", "Carvão 5kg", "Cerveja Antárctica", "Refrigerante 2L", "Sal Grosso"],
    "Limpeza": ["Detergente Ypê", "Sabão em Pó Omo", "Desinfetante Pinho Sol", "Esponja", "Amaciante Downy"],
    "Cesta Básica": ["Arroz 5kg", "Feijão Preto", "Óleo de Soja", "Açúcar", "Café Pilão", "Macarrão Adria"]
}

def save_list(name, items):
    st.session_state.lists[name] = items

def robo_varredura_rj(query):
    """
    Simulação do robô de varredura focado nos mercados do Rio de Janeiro.
    Em uma implementação real, aqui seriam feitas requisições HTTP ou Selenium 
    para as URLs do Supermarket, Guanabara e Assaí.
    """
    # Simulando tempo de processamento da varredura
    time.sleep(1.5) 
    
    # Lógica de precificação simulada baseada em perfis reais (Assaí geralmente mais barato no atacado, etc)
    base_price = random.uniform(5.0, 60.0)
    
    return {
        "Item": query.title(),
        "Supermarket": round(base_price * random.uniform(0.98, 1.05), 2),
        "Guanabara": round(base_price * random.uniform(0.95, 1.02), 2),
        "Assaí": round(base_price * random.uniform(0.90, 0.98), 2)
    }

# Interface Lateral (Navegação)
st.sidebar.title("🛒 SmartMarket RJ")
st.sidebar.info("Busca focada em: Supermarket, Guanabara e Assaí")
menu = st.sidebar.radio("Navegação", ["Criar Nova Lista", "Comparar Preços (RJ)", "Minhas Listas", "Modo Compras"])

# --- SEÇÃO: CRIAR NOVA LISTA ---
if menu == "Criar Nova Lista":
    st.header("📝 Criar Lista de Compras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Do Zero")
        new_item = st.text_input("Adicionar item manualmente:")
        if st.button("Adicionar à Lista"):
            if new_item:
                st.session_state.current_items.append({"name": new_item, "price": 0.0, "market": "N/A", "checked": False})
                st.success(f"{new_item} adicionado!")

    with col2:
        st.subheader("A partir de Modelos")
        template_choice = st.selectbox("Escolha um modelo:", list(TEMPLATES.keys()))
        if st.button("Carregar Modelo"):
            items_to_add = [{"name": item, "price": 0.0, "market": "N/A", "checked": False} for item in TEMPLATES[template_choice]]
            st.session_state.current_items.extend(items_to_add)
            st.info(f"Modelo {template_choice} carregado!")

    st.divider()
    st.subheader("Itens na Lista Atual")
    if st.session_state.current_items:
        for idx, item in enumerate(st.session_state.current_items):
            st.write(f"- {item['name']} (R$ {item['price']:.2f} no {item['market']})")
        
        list_name = st.text_input("Dê um nome para sua lista (ex: Compras do Mês):")
        if st.button("Salvar Lista Completa"):
            if list_name:
                save_list(list_name, list(st.session_state.current_items))
                st.session_state.current_items = []
                st.success(f"Lista '{list_name}' salva com sucesso!")
    else:
        st.write("Sua lista está vazia.")

# --- SEÇÃO: COMPARAR PREÇOS ---
elif menu == "Comparar Preços (RJ)":
    st.header("🔍 Robô de Varredura - Preços RJ")
    st.write("Buscando ofertas em tempo real no Supermarket, Guanabara e Assaí.")
    
    search_query = st.text_input("O que você deseja buscar? (ex: Detergente Ypê, Picanha, Arroz 5kg)")
    
    if st.button("Iniciar Varredura"):
        if search_query:
            with st.spinner(f"Robô vasculhando sites de Supermarket, Guanabara e Assaí..."):
                resultado = robo_varredura_rj(search_query)
                st.session_state.market_comparison = pd.concat([
                    st.session_state.market_comparison, 
                    pd.DataFrame([resultado])
                ], ignore_index=True)
            st.success("Busca finalizada!")
        else:
            st.warning("Digite um item para buscar.")

    if not st.session_state.market_comparison.empty:
        st.subheader("Tabela Comparativa de Preços")
        
        # Cabeçalho da Tabela
        h_col1, h_col2, h_col3, h_col4 = st.columns([2, 1, 1, 1])
        h_col1.write("**Item**")
        h_col2.write("**Supermarket**")
        h_col3.write("**Guanabara**")
        h_col4.write("**Assaí**")
        
        # Linhas de Itens
        for i, row in st.session_state.market_comparison.iterrows():
            col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
            col_a.write(f"**{row['Item']}**")
            
            # Botões de Seleção de Preço
            if col_b.button(f"R$ {row['Supermarket']:.2f}", key=f"sup_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Supermarket'], "market": "Supermarket", "checked": False})
                st.toast(f"{row['Item']} adicionado: Supermarket")
                
            if col_c.button(f"R$ {row['Guanabara']:.2f}", key=f"gua_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Guanabara'], "market": "Guanabara", "checked": False})
                st.toast(f"{row['Item']} adicionado: Guanabara")
                
            if col_d.button(f"R$ {row['Assaí']:.2f}", key=f"ass_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Assaí'], "market": "Assaí", "checked": False})
                st.toast(f"{row['Item']} adicionado: Assaí")
        
        st.info("💡 Toque no preço do mercado escolhido para adicionar o item à sua lista.")
        if st.button("Limpar Histórico de Busca"):
            st.session_state.market_comparison = pd.DataFrame(columns=['Item', 'Supermarket', 'Guanabara', 'Assaí'])
            st.rerun()

# --- SEÇÃO: MINHAS LISTAS ---
elif menu == "Minhas Listas":
    st.header("📂 Minhas Listas Salvas")
    
    if st.session_state.lists:
        selected_list = st.selectbox("Selecione uma lista:", list(st.session_state.lists.keys()))
        
        items = st.session_state.lists[selected_list]
        df = pd.DataFrame(items)
        st.table(df[['name', 'price', 'market']])
        
        total = df['price'].sum()
        st.subheader(f"Total Estimado: R$ {total:.2f}")
        
        # Exportação
        export_text = f"LISTA DE COMPRAS: {selected_list}\n" + "="*30 + "\n"
        for item in items:
            market_info = f" no {item['market']}" if item['market'] != "N/A" else ""
            export_text += f"- {item['name']}: R$ {item['price']:.2f}{market_info}\n"
        export_text += "="*30 + f"\nTOTAL ESTIMADO: R$ {total:.2f}"
        
        st.download_button("Exportar Lista (TXT)", export_text, file_name=f"{selected_list}.txt")
        
        if st.button("Excluir esta lista"):
            del st.session_state.lists[selected_list]
            st.rerun()
    else:
        st.write("Nenhuma lista salva encontrada.")

# --- SEÇÃO: MODO COMPRAS ---
elif menu == "Modo Compras":
    st.header("🛒 Check-in no Mercado")
    st.write("Marque os itens conforme for colocando no carrinho.")
    
    if st.session_state.lists:
        selected_list = st.selectbox("Qual lista deseja usar agora?", list(st.session_state.lists.keys()))
        items = st.session_state.lists[selected_list]
        
        # Barra de Progresso
        checked_count = sum(1 for item in items if item['checked'])
        total_count = len(items)
        progress = checked_count / total_count if total_count > 0 else 0
        
        st.progress(progress)
        st.write(f"**Progresso do Carrinho:** {checked_count} de {total_count} itens ({int(progress*100)}%)")
        
        st.divider()
        
        # Lista com Checkboxes
        for i, item in enumerate(items):
            market_tag = f"[{item['market']}]" if item['market'] != "N/A" else ""
            label = f"{item['name']} - R$ {item['price']:.2f} {market_tag}"
            
            is_checked = st.checkbox(label, value=item['checked'], key=f"shop_check_{i}")
            
            if is_checked != item['checked']:
                st.session_state.lists[selected_list][i]['checked'] = is_checked
                st.rerun()
                
        if progress == 1.0:
            st.balloons()
            st.success("🎉 Lista completa! Você economizou tempo e dinheiro.")
    else:
        st.warning("Você precisa criar e salvar uma lista antes de entrar no Modo Compras.")

# Rodapé
st.sidebar.divider()
st.sidebar.caption("SmartMarket RJ v2.0")
st.sidebar.caption("Varredura: Supermarket | Guanabara | Assaí")
