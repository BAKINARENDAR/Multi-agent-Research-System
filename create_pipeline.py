from agents import (
    build_reader_agent,
    build_search_agent,
    critic_chain,
    writer_chain,
    editor_chain
)

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # =========================================================
    # STEP 1 - SEARCH AGENT
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent and reliable information about {topic}"
            )
        ]
    })

    state["search_results"] = (
        search_result["messages"][-1].content
    )

    print("\nSearch Results:")
    print(state["search_results"])


    # =========================================================
    # STEP 2 - READER AGENT
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 2 - READER AGENT")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
                Based on the following search results about
                '{topic}', pick the most relevant URL and
                scrape it for deeper content.

                Search Results:
                {state["search_results"][:800]}
                """
            )
        ]
    })

    state["scraped_content"] = (
        reader_result["messages"][-1].content
    )

    print("\nReader Output:")
    print(state["scraped_content"])


    # =========================================================
    # STEP 3 - WRITER CHAIN
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 3 - WRITER CHAIN")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nResearch Report:")
    print(state["report"])


    # =========================================================
    # STEP 4 - CRITIC CHAIN
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC CHAIN")
    print("=" * 50)

    state["critique"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Feedback:")
    print(state["critique"])

# =========================================================
        # STEP 4 - CRITIC CHAIN
# =========================================================
    print("\n" + "="*50)
    print("STEP 5 - EDITOR CHAIN")
    print("=" * 50)
    state["final_report"]=editor_chain.invoke({
        "research":research_combined,
        "report":state["report"],
        "critique":state["critique"]
    })
    print("\nFinal Research Report:")
    print(state["final_report"])


    return state



if __name__ == "__main__":

    topic = input("Enter research topic: ")

    result = run_research_pipeline(topic)