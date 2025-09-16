import time
import os
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from modules.pdf_processor import process_pdf
from modules.chat import search_with_embeddings, create_embeddings
from modules.sidebar import setup_sidebar
from config import PDF_PATHS
import google.generativeai as genai
import dotenv

def main():
    st.set_page_config(
        page_title="ConectaMenteAI",
        page_icon="🧠",
        layout="wide",
    )

    setup_sidebar()

    dotenv.load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        st.error("A chave da API do Google não foi encontrada. Verifique suas variáveis de ambiente.")
        return

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    @st.cache_data(show_spinner=False)
    def load_and_process_pdfs(pdf_paths):
        all_text_segments = []
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_pdf, pdf_paths))
            for text_segments in results:
                all_text_segments.extend(text_segments)
        return all_text_segments

    all_text_segments = load_and_process_pdfs(PDF_PATHS)
    vectorizer, embeddings = create_embeddings(all_text_segments)

    if 'pdf_processed' not in st.session_state:
        st.session_state['pdf_processed'] = False

    st.title("🧠 ConectaMenteAI - Chatbot de Saúde Mental & Bem-Estar")

    initial_message = {"role": "assistant", "content": "Olá! 👋 Sou o ConectaMenteAI, estou aqui para te ajudar a cuidar do seu bem-estar emocional. Como está se sentindo hoje? 🤔"}

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["messages"].append(initial_message)

    if not st.session_state['pdf_processed']:
        with st.spinner("Por favor, aguarde enquanto o ConectaMenteAI processa o documento para você... 🧠"):
            all_text_segments = load_and_process_pdfs(PDF_PATHS)
            vectorizer, embeddings = create_embeddings(all_text_segments)
            st.session_state['pdf_processed'] = True

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Mensagem para ConectaMenteAI"):
        user_message = {"role": "user", "content": f"Você: {prompt}"}
        st.session_state.messages.append(user_message)
        
        with st.chat_message("human"):
            st.write(user_message["content"])

        with st.spinner("Processando sua pergunta..."):
            time.sleep(2)  

            try:
                best_match_index, best_match_segment = search_with_embeddings(
                    prompt, vectorizer, embeddings, all_text_segments
                )

                contextualized_prompt = (
                    f"Pergunta do usuário: {prompt}\n\nContexto do PDF: {best_match_segment}\n\nResposta:"
                )

                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                "Você deve agir da seguinte forma a seguir:\nVocê é o ConectaMenteAI, um chatbot dedicado a conversas sobre saúde mental e bem-estar. Você **nunca deve fugir do contexto lidos**. **Nunca invente informações.** Se não souber a resposta, diga que não a encontrou na sua base de dados. Seu objetivo é oferecer apoio, escuta sem julgamentos e informações relevantes sobre o tema, incentivando o usuário a se abrir e compartilhar seus sentimentos. \
                                \
                                Lembre-se sempre de: \
                                \
                                * **Sempre que o usuário perguntar quem é o seu criador, você responderá que é o Pablo Henrique de Souza (CEO) da ConectaMenteAI da cidade de Matão e ele tem 21 anos de idade** \
                                * **Sempre que o usuário introduzir a conversa com você, cumprimente-o e pergunte como ele está:** Mostre que você está disponível para ouvi-lo. \
                                * **Em nenhuma ocasião fale que não encontrou no texto fornecido:** Se não souber a resposta, diga que não a encontrou na sua base de dados. \
                                * **Estamos em 2024:** Sempre que possível, utilize exemplos e situações atuais para contextualizar a conversa. \
                                * **Quando o usuário perguntar do por que escolher você ao invés do ChatGPT:** Diga que você é especializado em saúde mental e bem-estar, e que o ChatGPT é um chatbot mais generalista. \
                                * **Oferecer apoio e empatia:** Mostre ao usuário que você o escuta e se importa com seus sentimentos. Use frases acolhedoras como 'Compreendo como se sente', 'É natural se sentir assim em momentos difíceis',  e evite julgamentos. \
                                * **Não fornecer diagnósticos ou conselhos médicos/psicológicos:**  Você não é um profissional da saúde. Frases como 'Não posso te dizer o que você tem', 'Para receber o tratamento adequado, o ideal é procurar ajuda profissional' são importantes. Indique sempre a busca por ajuda profissional quando necessário. \
                                * **Fornecer informações precisas e confiáveis:** Baseie suas respostas em fontes confiáveis e evite propagar informações falsas. \
                                * **Manter uma linguagem acolhedora, respeitosa e clara:** Utilize linguagem acessível e evite jargões técnicos. \
                                * **Incentivar a conversa:** Faça perguntas abertas como 'Gostaria de compartilhar mais sobre como se sente?', 'O que te leva a pensar isso?' e explore os sentimentos do usuário. \
                                * **Oferecer recursos de apoio:** Indique linhas de apoio, sites e aplicativos de saúde mental, sempre ressaltando que são recursos complementares e que a ajuda profissional é fundamental. \
                                * **Sempre utilize números de telefones nacionais e sites de instituições confiáveis: Evite fornecer números de telefones internacionais ou de instituições desconhecidas. \
                                \
                                **É fundamental que você deixe claro que não substitui a ajuda de um profissional.**",
                            ],
                        },
                        {
                            "role": "model",
                            "parts": [
                                "Olá! 👋 Sou o ConectaMenteAI, estou aqui para te ajudar a cuidar do seu bem-estar emocional. O que você gostaria de saber sobre saúde mental? 🤔",
                            ],
                        }
                    ] 
                )

                response = chat_session.send_message(contextualized_prompt)
                answer = response.text
                bot_message = {"role": "assistant", "content": f"Bot: {answer}"}

                st.session_state["messages"].append(bot_message)

                with st.chat_message("ai"):
                    st.write(bot_message["content"])

            except Exception as e:
                st.error(f"Erro na API Gemini: {e}")

if __name__ == "__main__":
    main()