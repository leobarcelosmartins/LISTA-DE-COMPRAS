import streamlit as st
import pandas as pd
import json

# Configuração da página
st.set_page_config(page_title="SmartMarket - Comparador e Lista", layout="wide")

# Inicialização do estado da sessão para persistência de dados
if 'lists' not in st.session_state:
    st.session_state.lists = {}
if 'current_items' not in st.session_state:
    st.session_state.current_items = []
if 'market_comparison' not in st.session_state:
    st.session_state.market_comparison = pd.DataFrame(columns=['Item', 'Mercado 1', 'Mercado 2', 'Mercado 3'])

# Modelos prontos
TEMPLATES = {
    "Churrasco": ["Carne Bovina", "Linguiça", "Pão de Alho", "Carvão", "Cerveja", "Refrigerante", "Sal Grosso"],
    "Limpeza Mensal": ["Detergente", "Sabão em Pó", "Desinfetante", "Esponja", "Amaciante", "Água Sanitária"],
    "Cesta Básica": ["Arroz", "Feijão", "Óleo", "Açúcar", "Café", "Macarrão", "Farinha"]
}

def save_list(name, items):
    st.session_state.lists[name] = items

# Interface Lateral (Navegação)
st.sidebar.title("🛒 SmartMarket")
menu = st.sidebar.radio("Navegação", ["Criar Nova Lista", "Comparar Preços", "Minhas Listas", "Modo Compras"])

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
            st.write(f"- {item['name']}")
        
        list_name = st.text_input("Dê um nome para sua lista (ex: Compras do Mês):")
        if st.button("Salvar Lista Completa"):
            if list_name:
                save_list(list_name, list(st.session_state.current_items))
                st.session_state.current_items = []
                st.success(f"Lista '{list_name}' salva com sucesso!")
    else:
        st.write("Sua lista está vazia.")

# --- SEÇÃO: COMPARAR PREÇOS ---
elif menu == "Comparar Preços":
    st.header("🔍 Comparador de Preços (Simulação de Varredura)")
    st.write("Busque os melhores preços na internet para montar sua lista.")
    
    search_query = st.text_input("O que você deseja buscar? (ex: Detergente Ypê)")
    
    if st.button("Varrer Internet"):
        # Simulando uma busca de preços (Em um app real, aqui entraria a lógica de scraping ou API)
        import random
        base_price = random.uniform(2.0, 50.0)
        mock_data = {
            "Item": search_query,
            "Mercado 1": round(base_price * 0.95, 2),
            "Mercado 2": round(base_price * 1.05, 2),
            "Mercado 3": round(base_price, 2)
        }
        st.session_state.market_comparison = pd.concat([st.session_state.market_comparison, pd.DataFrame([mock_data])], ignore_index=True)

    if not st.session_state.market_comparison.empty:
        st.subheader("Resultados da Comparação")
        
        # Exibindo a tabela para seleção
        for i, row in st.session_state.market_comparison.iterrows():
            col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
            col_a.write(f"**{row['Item']}**")
            
            if col_b.button(f"R$ {row['Mercado 1']:.2f} (M1)", key=f"m1_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Mercado 1'], "market": "Mercado 1", "checked": False})
                st.toast(f"{row['Item']} adicionado pelo preço do Mercado 1!")
                
            if col_c.button(f"R$ {row['Mercado 2']:.2f} (M2)", key=f"m2_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Mercado 2'], "market": "Mercado 2", "checked": False})
                st.toast(f"{row['Item']} adicionado pelo preço do Mercado 2!")
                
            if col_d.button(f"R$ {row['Mercado 3']:.2f} (M3)", key=f"m3_{i}"):
                st.session_state.current_items.append({"name": row['Item'], "price": row['Mercado 3'], "market": "Mercado 3", "checked": False})
                st.toast(f"{row['Item']} adicionado pelo preço do Mercado 3!")
        
        st.info("Clique no preço desejado para adicionar o item à sua lista atual.")
        if st.button("Limpar Buscas"):
            st.session_state.market_comparison = pd.DataFrame(columns=['Item', 'Mercado 1', 'Mercado 2', 'Mercado 3'])
            st.rerun()

# --- SEÇÃO: MINHAS LISTAS ---
elif menu == "Minhas Listas":
    st.header("📂 Minhas Listas Salvas")
    
    if st.session_state.lists:
        selected_list = st.selectbox("Selecione uma lista para ver detalhes:", list(st.session_state.lists.keys()))
        
        items = st.session_state.lists[selected_list]
        df = pd.DataFrame(items)
        st.table(df[['name', 'price', 'market']])
        
        total = df['price'].sum()
        st.subheader(f"Total Estimado: R$ {total:.2f}")
        
        # Exportação
        export_text = f"Lista: {selected_list}\n" + "="*20 + "\n"
        for item in items:
            export_text += f"- {item['name']}: R$ {item['price']:.2f} ({item['market']})\n"
        export_text += "="*20 + f"\nTOTAL: R$ {total:.2f}"
        
        st.download_button("Exportar Lista (TXT)", export_text, file_name=f"{selected_list}.txt")
        
        if st.button("Excluir esta lista"):
            del st.session_state.lists[selected_list]
            st.rerun()
    else:
        st.write("Você ainda não salvou nenhuma lista.")

# --- SEÇÃO: MODO COMPRAS ---
elif menu == "Modo Compras":
    st.header("🛒 Modo Compras")
    st.write("Marque os itens enquanto coloca no carrinho.")
    
    if st.session_state.lists:
        selected_list = st.selectbox("Qual lista você está usando agora?", list(st.session_state.lists.keys()))
        items = st.session_state.lists[selected_list]
        
        # Barra de Progresso
        checked_count = sum(1 for item in items if item['checked'])
        total_count = len(items)
        progress = checked_count / total_count if total_count > 0 else 0
        
        st.progress(progress)
        st.write(f"Progresso: {checked_count} de {total_count} itens ({int(progress*100)}%)")
        
        # Lista com Checkboxes
        for i, item in enumerate(items):
            is_checked = st.checkbox(f"{item['name']} - R$ {item['price']:.2f} ({item['market']})", value=item['checked'], key=f"check_{i}")
            if is_checked != item['checked']:
                st.session_state.lists[selected_list][i]['checked'] = is_checked
                st.rerun()
                
        if progress == 1.0:
            st.balloons()
            st.success("Compra finalizada! Tudo no carrinho.")
    else:
        st.warning("Crie e salve uma lista primeiro!")

# Rodapé
st.sidebar.divider()
st.sidebar.caption("SmartMarket App v1.0 - Desenvolvido em Python")
