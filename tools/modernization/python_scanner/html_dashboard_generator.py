"""
tools/modernization/python_scanner/html_dashboard_generator.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.19

Modernization HTML Dashboard Generator

Generates a standalone HTML dashboard from the
modernization dashboard data produced by
DashboardBuilder.

Output:
    modernization_dashboard.html
"""

from __future__ import annotations

import html

from pathlib import Path

from typing import Any
from typing import Dict


class HTMLDashboardGenerator:
    """
    Generates a standalone HTML dashboard.

    The generator consumes the dictionary produced by
    DashboardBuilder.build() and creates a self-contained
    HTML report that can be opened in any browser.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        self.output_directory = Path(
            output_directory,
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # PUBLIC
    # =====================================================

    def generate(
        self,
        dashboard: Dict[str, Any],
    ) -> Path:
        """
        Build and save the HTML dashboard.

        Parameters
        ----------
        dashboard
            Dashboard dictionary returned by
            DashboardBuilder.build().

        Returns
        -------
        Path
            Path to the generated HTML report.
        """

        output_file = (
            self.output_directory
            / "modernization_dashboard.html"
        )

        html_document = self._build_document(
            dashboard,
        )

        output_file.write_text(
            html_document,
            encoding="utf-8",
        )

        return output_file

    # =====================================================
    # HTML
    # =====================================================

    def _build_document(
        self,
        dashboard: Dict[str, Any],
    ) -> str:
        """
        Build the complete HTML document.

        Remaining sections are implemented in
        Parts 2–4.
        """

        return (
            "<!DOCTYPE html>\n"
            "<html lang='en'>\n"
            f"{self._build_head()}"
            "<body>\n"
            "<div class='container'>\n"
            "<h1>"
            "UDUAK QUANT SYSTEM"
            "</h1>\n"
            "<h2>"
            "Modernization Dashboard"
            "</h2>\n"
            "<hr>\n"
            "<!-- Project Summary -->\n"
            f"{self._project_summary(dashboard)}"
            "<!-- Remaining sections added in Part 2 -->\n"
            "</div>\n"
            "</body>\n"
            "</html>\n"
        )

    # =====================================================
    # PLACEHOLDERS
    # =====================================================

    def _build_head(
        self,
    ) -> str:
        """
        HTML <head>.

        Implemented in Part 2.
        """

        return (
            "<head>\n"
            "<meta charset='utf-8'>\n"
            "<title>"
            "Modernization Dashboard"
            "</title>\n"
            "</head>\n"
        )

    # -----------------------------------------------------

    def _project_summary(
        self,
        dashboard: Dict[str, Any],
    ) -> str:
        """
        Project summary placeholder.

        Full implementation arrives in Part 2.
        """

        project = dashboard.get(
            "project",
            {},
        )

        modules = html.escape(
            str(
                project.get(
                    "modules",
                    "-",
                )
            )
        )

        classes = html.escape(
            str(
                project.get(
                    "classes",
                    "-",
                )
            )
        )

        functions = html.escape(
            str(
                project.get(
                    "functions",
                    "-",
                )
            )
        )

        imports = html.escape(
            str(
                project.get(
                    "imports",
                    "-",
                )
            )
        )

        return (
            "<table border='1' "
            "cellpadding='6'>"
            "<tr>"
            "<th>Modules</th>"
            "<th>Classes</th>"
            "<th>Functions</th>"
            "<th>Imports</th>"
            "</tr>"
            "<tr>"
            f"<td>{modules}</td>"
            f"<td>{classes}</td>"
            f"<td>{functions}</td>"
            f"<td>{imports}</td>"
            "</tr>"
            "</table>\n"
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    generator = HTMLDashboardGenerator(
        Path(
            "tools/modernization/reports",
        )
    )

    dashboard = {
        "project": {
            "modules": 168,
            "classes": 142,
            "functions": 516,
            "imports": 648,
        }
    }

    report = generator.generate(
        dashboard,
    )

    print("=" * 60)
    print("HTML DASHBOARD")
    print("=" * 60)
    print(report)

        # =====================================================
    # HTML HEAD
    # =====================================================

    def _build_head(
        self,
    ) -> str:
        """
        Build the HTML <head> section with embedded CSS.
        """

        return """
