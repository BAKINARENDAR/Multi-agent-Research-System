import os
import dotenv
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import web_search,scrap_url
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b"
)

# 1st agent
def build_search_agent():
    return create_agent(
        model=model,
        tools=[web_search],
        system_prompt="""
        You are a Search Agent.

        Your ONLY job is to search the web using the web_search tool.

        IMPORTANT RULES:
        - You can ONLY use the web_search tool.
        - Always call web_search with the argument `query`.
        - Never call web_open.
        - Never call scrap_url.
        - Never try to open URLs yourself.
        - Do not invent tool names.
        - Do not use arguments such as cursor or id.
        - Return the search results including useful titles,
        URLs and snippets.

        After searching, stop and return the search results.
        """
    )
# 2nd agent

def build_reader_agent():
    return create_agent(
        model=model,
        tools=[scrap_url],
        system_prompt="""
        You are a Reader Agent.

        Your job is to read webpages found by the Search Agent.

        IMPORTANT RULES:
        - You can ONLY use the scrap_url tool.
        - Always call scrap_url with the argument `url`.
        - Never call web_search.
        - Never call web_open.
        - Do not invent tool names.
        - Do not use arguments such as cursor or id.

        Choose a relevant URL from the search results and
        scrape that webpage using scrap_url.

        Return the useful factual information extracted
        from the webpage.
        """
    )

# writer chain

writer_prompt=ChatPromptTemplate.from_messages(
    [
        (
                "system",
                """
                You are an expert research report writer.

                Use the research material provided to write
                a clear, structured and informative report.

                Include:

                1. Title
                2. Introduction
                3. Main findings
                4. Important evidence
                5. Conclusion

                Do not invent information that is not present
                in the research material.
                """
            ),
            (
                "human",
                """
                Write a research report using the following
                research material:

                {research}
                """
            )
    ]
)

writer_chain=writer_prompt | model | StrOutputParser()


# critic chain

critic_prompt=ChatPromptTemplate.from_messages(
    [
        (
                "system",
                """
                You are a research report critic.

                Analyze the report for:

                - Accuracy
                - Completeness
                - Clarity
                - Structure
                - Evidence
                - Unsupported claims

                Give a score out of 10 and detailed feedback.

                Format your response as:

                Score: X/10

                Feedback:
                <your feedback>
                """
            ),
            (
                "human",
                """
                Review the following research report:

                {report}
                """
            )
    ]
)
critic_chain=critic_prompt | model | StrOutputParser()

# editor prompt
editor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert research report editor.

            Revise the draft report using the critic feedback.

            IMPORTANT RULES:

            1. Use ONLY information explicitly present in
               the research material.

            2. Do NOT add new facts, statistics, sources,
               examples, explanations, or recommendations
               that are not supported by the research.

            3. If the critic asks for additional information
               that is not present in the research material,
               DO NOT add it.

            4. If a claim is weak or unsupported, remove it
               or clearly describe it as an unverified claim
               rather than presenting it as fact.

            5. Do not invent methodology, sample sizes,
               geographic scope, interviews, surveys, or
               data-collection methods.

            6. Preserve accurate information from the
               original research.

            7. Return only the revised final report.
            """
        ),
        (
            "human",
            """
            Revise the following draft report.

            RESEARCH MATERIAL:
            {research}

            DRAFT REPORT:
            {report}

            CRITIC FEEDBACK:
            {critique}

            Produce the final report using ONLY evidence
            supported by the research material.
            """
        )
    ]
)

editor_chain = editor_prompt | model | StrOutputParser()
