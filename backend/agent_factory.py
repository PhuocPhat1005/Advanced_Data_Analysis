from dotenv import load_dotenv

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# Load biến môi trường từ .env
load_dotenv()

def create_df_agent(dataframes: list, temperature: float, model_name: str):
    """
    Khởi tạo một Pandas DataFrame Agent dùng Google Gemini qua LangChain.
    - dataframes: list các pandas.DataFrame đã load sẵn
    - model_name: tên model Gemini được chọn (vd. "gemini-2.5-pro")
    """

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
    )
    
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=dataframes,
        verbose=True,
        allow_dangerous_code=True,
        return_intermediate_steps=True,
        agent_executor_kwargs={
            "handle_parsing_errors": True
        },
    )

    return agent
