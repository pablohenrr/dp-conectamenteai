import streamlit as st

def setup_sidebar():
    caminho_imagem = "assets/photos/conectamenteperfil.png"
    
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    
    sidebar_style = """
    <style>
    /* Estilizando apenas a sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        padding: 20px;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
        text-align: center; 
        color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
    }
    /* Estilizando apenas os elementos dentro da sidebar */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] figcaption {
        color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #00bcd4; 
        color: #FFFFFF;
        padding: 10px 20px;
        border-radius: 25px;
        border: none;
        cursor: pointer;
        margin-top: 10px;
        font-weight: bold;
        text-transform: uppercase;
        transition: background-color 0.3s ease;
        font-family: 'Roboto', sans-serif;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #008ba3; 
    }
    [data-testid="stSidebar"] hr {
        border: 1px solid #FFFFFF;
    }
    /* Estilização do rodapé */
    [data-testid="stSidebar"] .sidebar-footer {
        position: fixed;
        bottom: 20px;
        left: 10px;
        right: 10px;
        text-align: center;
        font-size: 12px;
        color: #FFFFFF; /* Mantendo a cor branca do rodapé na sidebar */
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """
    
    global_style = """
    <style>
    /* Ajusta a cor do texto fora da sidebar para garantir que o rodapé fora da sidebar não seja afetado */
    .sidebar-footer-outside {
        font-size: 12px;
        color: black !important; /* Cor preta para rodapé fora da sidebar */
        font-family: inherit; /* Fonte padrão do Streamlit */
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """
    
    st.markdown(sidebar_style, unsafe_allow_html=True)
    
    st.markdown(global_style, unsafe_allow_html=True)
    
    with st.sidebar:
        st.image(caminho_imagem, use_column_width=True)
        st.markdown("<h3>Chatbot de Saúde Mental & Bem-Estar</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p>Desenvolvido por <a href='https://www.linkedin.com/in/pablo-henrique-de-souza-a48125239/' style='color:#00bcd4; text-decoration: none;'>Pablo Henrique de Souza (CEO)</a></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("<h4>Funcionalidades:</h4>", unsafe_allow_html=True)
        if st.button("🧹 Limpar Conversa", key="clear_history"):
            initial_message = {"role": "assistant", "content": "Olá! 👋 Sou o ConectaMenteAI, estou aqui para te ajudar a cuidar do seu bem-estar emocional. Como está se sentindo hoje? 🤔"}
            st.session_state["messages"] = [initial_message]
            st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("ℹ️ Sobre o Chatbot"):
            st.write("O ConectaMenteAI é um chatbot desenvolvido para fornecer suporte emocional e informações sobre saúde mental e bem-estar.")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("📚 Recursos"):
            st.write("Explore nossos recursos para aprender mais sobre saúde mental, incluindo artigos, dicas e guias práticos.")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h4>Contato:</h4>", unsafe_allow_html=True)
        st.markdown("Entre em contato conosco:")
        st.markdown("<a href='mailto:contato@conectamenteai.com' style='color:#00bcd4; text-decoration: none;'>Envie um e-mail</a>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-footer'>ConectaMenteAI - Todos os direitos reservados</div>", unsafe_allow_html=True)