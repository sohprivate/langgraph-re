import argparse
from dotenv import load_dotenv

from .agents.weather_agent import WeatherAgent
from .agents.search_agent import SearchAgent
from .agents.analysis_agent import AnalysisAgent
from .agents.report_agent import ReportAgent
from .workflow import WorkflowState, build_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weather data research agent")
    parser.add_argument("--location", required=True, help="Location, e.g. Tokyo,JP")
    parser.add_argument("--query", required=True, help="Research topic")
    parser.add_argument("--output", default="report.md", help="Output Markdown file")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    weather_agent = WeatherAgent()
    search_agent = SearchAgent()
    analysis_agent = AnalysisAgent()
    report_agent = ReportAgent()

    workflow = build_workflow(
        weather_agent=weather_agent,
        analysis_agent=analysis_agent,
        search_agent=search_agent,
        report_agent=report_agent,
    )

    state = WorkflowState(location=args.location, query=args.query)
    result = workflow(state)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# Weather Report for {args.location}\n\n")
        if result.analysis:
            f.write("## Current Weather Stats\n")
            f.write(result.analysis + "\n\n")
        if result.report:
            f.write("## Summary\n")
            f.write(result.report + "\n")

    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
