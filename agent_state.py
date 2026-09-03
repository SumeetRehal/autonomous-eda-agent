from typing import TypedDict, Optional
import pandas as pd

class EDAState(TypedDict):
    df: pd.DataFrame
    schema_summary: str
    code_to_execute: str
    execution_error: Optional[str]
    insights_report: str
