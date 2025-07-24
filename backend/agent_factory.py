from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load biến môi trường từ .env
load_dotenv()
assert os.getenv("GOOGLE_API_KEY"), "Vui lòng set GOOGLE_API_KEY trong .env"

def create_df_agent(dataframes: list, temperature: float, model_name: str):
    """
    Khởi tạo một Pandas DataFrame Agent dùng Google Gemini qua LangChain.
    - dataframes: list các pandas.DataFrame đã load sẵn
    - model_name: tên model Gemini được chọn (vd. "gemini-2.5-pro")
    """
    # Khởi llm
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=dataframes,
        return_intermediate_steps=True,
        agent_type="zero-shot-react-description",
        verbose=True,
        allow_dangerous_code=True,
        agent_executor_kwargs={
            "handle_parsing_errors": True,
        },
    )

    return agent
