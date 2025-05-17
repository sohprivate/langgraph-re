from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

try:
    from langgraph.graph import StateGraph
except ImportError:  # pragma: no cover - fallback when langgraph is missing
    class StateGraph:
        """Minimal graph orchestrator used when langgraph is unavailable."""

        def __init__(self, state_cls: type) -> None:
            self.state_cls = state_cls
            self._nodes: list[Callable[[Any], Any]] = []

        def add_node(self, name: str, func: Callable[[Any], Any]) -> None:
            self._nodes.append(func)

        def set_entry_point(self, name: str) -> None:
            pass

        def add_edge(self, from_node: str, to_node: str) -> None:
            pass

        def compile(self) -> Callable[[Any], Any]:
            def run(state: Any) -> Any:
                for node in self._nodes:
                    state = node(state)
                return state

            return run


@dataclass
class WorkflowState:
    location: str
    query: str
    weather_data: Dict[str, Any] | None = None
    analysis: str | None = None
    search_results: list[Dict[str, Any]] | None = None
    report: str | None = None


def build_workflow(weather_agent, analysis_agent, search_agent, report_agent) -> Callable[[WorkflowState], WorkflowState]:
    """Construct and compile the LangGraph workflow."""

    sg = StateGraph(WorkflowState)

    def fetch_weather(state: WorkflowState) -> WorkflowState:
        state.weather_data = weather_agent.get_current_weather(state.location)
        return state

    def analyze(state: WorkflowState) -> WorkflowState:
        stats = analysis_agent.basic_stats(state.weather_data)
        state.analysis = stats.to_markdown()
        return state

    def search(state: WorkflowState) -> WorkflowState:
        state.search_results = search_agent.search(state.query)
        return state

    def report(state: WorkflowState) -> WorkflowState:
        state.report = report_agent.summarize(state.analysis, state.search_results)
        return state

    sg.add_node("fetch_weather", fetch_weather)
    sg.add_node("analyze", analyze)
    sg.add_node("search", search)
    sg.add_node("report", report)

    sg.set_entry_point("fetch_weather")
    sg.add_edge("fetch_weather", "analyze")
    sg.add_edge("analyze", "search")
    sg.add_edge("search", "report")

    graph = sg.compile()

    def run(state: WorkflowState) -> WorkflowState:
        return graph(state)

    return run
