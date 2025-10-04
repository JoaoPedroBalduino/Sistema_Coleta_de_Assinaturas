# crud_operations.py - Operações CRUD e Relatórios

import pandas as pd

class CRUDOperations:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.table_name = "eleitor_assinatura"
    
    def create_assinatura(self, data):
        """Criar nova assinatura"""
        try:
            response = self.supabase.table(self.table_name).insert(data).execute()
            if response.data:
                return True, "Assinatura cadastrada com sucesso!"
            else:
                return False, "Erro ao cadastrar assinatura."
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def read_assinaturas(self, filtro_nome=None, filtro_municipio=None, filtro_zona=None):
        """Ler assinaturas com filtros opcionais"""
        try:
            response = self.supabase.table(self.table_name).select("*").execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                
                # Aplicar filtros
                if filtro_nome:
                    df = df[df['nome_completo'].str.contains(filtro_nome, case=False, na=False)]
                
                if filtro_municipio and filtro_municipio != "Todos":
                    df = df[df['municipio'] == filtro_municipio]
                
                if filtro_zona and filtro_zona > 0:
                    df = df[df['zona_eleitoral'] == filtro_zona]
                
                return df
            else:
                return pd.DataFrame()  # DataFrame vazio
                
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return None
    
    def update_assinatura(self, registro_id, data):
        """Atualizar assinatura existente"""
        try:
            response = self.supabase.table(self.table_name).update(data).eq("id", registro_id).execute()
            if response.data:
                return True, "Registro atualizado com sucesso!"
            else:
                return False, "Erro ao atualizar registro."
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def delete_assinatura(self, registro_id):
        """Deletar assinatura"""
        try:
            response = self.supabase.table(self.table_name).delete().eq("id", registro_id).execute()
            if response.data:
                return True, "Registro deletado com sucesso!"
            else:
                return False, "Erro ao deletar registro."
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def get_total_registros(self):
        """Obter total de registros"""
        try:
            response = self.supabase.table(self.table_name).select("id", count="exact").execute()
            return response.count if response.count else 0
        except:
            return "N/A"
    
    def get_assinatura_by_id(self, assinatura_id):
        """Buscar assinatura específica por ID"""
        try:
            response = self.supabase.table(self.table_name).select("*").eq("id", assinatura_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Erro ao buscar assinatura: {str(e)}")
            return None
    
    def validar_login(self, username, password):
        """Validar login de usuário"""
        try:
            response = self.supabase.table("usuarios").select("*").eq("username", username).eq("password", password).execute()
            if response.data:
                return True, response.data[0]
            return False, None
        except Exception as e:
            print(f"Erro no login: {str(e)}")
            return False, None
    
    def get_assinaturas_por_municipio(self):
        """Buscar dados da view vw_assinaturas_por_municipio"""
        try:
            response = self.supabase.table("vw_assinaturas_por_municipio").select("*").execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Erro ao carregar relatório por município: {str(e)}")
            return None
    
    def get_total_assinaturas_coletor(self, coletor_id):
        """Chamar função fn_total_assinaturas_coletor"""
        try:
            response = self.supabase.rpc("fn_total_assinaturas_coletor", {"p_coletor_id": coletor_id}).execute()
            if response.data is not None:
                return response.data
            return 0
        except Exception as e:
            print(f"Erro ao buscar total do coletor: {str(e)}")
            return 0
    
    def get_coletores(self):
        """Buscar lista de coletores da tabela"""
        try:
            response = self.supabase.table("coletor").select("*").execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Erro ao carregar coletores: {str(e)}")
            return None