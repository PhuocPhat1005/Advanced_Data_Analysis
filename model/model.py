# model/df_agent.p

from langchain.schema import SystemMessage, HumanMessage

class DFAgent:
    def __init__(self, agent, df_names):
        """
        - agent: object do create_pandas_dataframe_agent trả về
        - df_names: list tên DataFrame để ghi log
        """
        self.agent = agent
        self.df_names = df_names

    def ask(self, prompt: str) -> str:
        """
        Gửi prompt tới agent và trả về kết quả.
        Có thể thêm logging hoặc memory ở đây.
        """
        # Bạn có thể thêm SystemMessage/HumanMessage nếu cần
        return self.agent.invoke(prompt)