<head>

<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
UDUAK QUANT SYSTEM - Modernization Dashboard
</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{

    background:#f4f6f9;

    color:#222;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    line-height:1.6;
}

.container{

    max-width:1400px;

    margin:auto;

    padding:30px;
}

h1{

    color:#183153;

    margin-bottom:8px;
}

h2{

    color:#3f5873;

    margin-bottom:20px;
}

hr{

    margin-bottom:25px;

    border:none;

    border-top:2px solid #d7dde5;
}

.section{

    background:white;

    padding:20px;

    margin-bottom:25px;

    border-radius:10px;

    box-shadow:
        0 2px 10px rgba(
            0,
            0,
            0,
            0.08
        );
}

.section-title{

    font-size:22px;

    color:#183153;

    margin-bottom:18px;
}

.cards{

    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(180px,1fr)
        );

    gap:18px;
}

.card{

    background:#183153;

    color:white;

    padding:18px;

    border-radius:8px;

    text-align:center;
}

.card-value{

    font-size:34px;

    font-weight:bold;

    margin-top:8px;
}

.good{

    color:#27ae60;

    font-weight:bold;
}

.warning{

    color:#f39c12;

    font-weight:bold;
}

.bad{

    color:#c0392b;

    font-weight:bold;
}

table{

    width:100%;

    border-collapse:collapse;
}

th{

    background:#183153;

    color:white;

    padding:10px;
}

td{

    padding:9px;

    border:1px solid #d9d9d9;
}

tr:nth-child(even){

    background:#fafafa;
}

.footer{

    margin-top:40px;

    text-align:center;

    color:#777;

    font-size:13px;
}

</style>

</head>
"""

    # =====================================================
    # PROJECT SUMMARY
    # =====================================================

    def _project_summary(
        self,
        dashboard: Dict[str, Any],
    ) -> str:

        project = dashboard.get(
            "project",
            {},
        )

        modules = project.get(
            "modules",
            0,
        )

        classes = project.get(
            "classes",
            0,
        )

        functions = project.get(
            "functions",
            0,
        )

        imports = project.get(
            "imports",
            0,
        )

        syntax = project.get(
            "syntax_errors",
            0,
        )

        return f"""
<div class="section">

<div class="section-title">
Project Summary
</div>

<div class="cards">

<div class="card">

<div>Modules</div>

<div class="card-value">
{modules}
</div>

</div>

<div class="card">

<div>Classes</div>

<div class="card-value">
{classes}
</div>

</div>

<div class="card">

<div>Functions</div>

<div class="card-value">
{functions}
</div>

</div>

<div class="card">

<div>Imports</div>

<div class="card-value">
{imports}
</div>

</div>

<div class="card">

<div>Syntax Errors</div>

<div class="card-value">
{syntax}
</div>

</div>

</div>

</div>
"""

    # =====================================================
    # HEALTH SCORE
    # =====================================================

    def _health_section(
        self,
        dashboard: Dict[str, Any],
    ) -> str:

        health = dashboard.get(
            "health",
            {},
        )

        score = health.get(
            "score",
            0,
        )

        grade = health.get(
            "grade",
            "N/A",
        )

        status = "good"

        if score < 80:
            status = "warning"

        if score < 60:
            status = "bad"

        return f"""
<div class="section">

<div class="section-title">
Project Health
</div>

<div class="cards">

<div class="card">

<div>Health Score</div>

<div class="card-value {status}">
{score}
</div>

</div>

<div class="card">

<div>Grade</div>

<div class="card-value">
{grade}
</div>

</div>

</div>

</div>
"""

    # =====================================================
    # ARCHITECTURE
    # =====================================================

    def _architecture_section(
        self,
        dashboard: Dict[str, Any],
    ) -> str:

        architecture = dashboard.get(
            "architecture",
            {},
        )

        rows = ""

        for key, value in architecture.items():

            rows += f"""
