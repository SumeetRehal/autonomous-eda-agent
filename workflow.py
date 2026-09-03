from langgraph.graph import StateGraph, END
from agent_state import EDAState
from core_nodes import profile_schema, plan_and_generate_code, execute_code, synthesize_insights

def execution_check(state: EDAState):
    if state.get("execution_error"):
        return "plan_and_generate"
    return "synthesize"

builder = StateGraph(EDAState)
builder.add_node("profile", profile_schema)
builder.add_node("plan_and_generate", plan_and_generate_code)
builder.add_node("execute", execute_code)
builder.add_node("synthesize", synthesize_insights)

builder.set_entry_point("profile")
builder.add_edge("profile", "plan_and_generate")
builder.add_edge("plan_and_generate", "execute")
builder.add_conditional_edges("execute", execution_check, {
    "plan_and_generate": "plan_and_generate",
    "synthesize": "synthesize"
})
builder.add_edge("synthesize", END)

eda_graph = builder.compile()
