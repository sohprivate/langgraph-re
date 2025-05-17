import argparse
from dotenv import load_dotenv

from .agents.weather_agent import WeatherAgent
from .agents.search_agent import SearchAgent
from .agents.analysis_agent import AnalysisAgent
from .agents.report_agent import ReportAgent


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

    weather = weather_agent.get_current_weather(args.location)

    stats = analysis_agent.basic_stats(weather)
    stats_md = stats.to_markdown()

    search_results = search_agent.search(args.query)

    summary = report_agent.summarize(stats_md, search_results)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# Weather Report for {args.location}\n\n")
        f.write("## Current Weather Stats\n")
        f.write(stats_md + "\n\n")
        f.write("## Summary\n")
        f.write(summary + "\n")

    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
