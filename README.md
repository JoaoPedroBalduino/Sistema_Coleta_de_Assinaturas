# 📝 Sistema de Coleta de Assinaturas

Aplicação web desenvolvida em **Python + Streamlit**, integrada ao **Supabase**, para gerenciar a coleta de assinaturas de eleitores.
O sistema permite **cadastrar, listar, editar, excluir, consultar fichas virtuais e gerar relatórios** detalhados.

---

## 🌐 Acesso Online

Acesse o sistema online: [Clique aqui](https://cxz9k47hrtgciljhaav8nk.streamlit.app/)

---

## 🎥 Vídeo Explicativo

Assista ao vídeo no YouTube explicando o projeto:  
[![Miniatura do Vídeo](https://img.youtube.com/vi/KGwS9bf6dFI/0.jpg)](https://www.youtube.com/watch?v=KGwS9bf6dFI&t=95s)

**CLIQUE NA IMAGEM**

---

## 🚀 Funcionalidades

* 🔐 **Login de Usuário** (Admin, Coletor, Supervisor)
* ➕ **Cadastro de Assinaturas**
* 📋 **Listagem com filtros** (nome, município, zona eleitoral)
* ✏️ **Edição de registros**
* 🗑️ **Exclusão de registros**
* 🎫 **Ficha Virtual** de cada eleitor
* 📊 **Dashboard** com métricas rápidas
* 📈 **Relatórios e gráficos** (Plotly)
* 📥 **Exportação CSV** de dados e relatórios

---

## 📂 Estrutura do Projeto

```
.
├── app.py                # Arquivo principal com Streamlit
├── config.py             # Configurações (Supabase, usuários, municípios e coletores)
├── crud_operations.py    # Classe CRUD com operações no Supabase
├── requirements.txt      # Dependências do projeto
└── docs/
    └── der.png           # Diagrama Entidade-Relacionamento
```

---

## 🗃️ Modelo Entidade-Relacionamento (DER)

![DER do Sistema](https://raw.githubusercontent.com/JoaoPedroBalduino/Sistema_Coleta_de_Assinaturas/refs/heads/main/Modelo%20de%20Relacionamento.png)

---

## ⚙️ Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Supabase](https://supabase.com/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly](https://plotly.com/python/)

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

> **Exemplo de `requirements.txt`:**
>
> ```
> streamlit
> supabase
> pandas
> plotly
> ```

---

## ▶️ Execução

Inicie o servidor local:

```bash
streamlit run app.py
```

Acesse no navegador:
👉 `http://localhost:8501`

---

## 🔑 Login de Teste

| Usuário    | Senha      | Perfil        |
| ---------- | ---------- | ------------- |
| admin      | admin123   | Administrador |
| coletor    | coletor123 | Coletor       |
| supervisor | super123   | Supervisor    |

---

## 📊 Banco de Dados

O sistema utiliza o **Supabase (PostgreSQL)** com as seguintes tabelas:

* `usuarios` → controle de login
* `municipio` → municípios disponíveis
* `coletor` → coletores de assinaturas
* `eleitor_assinatura` → registros de assinaturas coletadas
* View: `vw_assinaturas_por_municipio`
* Funções: `fn_total_assinaturas_coletor`, `fn_estatisticas_coletor`

---

## 🤝 Contribuições

1. Faça um **fork** do projeto
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commit suas alterações (`git commit -m 'Adicionei minha feature'`)
4. Envie para o repositório remoto (`git push origin feature/minha-feature`)
5. Abra um **Pull Request** 🎉

---

## 📜 Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir.
