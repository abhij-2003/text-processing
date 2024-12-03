import streamlit as st
from config import (
    GOOGLE_API_KEY, PAGE_TITLE, PAGE_ICON, 
    LAYOUT, SUPPORTED_FILE_TYPES
)
from services.chat_service import ChatService
from services.sentiment_service import SentimentService
from services.topic_service import TopicService
from services.paraphrase_service import ParaphraseService
from utils.file_handler import FileHandler

def init_session_state():
    """Initialize session state variables"""
    if "chat_service" not in st.session_state:
        st.session_state.chat_service = ChatService(GOOGLE_API_KEY)
    if "sentiment_service" not in st.session_state:
        st.session_state.sentiment_service = SentimentService()
    if "topic_service" not in st.session_state:
        st.session_state.topic_service = TopicService()
    if "paraphrase_service" not in st.session_state:
        st.session_state.paraphrase_service = ParaphraseService(GOOGLE_API_KEY)
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Chat"

def display_chat_interface():
    """Display chat interface"""
    st.subheader("💬 Chat Interface")
    
    # Display chat history
    for message in st.session_state.chat_service.get_history():
        role = "assistant" if message.role == "model" else message.role
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Chat input
    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        response = st.session_state.chat_service.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)

def display_sentiment_interface():
    """Display sentiment analysis interface"""
    st.subheader("📊 Sentiment Analysis")
    
    # Input section
    text_input = st.text_area("Enter text for sentiment analysis", height=100)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("Analyze Sentiment")
    with col2:
        if st.session_state.sentiment_service.results:
            clear_button = st.button("Clear History")
            if clear_button:
                st.session_state.sentiment_service = SentimentService()
                st.rerun()
    
    if analyze_button and text_input:
        result = st.session_state.sentiment_service.analyze_sentiment(text_input)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sentiment", result['Sentiment'])
        with col2:
            st.metric("Polarity", f"{result['Polarity']:.2f}")
        with col3:
            st.metric("Subjectivity", f"{result['Subjectivity']:.2f}")
        
        # Display analysis explanation
        with st.expander("📖 Understanding the Results"):
            st.write("""
            - **Sentiment**: Overall emotional tone of the text
            - **Polarity**: Measures how positive or negative the text is (-1 to 1)
                - Values closer to 1 indicate positive sentiment
                - Values closer to -1 indicate negative sentiment
                - Values around 0 indicate neutral sentiment
            - **Subjectivity**: Measures how subjective or objective the text is (0 to 1)
                - Values closer to 1 indicate subjective/personal opinion
                - Values closer to 0 indicate objective/factual information
            """)

def display_topic_interface():
    """Display topic analysis interface"""
    st.subheader("📑 Topic Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload a document (PDF, TXT, or DOCX)", 
        type=SUPPORTED_FILE_TYPES
    )
    
    if uploaded_file and st.button("Analyze Topics"):
        try:
            text = FileHandler.extract_text_from_file(uploaded_file)
            results = st.session_state.topic_service.analyze_topics(text)
            
            # Display dominant topic
            if results['dominant_topic']:
                st.subheader("📌 Main Theme")
                st.info(f"The document primarily discusses {results['dominant_topic']['summary']}")
            
            # Display all topics
            st.subheader("🔍 Key Themes Identified")
            for topic in results['topics']:
                with st.expander(f"Theme {topic['id']}", expanded=True):
                    # Display topic summary
                    st.write("📝 Summary:")
                    st.write(topic['summary'])
                    
                    # Display keywords
                    st.write("🔑 Key terms:")
                    keywords_list = [keyword['word'] for keyword in topic['keywords']]
                    st.write(", ".join(keywords_list))
            
            # Display coherence score
            st.metric(
                "Analysis Confidence", 
                "High" if results['coherence_score'] > 0.5 else "Medium",
                help="Indicates how well-defined and distinct the themes are"
            )
            
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")

def display_paraphrase_interface():
    """Display paraphrasing interface"""
    st.subheader("📝 Paraphrasing Tool")
    
    text_input = st.text_area("Enter text to paraphrase:")
    if st.button("Paraphrase"):
        if text_input:
            with st.spinner("Generating paraphrase..."):
                paraphrased_text = st.session_state.paraphrase_service.paraphrase(text_input)
                st.subheader("Paraphrased Version:")
                st.write(paraphrased_text)

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )

    # Custom CSS for sidebar styling
    st.markdown("""
        <style>
        /* Radio button container styling */
        .stRadio [role=radiogroup] {
            padding: 0.5rem;
            gap: 0.5rem;
            background-color: rgba(151, 166, 195, 0.15);
            border-radius: 0.5rem;
        }
        
        /* Radio button label styling */
        .stRadio label {
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
            cursor: pointer;
            color: rgb(49, 51, 63);
            background-color: rgba(151, 166, 195, 0.1);
            transition: background-color 0.2s ease;
        }
        
        /* Radio button hover effect */
        .stRadio label:hover {
            background-color: rgba(151, 166, 195, 0.2);
        }
        
        /* Selected radio button styling */
        .stRadio [role=radiogroup] [data-checked=true] {
            background-color: rgba(151, 166, 195, 0.4);
            border-color: rgb(49, 51, 63);
        }
        
        /* Radio group label styling */
        .stRadio > label {
            color: rgb(49, 51, 63) !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            display: block !important;
            background-color: transparent !important;
        }
        
        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            .stRadio > label {
                color: rgb(250, 250, 250) !important;
            }
            .stRadio [role=radiogroup] label span {
                color: rgb(250, 250, 250) !important;
            }
            .stRadio [role=radiogroup] {
                background-color: rgba(151, 166, 195, 0.1);
            }
            .stRadio label {
                background-color: rgba(151, 166, 195, 0.05);
            }
            .stRadio label:hover {
                background-color: rgba(151, 166, 195, 0.15);
            }
            .stRadio [role=radiogroup] [data-checked=true] {
                background-color: rgba(151, 166, 195, 0.3);
            }
        }
        </style>
    """, unsafe_allow_html=True)

    init_session_state()

    st.title("🤖 Text Analysis Suite")

    # Sidebar navigation using radio buttons
    with st.sidebar:
        st.session_state.current_page = st.radio(
            "Choose Analysis Type",
            ["Chat", "Sentiment Analysis", "Topic Analysis", "Paraphrasing"],
            key="navigation"
        )

    # Display the selected interface
    if st.session_state.current_page == "Chat":
        display_chat_interface()
    elif st.session_state.current_page == "Sentiment Analysis":
        display_sentiment_interface()
    elif st.session_state.current_page == "Topic Analysis":
        display_topic_interface()
    else:
        display_paraphrase_interface()

if __name__ == "__main__":
    main()