<tr>

<td>{html.escape(str(key))}</td>

<td>{html.escape(str(value))}</td>

</tr>
"""

        return f"""
<div class="section">

<div class="section-title">
Architecture Analysis
</div>

<table>

<tr>

<th>Metric</th>

<th>Value</th>

</tr>

{rows}

</table>

</div>
"""

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _recommendation_section(
        self,
        dashboard: Dict[str, Any],
    ) -> str:

        recommendations = (
            dashboard
            .get(
                "recommendations",
                {},
            )
            .get(
                "items",
                [],
            )
        )

        rows = ""

        if not recommendations:

            rows = """
<tr>

<td>No recommendations.</td>

</tr>
"""

        else:

            for recommendation in recommendations:

                rows += f"""
<tr>

<td>
{html.escape(str(recommendation))}
</td>

</tr>
"""

        return f"""
<div class="section">

<div class="section-title">
Modernization Recommendations
</div>

<table>

<tr>

<th>Recommendation</th>

</tr>

{rows}

</table>

</div>
"""

    # =====================================================
    # DEPENDENCIES
    # =====================================================

    def _dependency_section(
        self,
        dashboard: Dict[str, Any],
    ) -> str:

        dependency = dashboard.get(
            "dependencies",
            {},
        )

        cycles = dependency.get(
            "cycles",
            [],
        )

        rows = ""

        if not cycles:

            rows = """
<tr>

<td class="good">
No circular dependencies detected.
</td>

</tr>
"""

        else:

            for cycle in cycles:

                rows += f"""
<tr>

<td class="bad">

{html.escape(' -> '.join(cycle))}

</td>

</tr>
"""

        return f"""
<div class="section">

<div class="section-title">
Dependency Analysis
</div>

<table>

<tr>

<th>Circular Dependencies</th>

</tr>

{rows}

</table>

</div>
"""

    # =====================================================
    # BUILD COMPLETE DOCUMENT
    # =====================================================

    def _build_document(
        self,
        dashboard: Dict[str, Any],
    ) -> str:
        """
        Assemble the complete HTML document.
        """

        return (
            "<!DOCTYPE html>\n"
            "<html lang='en'>\n"
            f"{self._build_head()}"
            "<body>\n"
            "<div class='container'>\n"

            "<h1>"
            "UDUAK QUANT SYSTEM"
            "</h1>\n"

            "<h2>"
            "Modernization Dashboard"
            "</h2>\n"

            "<hr>\n"

            f"{self._project_summary(dashboard)}"

            f"{self._health_section(dashboard)}"

            f"{self._architecture_section(dashboard)}"

            f"{self._recommendation_section(dashboard)}"

            f"{self._dependency_section(dashboard)}"

            "<div class='footer'>\n"

            "Generated automatically by the "

            "<strong>"

            "UDUAK QUANT SYSTEM "

            "Modernization Toolkit"

            "</strong>"

            "</div>\n"

            "</div>\n"

            "</body>\n"

            "</html>\n"
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path

    generator = HTMLDashboardGenerator(

        Path(
            "tools/modernization/reports",
        )

    )

    dashboard = {

        "project": {

            "modules": 168,

            "classes": 142,

            "functions": 516,

            "imports": 648,

            "syntax_errors": 0,

        },

        "health": {

            "score": 96,

            "grade": "A",

        },

        "architecture": {

            "Layers": 6,

            "Packages": 28,

            "Coupling": "Low",

            "Cohesion": "High",

        },

        "recommendations": {

            "items": [

                "Separate execution layer from analysis layer.",

                "Reduce large utility modules.",

                "Increase unit-test coverage.",

            ],

        },

        "dependencies": {

            "cycles": [

            ],

        },

    }

    report = generator.generate(

        dashboard,

    )

    print("=" * 60)

    print("HTML DASHBOARD")

    print("=" * 60)

    print(report)