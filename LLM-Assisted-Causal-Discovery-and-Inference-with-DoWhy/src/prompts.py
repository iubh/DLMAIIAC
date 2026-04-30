"""Prompt(s) and tiny helpers for the teaching notebook.

This module is intentionally minimal: students should be able to read it quickly.
"""

from __future__ import annotations


CAUSAL_DISCOVERY_PROMPT = """You are a causal inference expert.

We have the following variables from a job training study (Lalonde dataset):

In the context of evaluating the impact of a job training program on earnings, several key variables are used. 
These variables are divided into categories based on their roles in the study:

Treatment and Outcome Variables:
treat: A binary indicator representing participation in the job training program (1 = participated/treated, 0 = did not participate/control). This serves as the treatment variable to distinguish between those who received the intervention and those who did not.
re78: The real earnings of individuals measured in 1978, which is after they have potentially undergone the job training. This variable represents the primary outcome for estimating the causal effect of the treatment.

Pre-treatment Covariates:
age: The age of participants at the baseline measurement.
educ: Number of years an individual has spent in formal education.
black: A binary indicator where 1 signifies that the individual is Black, and 0 otherwise.
hisp: A binary indicator where 1 indicates Hispanic ethnicity, and 0 otherwise.
married: Indicator variable for marital status, with 1 meaning married and 0 not married.
nodegr: Binary indicator for educational attainment, specifically whether an individual lacks a high school degree (1 = no degree, 0 = has a degree).

Historical Earnings:
re74: Real earnings from the year 1974, reflecting pre-treatment labor market income.
re75: Real earnings from the year 1975, also representing pre-treatment labor market income.

Employment Status Indicators:
u74: Employment status in 1974, where 1 indicates unemployment and 0 indicates employment.
u75: Employment status in 1975, with 1 indicating unemployment and 0 indicating employment.

Task:
Construct a plausible causal directed acyclic graph (DAG) representing the main causal structure relevant for estimating the causal effect of treat on re78 as JSON.

Important causal modeling principles

When constructing the DAG:
Include likely confounders:
Variables that plausibly affect BOTH treatment assignment (treat) and the outcome (re78) should typically be modeled as common causes.
In this dataset, pre-treatment socioeconomic and labor-market variables are likely confounders.

Emphasize temporal ordering:
Pre-treatment variables may cause treatment and post-treatment outcomes.
Post-treatment variables should generally not cause pre-treatment variables.
Historical earnings (re74, re75) occur before treatment and are strong predictors of future earnings.

Capture major labor-market relationships:
Education and degree status influence employment and earnings.
Prior earnings and unemployment status influence future earnings and treatment participation.
Demographic variables may influence both treatment participation and earnings opportunities.

Prefer sparse, high-level structure:
Include only the most important causal relationships.
Avoid redundant or weak edges.
Focus on the main confounding structure needed for causal adjustment.

Ensure the graph is acyclic:
Do not create feedback loops or cycles.

Rules:
- Output ONLY JSON. No commentary.
- The JSON must have a top-level key "edges".
- Each edge is a pair ["cause", "effect"].
- Use only the variable names listed above.
- Keep it reasonably sparse and concentrate on the major causa relations (5-10 edges max.).

Expected format:
{
  "edges": [
    ["educ", "treat"],
    ["educ", "re78"]
  ]
}
"""


# def example_fallback_edges() -> list[list[str]]:
#     """A realistic edge list used when no local LLM server is available.

#     This is *not* the ground truth; it's a plausible prior suitable for teaching.
#     """

#     return [
#         ["age", "educ"],
#         ["educ", "nodegr"],
#         ["educ", "treat"],
#         ["educ", "re78"],
#         ["nodegr", "treat"],
#         ["black", "treat"],
#         ["hisp", "treat"],
#         ["married", "treat"],
#         ["re74", "treat"],
#         ["re75", "treat"],
#         ["re74", "re78"],
#         ["re75", "re78"],
#         ["treat", "re78"],
#     ]
