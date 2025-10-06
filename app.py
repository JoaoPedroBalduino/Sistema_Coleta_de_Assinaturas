# app.py - Arquivo principal com Login e novas funcionalidades
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Configurações e dados
from config import SUPABASE_CONFIG, MUNICIPIOS, COLETORES, USUARIOS_LOGIN
from crud_operations import CRUDOperations

# Configuração do Supabase
supabase: Client = create_client(SUPABASE_CONFIG["url"], SUPABASE_CONFIG["key"])
crud = CRUDOperations(supabase)

st.set_page_config(page_title="Sistema de Coleta de Assinaturas", page_icon="📝", layout="wide")

# SISTEMA DE LOGIN ============================================================================

def tela_login():
    st.title("Login - Sistema de Coleta de Assinaturas")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Entre com suas credenciais")
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            login_button = st.form_submit_button("Entrar", use_container_width=True)
        
        if login_button:
            if username in USUARIOS_LOGIN and USUARIOS_LOGIN[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos!")
        
        st.markdown("---")
        st.info("🔍 **Usuários de teste:**\n- admin / admin123\n- coletor / coletor123\n- supervisor / super123")

def logout():
    """Função para fazer logout"""
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# FICHA VIRTUAL ============================================================================

def tela_ficha_virtual():
    st.header("🎫 Ficha Virtual de Assinatura")
    
    # Buscar todas as assinaturas para popular o selectbox
    df_todas = crud.read_assinaturas()
    
    if df_todas is not None and not df_todas.empty:
        col1, col2 = st.columns(2)
        with col1:
            search_type = st.radio("Buscar por:", ["Nome Completo", "Título de Eleitor"])
        
        with col2:
            if search_type == "Nome Completo":
                # Lista de nomes para seleção
                nomes_opcoes = df_todas['nome_completo'].unique().tolist()
                nomes_opcoes.sort()  # Ordenar alfabeticamente
                selected_nome = st.selectbox("Selecione o nome:", nomes_opcoes)
                search_value = selected_nome
            else:
                # Lista de títulos para seleção
                titulos_opcoes = df_todas['titulo_eleitor'].unique().tolist()
                titulos_opcoes.sort()
                selected_titulo = st.selectbox("Selecione o título:", titulos_opcoes)
                search_value = selected_titulo
        
        if st.button("🔍 Buscar Ficha"):
            if search_type == "Nome Completo":
                registros_encontrados = df_todas[df_todas['nome_completo'] == search_value]
            else:
                registros_encontrados = df_todas[df_todas['titulo_eleitor'] == search_value]
            
            if not registros_encontrados.empty:
                registro = registros_encontrados.iloc[0].to_dict()
                st.success("Ficha encontrada!")
                
                # Ficha virtual em markdown formal
                st.markdown("---")
                
                # Cabeçalho
                st.markdown("""
                <div style='text-align: center; padding: 20px; border-bottom: 2px solid #1f77b4; margin-bottom: 30px;'>
                    <h1 style='color: #1f77b4; margin: 0;'>FICHA DE ASSINATURA ELEITORAL</h1>
                    <p style='color: #666; margin: 5px 0 0 0;'>Sistema de Coleta de Assinaturas - Documento Oficial</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Seções da ficha
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### IDENTIFICAÇÃO PESSOAL")
                    st.markdown(f"**Nome Completo:** {registro['nome_completo']}")
                    st.markdown(f"**Nome da Mãe:** {registro['nome_mae']}")
                    
                    st.markdown("### DADOS ELEITORAIS")
                    st.markdown(f"**Título de Eleitor:** {registro['titulo_eleitor']}")
                    st.markdown(f"**Zona Eleitoral:** {registro['zona_eleitoral']}")
                    st.markdown(f"**Seção Eleitoral:** {registro['secao_eleitoral']}")
                
                with col2:
                    st.markdown("### LOCALIZAÇÃO")
                    st.markdown(f"**Município:** {registro.get('municipio', 'Não informado')}")
                    st.markdown(f"**Estado:** {registro.get('municipio_uf', 'Não informado')}")
                    
                    st.markdown("### DADOS DA COLETA")
                    st.markdown(f"**Coletor Responsável:** {registro.get('coletor', 'Não informado')}")
                    st.markdown(f"**Data da Assinatura:** {registro['data_assinatura']}")
                    st.markdown(f"**ID do Registro:** #{registro['id']}")
                
                # Observações (se existir)
                if registro.get('observacoes'):
                    st.markdown("### OBSERVAÇÕES")
                    st.markdown(f"{registro['observacoes']}")
                
                # Instruções
                st.markdown("---")
                st.info("**Instruções:** Use Ctrl+P para imprimir esta ficha ou Ctrl+S para salvar como PDF")
            
            else:
                st.error("Registro não encontrado!")
    else:
        st.info("Nenhuma assinatura cadastrada ainda.")

# RELATÓRIOS E DASHBOARD ============================================================================

def tela_relatorios():
    st.header("📊 Relatórios e Dashboard")
    
    # Métricas principais
    total_assinaturas = crud.get_total_registros()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Total de Assinaturas", total_assinaturas)
    
    with col2:
        df_municipios = crud.get_assinaturas_por_municipio()
        if df_municipios is not None and not df_municipios.empty:
            total_municipios = len(df_municipios)
            st.metric("🏢 Municípios Ativos", total_municipios)
        else:
            st.metric("🏢 Municípios Ativos", 0)
    
    with col3:
        df_coletores = crud.get_coletores()
        if df_coletores is not None and not df_coletores.empty:
            total_coletores = len(df_coletores)
            st.metric("👥 Coletores Cadastrados", total_coletores)
        else:
            st.metric("👥 Coletores Cadastrados", 0)
    
    st.markdown("---")
    
    # Relatório de Assinaturas por Município
    st.subheader("🏢 Assinaturas por Município")
    
    df_municipios = crud.get_assinaturas_por_municipio()
    if df_municipios is not None and not df_municipios.empty:
        # Verificar se temos dados suficientes para o gráfico
        if len(df_municipios) > 0:
            # Gráfico de barras - usando só as colunas que existem
            municipios_para_grafico = df_municipios.head(15)
            
            # Verificar se a coluna 'estado' existe para colorir o gráfico
            if 'estado' in municipios_para_grafico.columns:
                fig = px.bar(
                    municipios_para_grafico, 
                    x='municipio', 
                    y='total_assinaturas',
                    color='estado',
                    title="Top 15 Municípios com Mais Assinaturas",
                    labels={'total_assinaturas': 'Total de Assinaturas', 'municipio': 'Município'}
                )
            else:
                fig = px.bar(
                    municipios_para_grafico, 
                    x='municipio', 
                    y='total_assinaturas',
                    title="Top 15 Municípios com Mais Assinaturas",
                    labels={'total_assinaturas': 'Total de Assinaturas', 'municipio': 'Município'}
                )
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 Nenhum dado disponível para gráfico.")
        
        # Tabela detalhada
        st.subheader("📋 Tabela Detalhada por Estado")
        df_display = df_municipios.copy()
        
        # Ajustar colunas baseado no que realmente existe na view
        if 'regiao' in df_display.columns and 'populacao' in df_display.columns:
            df_display = df_display[['municipio_id', 'municipio', 'estado', 'regiao', 'total_assinaturas']]
            df_display.columns = ['ID', 'Município', 'Estado', 'Região', 'Total de Assinaturas']
        else:
            # Fallback para estrutura básica
            df_display = df_display[['municipio_id', 'municipio', 'estado', 'total_assinaturas']]
            df_display.columns = ['ID', 'Município', 'Estado', 'Total de Assinaturas']
        
        st.dataframe(df_display, use_container_width=True)
        
        # Download CSV
        csv = df_municipios.to_csv(index=False)
        st.download_button(
            label="📥 Baixar Relatório CSV",
            data=csv,
            file_name=f"relatorio_municipios_{date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("📭 Nenhum dado de município encontrado.")
    
    st.markdown("---")
    
    # Relatório de Performance dos Coletores
    st.subheader("👥 Performance dos Coletores")
    
    df_coletores = crud.get_coletores()
    if df_coletores is not None and not df_coletores.empty:
        coletores_performance = []
        
        for _, coletor in df_coletores.iterrows():
            total = crud.get_total_assinaturas_coletor(coletor['id'])
            coletores_performance.append({
                'Nome': coletor['nome'],
                'ID': coletor['id'],
                'Total de Assinaturas': total
            })
        
        df_performance = pd.DataFrame(coletores_performance)
        df_performance = df_performance.sort_values('Total de Assinaturas', ascending=False)
        
        # Gráfico de pizza
        fig_pie = px.pie(
            df_performance, 
            values='Total de Assinaturas', 
            names='Nome',
            title="Distribuição de Assinaturas por Coletor"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tabela de performance
        st.dataframe(df_performance, use_container_width=True)
    else:
        st.info("📭 Nenhum dado de coletor encontrado.")

# PÁGINA PRINCIPAL COM MENU ============================================================================

def main_app():
    st.title("📝 Sistema de Coleta de Assinaturas")
    
    # Mostrar usuário logado e botão de logout
    st.sidebar.markdown(f"👤 **Usuário:** {st.session_state.username}")
    logout()
    
    # Menu de navegação
    menu = st.sidebar.selectbox("Escolha uma operação:", 
                                ["🏠 Dashboard", "➕ Cadastrar Assinatura", "📋 Listar Assinaturas", 
                                "✏️ Editar Assinatura", "🗑️ Deletar Assinatura", "🎫 Ficha Virtual", 
                                "📊 Relatórios"])
    
    # DASHBOARD ============================================================================
    
    if menu == "🏠 Dashboard":
        st.header("🏠 Dashboard Principal")
        
        # Métricas rápidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = crud.get_total_registros()
            st.metric("📝 Total Assinaturas", total)
        
        with col2:
            df_hoje = crud.read_assinaturas()
            if df_hoje is not None and not df_hoje.empty:
                hoje = str(date.today())
                total_hoje = len(df_hoje[df_hoje['data_assinatura'] == hoje])
                st.metric("📅 Hoje", total_hoje)
            else:
                st.metric("📅 Hoje", 0)
        
        with col3:
            df_municipios = crud.get_assinaturas_por_municipio()
            if df_municipios is not None and not df_municipios.empty:
                st.metric("🏢 Municípios", len(df_municipios))
            else:
                st.metric("🏢 Municípios", 0)
        
        with col4:
            df_coletores = crud.get_coletores()
            if df_coletores is not None and not df_coletores.empty:
                st.metric("👥 Coletores", len(df_coletores))
            else:
                st.metric("👥 Coletores", 0)
        
        st.markdown("---")
        st.info("👈 Use o menu lateral para navegar pelas funcionalidades do sistema.")
    
    
    # CADASTRAR ASSINATURA ============================================================================
    
    elif menu == "➕ Cadastrar Assinatura":
        st.header("➕ Cadastrar Nova Assinatura")
        
        with st.form("assinatura_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_completo = st.text_input("Nome completo *")
                nome_mae = st.text_input("Nome da mãe *")
                titulo_eleitor = st.text_input("Título de Eleitor (12 dígitos) *", max_chars=12)
                zona_eleitoral = st.number_input("Zona Eleitoral *", min_value=1, value=1)
                secao_eleitoral = st.number_input("Seção Eleitoral *", min_value=1, value=1)
            
            with col2:
                municipio = st.selectbox("Município *", options=list(MUNICIPIOS.keys()))
                coletor = st.selectbox("Coletor *", options=list(COLETORES.keys()))
                data_assinatura = st.date_input("Data da assinatura", value=date.today())
                observacoes = st.text_area("Observações")
            
            enviado = st.form_submit_button("💾 Salvar Assinatura", use_container_width=True)

        if enviado:
            # Validações básicas
            if not nome_completo or not nome_mae or not titulo_eleitor:
                st.error("❌ Preencha todos os campos obrigatórios!")
            elif len(titulo_eleitor) != 12 or not titulo_eleitor.isdigit():
                st.error("❌ Título de eleitor deve ter exatamente 12 dígitos!")
            else:
                data = {
                    "nome_completo": nome_completo,
                    "nome_mae": nome_mae,
                    "titulo_eleitor": titulo_eleitor,
                    "zona_eleitoral": zona_eleitoral,
                    "secao_eleitoral": secao_eleitoral,
                    "municipio": municipio,
                    "municipio_uf": MUNICIPIOS[municipio],
                    "coletor": coletor,
                    "coletor_id": COLETORES[coletor],
                    "data_assinatura": str(data_assinatura),
                    "observacoes": observacoes,
                }
                
                success, message = crud.create_assinatura(data)
                if success:
                    st.success("✅ Assinatura cadastrada com sucesso!")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")

    # LISTAR ASSINATURAS ============================================================================
    
    elif menu == "📋 Listar Assinaturas":
        st.header("📋 Lista de Assinaturas")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_nome = st.text_input("🔍 Filtrar por nome:")
        with col2:
            filtro_municipio = st.selectbox("🔍 Filtrar por município:", 
                                           options=["Todos"] + list(MUNICIPIOS.keys()))
        with col3:
            filtro_zona = st.number_input("🔍 Filtrar por zona:", min_value=0, value=0)
        
        # Buscar e filtrar dados
        df_filtrado = crud.read_assinaturas(filtro_nome, filtro_municipio, filtro_zona)
        
        if df_filtrado is not None and not df_filtrado.empty:
            st.info(f"📊 Total de registros encontrados: {len(df_filtrado)}")
            
            # Exibir tabela organizada
            colunas_exibir = ['nome_completo', 'titulo_eleitor', 'municipio', 'zona_eleitoral', 
                             'secao_eleitoral', 'coletor', 'data_assinatura']
            df_display = df_filtrado[colunas_exibir].copy()
            df_display.columns = ['Nome Completo', 'Título', 'Município', 'Zona', 'Seção', 'Coletor', 'Data']
            
            st.dataframe(df_display, use_container_width=True)
            
            # Download CSV
            csv = df_filtrado.to_csv(index=False)
            st.download_button(
                label="📥 Baixar dados em CSV",
                data=csv,
                file_name=f"assinaturas_{date.today()}.csv",
                mime="text/csv"
            )
        elif df_filtrado is not None:
            st.warning("🔍 Nenhum registro encontrado com os filtros aplicados.")
        else:
            st.error("❌ Erro ao carregar dados.")

    # EDITAR ASSINATURA ============================================================================
    
    elif menu == "✏️ Editar Assinatura":
        st.header("✏️ Editar Assinatura")
        
        df_todos = crud.read_assinaturas()
        
        if df_todos is not None and not df_todos.empty:
            # Selectbox para escolher o registro
            opcoes = [f"{row['nome_completo']} - {row['titulo_eleitor']} ({row.get('municipio', 'N/A')})" 
                     for _, row in df_todos.iterrows()]
            indice_selecionado = st.selectbox("Selecione a assinatura para editar:", 
                                            range(len(opcoes)), format_func=lambda x: opcoes[x])
            
            if st.button("🔄 Carregar dados para edição"):
                registro = df_todos.iloc[indice_selecionado]
                st.session_state.registro_edicao = registro
            
            # Formulário de edição
            if 'registro_edicao' in st.session_state:
                registro = st.session_state.registro_edicao
                
                with st.form("edicao_form"):
                    st.subheader(f"Editando: {registro['nome_completo']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nome_completo = st.text_input("Nome completo", value=registro['nome_completo'])
                        nome_mae = st.text_input("Nome da mãe", value=registro['nome_mae'])
                        titulo_eleitor = st.text_input("Título de Eleitor", value=registro['titulo_eleitor'], max_chars=12)
                        zona_eleitoral = st.number_input("Zona Eleitoral", value=int(registro['zona_eleitoral']))
                        secao_eleitoral = st.number_input("Seção Eleitoral", value=int(registro['secao_eleitoral']))
                    
                    with col2:
                        # Encontrar índice do município atual
                        municipio_atual = registro.get('municipio', list(MUNICIPIOS.keys())[0])
                        if municipio_atual in MUNICIPIOS:
                            municipio_index = list(MUNICIPIOS.keys()).index(municipio_atual)
                        else:
                            municipio_index = 0
                        
                        municipio = st.selectbox("Município", options=list(MUNICIPIOS.keys()), index=municipio_index)
                        
                        # Encontrar índice do coletor atual
                        coletor_atual = registro.get('coletor', list(COLETORES.keys())[0])
                        if coletor_atual in COLETORES:
                            coletor_index = list(COLETORES.keys()).index(coletor_atual)
                        else:
                            coletor_index = 0
                        
                        coletor = st.selectbox("Coletor", options=list(COLETORES.keys()), index=coletor_index)
                        data_assinatura = st.date_input("Data da assinatura", value=pd.to_datetime(registro['data_assinatura']).date())
                        observacoes = st.text_area("Observações", value=registro.get('observacoes', ''))
                    
                    atualizar = st.form_submit_button("💾 Atualizar Registro", use_container_width=True)
                
                if atualizar:
                    data_atualizada = {
                        "nome_completo": nome_completo,
                        "nome_mae": nome_mae,
                        "titulo_eleitor": titulo_eleitor,
                        "zona_eleitoral": zona_eleitoral,
                        "secao_eleitoral": secao_eleitoral,
                        "municipio": municipio,
                        "municipio_uf": MUNICIPIOS[municipio],
                        "coletor": coletor,
                        "coletor_id": COLETORES[coletor],
                        "data_assinatura": str(data_assinatura),
                        "observacoes": observacoes,
                    }
                    
                    success, message = crud.update_assinatura(registro['id'], data_atualizada)
                    if success:
                        st.success("✅ Registro atualizado com sucesso!")
                        del st.session_state.registro_edicao
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        else:
            st.info("📭 Nenhuma assinatura cadastrada para edição.")

    # DELETE - Deletar assinatura ============================================================================
    
    elif menu == "🗑️ Deletar Assinatura":
        st.header("🗑️ Deletar Assinatura")
        st.warning("⚠️ Esta ação não pode ser desfeita!")
        
        df_todos = crud.read_assinaturas()
        
        if df_todos is not None and not df_todos.empty:
            # Selectbox para escolher o registro
            opcoes = [f"{row['nome_completo']} - {row['titulo_eleitor']} ({row.get('municipio', 'N/A')})" 
                     for _, row in df_todos.iterrows()]
            indice_selecionado = st.selectbox("Selecione a assinatura para deletar:", 
                                            range(len(opcoes)), format_func=lambda x: opcoes[x])
            
            # Mostrar detalhes do registro selecionado 
            registro = df_todos.iloc[indice_selecionado]
            
            with st.expander("👁️ Visualizar detalhes do registro"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text(f"Nome: {registro['nome_completo']}")
                    st.text(f"Nome da Mãe: {registro['nome_mae']}")
                    st.text(f"Título: {registro['titulo_eleitor']}")
                    st.text(f"Zona: {registro['zona_eleitoral']}")
                with col2:
                    st.text(f"Seção: {registro['secao_eleitoral']}")
                    st.text(f"Município: {registro.get('municipio', 'N/A')}")
                    st.text(f"Coletor: {registro.get('coletor', 'N/A')}")
                    st.text(f"Data: {registro['data_assinatura']}")
            
            # Confirmação de exclusão 
            confirmar = st.checkbox("✅ Confirmo que desejo deletar este registro")
            
            if confirmar:
                if st.button("🗑️ DELETAR REGISTRO", type="primary"):
                    success, message = crud.delete_assinatura(registro['id'])
                    if success:
                        st.success("✅ Registro deletado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        else:
            st.info("📭 Nenhuma assinatura cadastrada para deletar.")
    
    # FICHA VIRTUAL ============================================================================
    elif menu == "🎫 Ficha Virtual":
        tela_ficha_virtual()
    
    # RELATÓRIOS ============================================================================
    elif menu == "📊 Relatórios":
        tela_relatorios()

    # 📊 Footer com estatísticas
    st.sidebar.markdown("---")
    total_registros = crud.get_total_registros()
    st.sidebar.metric("📊 Total de Assinaturas", total_registros)

# CONTROLE PRINCIPAL DA APLICAÇÃO ============================================================================
if __name__ == "__main__":
    # Inicializar session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
    
    # Verificar se está logado
    if not st.session_state.logged_in:
        tela_login()
    else:
        main_app()