from __future__ import annotations

import argparse
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import xml.etree.ElementTree as ET

import pandas as pd
import yaml

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "pr": PKG_REL_NS}


@dataclass
class ParsedRow:
    timestamp: datetime
    v_bus: float
    i_inc: float
    p_total: float
    i_f_1: float
    i_f_2: float
    i_f_3: float
    source_sheet: str
    source_row: int


def _col_to_index(col: str) -> int:
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx


def _parse_cell_ref(cell_ref: str) -> int:
    col = "".join(ch for ch in cell_ref if ch.isalpha())
    return _col_to_index(col)


def _read_shared_strings(zf: zipfile.ZipFile) -> List[str]:
    path = "xl/sharedStrings.xml"
    if path not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(path))
    out: List[str] = []
    for si in root.findall("m:si", NS):
        tokens = [t.text or "" for t in si.findall(".//m:t", NS)]
        out.append("".join(tokens))
    return out


def _read_workbook_sheet_map(zf: zipfile.ZipFile) -> List[tuple[str, str]]:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("pr:Relationship", NS)}
    sheets: List[tuple[str, str]] = []
    for s in wb.findall("m:sheets/m:sheet", NS):
        name = s.attrib["name"]
        rid = s.attrib[f"{{{REL_NS}}}id"]
        target = rel_map[rid]
        sheets.append((name, f"xl/{target}"))
    return sheets


def _cell_value(cell: ET.Element, shared_strings: List[str]) -> str:
    t = cell.attrib.get("t")
    v = cell.find("m:v", NS)
    raw = v.text if v is not None and v.text is not None else ""
    if t == "s" and raw.isdigit():
        idx = int(raw)
        if 0 <= idx < len(shared_strings):
            return shared_strings[idx]
    return raw


def _as_float(v: str) -> Optional[float]:
    s = str(v).strip().replace(",", "")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _first_n_numeric(values_by_col: Dict[int, str], cols: List[int], n: int) -> List[Optional[float]]:
    nums: List[float] = []
    for c in cols:
        val = _as_float(values_by_col.get(c, ""))
        if val is not None:
            nums.append(float(val))
        if len(nums) >= n:
            break
    out: List[Optional[float]] = nums[:n]
    while len(out) < n:
        out.append(None)
    return out


def _parse_date_from_row_values(values: Iterable[str]) -> Optional[datetime]:
    for v in values:
        m = re.search(r"DATE:\s*(\d{1,2})\s*[-/]\s*(\d{1,2})\s*[-/]\s*(\d{4})", str(v), flags=re.IGNORECASE)
        if m:
            day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return datetime(year, month, day)
    return None


def _excel_serial_to_datetime(serial_value: float) -> datetime:
    # Excel 1900-date-system serial base (with leap-year bug convention).
    base = datetime(1899, 12, 30)
    return base + timedelta(days=float(serial_value))


def _parse_sheet(sheet_name: str, xml_bytes: bytes, shared_strings: List[str]) -> List[ParsedRow]:
    root = ET.fromstring(xml_bytes)
    rows = root.findall("m:sheetData/m:row", NS)
    parsed: List[ParsedRow] = []
    current_date: Optional[datetime] = None

    # Column mapping from observed workbook layout.
    col_time = 2   # B
    col_date_serial = 1  # A
    col_i_inc = 7  # G TOTAL (KA), used as aggregate incomer current signal
    col_v1 = 8     # H BB1 (KV)
    col_v2 = 9     # I BB2 (KV)
    col_p_total = 15  # O TOTAL (MW)
    incomer_cols = [3, 4, 5, 6]  # C..F incomer amps
    mw_cols = [11, 12, 13, 14]   # K..N incomer MW
    feeder_cols = list(range(17, 29))  # Q..AB feeder circuits

    for row in rows:
        row_idx = int(row.attrib["r"])
        cells = row.findall("m:c", NS)
        if not cells:
            continue

        values_by_col: Dict[int, str] = {}
        for c in cells:
            cell_ref = c.attrib.get("r", "")
            if not cell_ref:
                continue
            col_idx = _parse_cell_ref(cell_ref)
            values_by_col[col_idx] = _cell_value(c, shared_strings)

        date_candidate = _parse_date_from_row_values(values_by_col.values())
        if date_candidate is not None:
            current_date = date_candidate
        else:
            serial_val = _as_float(values_by_col.get(col_date_serial, ""))
            if serial_val is not None and serial_val > 40000:
                current_date = _excel_serial_to_datetime(serial_val).replace(hour=0, minute=0, second=0, microsecond=0)

        if current_date is None:
            continue

        hour_val = _as_float(values_by_col.get(col_time, ""))
        if hour_val is None:
            continue
        hour_int = int(hour_val)
        if hour_int < 1 or hour_int > 24:
            continue

        i_inc = _as_float(values_by_col.get(col_i_inc, ""))
        if i_inc is None:
            incomers = [x for x in (_as_float(values_by_col.get(c, "")) for c in incomer_cols) if x is not None]
            if incomers:
                i_inc = float(sum(incomers))

        p_total = _as_float(values_by_col.get(col_p_total, ""))
        if p_total is None:
            incomer_mw = [x for x in (_as_float(values_by_col.get(c, "")) for c in mw_cols) if x is not None]
            if incomer_mw:
                p_total = float(sum(incomer_mw))

        f1, f2, f3 = _first_n_numeric(values_by_col, feeder_cols, n=3)
        if i_inc is None or p_total is None or f1 is None or f2 is None or f3 is None:
            continue

        v1 = _as_float(values_by_col.get(col_v1, ""))
        v2 = _as_float(values_by_col.get(col_v2, ""))
        if v1 is None and v2 is None:
            continue
        v_bus = float(pd.Series([x for x in [v1, v2] if x is not None]).mean())

        timestamp = current_date + timedelta(hours=hour_int - 1)
        parsed.append(
            ParsedRow(
                timestamp=timestamp,
                v_bus=v_bus,
                i_inc=float(i_inc),
                p_total=float(p_total),
                i_f_1=float(f1),
                i_f_2=float(f2),
                i_f_3=float(f3),
                source_sheet=sheet_name,
                source_row=row_idx,
            )
        )

    return parsed


def ingest_workbook(xlsx_path: Path) -> pd.DataFrame:
    all_rows: List[ParsedRow] = []
    with zipfile.ZipFile(xlsx_path) as zf:
        shared_strings = _read_shared_strings(zf)
        sheets = _read_workbook_sheet_map(zf)
        for sheet_name, xml_path in sheets:
            parsed = _parse_sheet(sheet_name=sheet_name, xml_bytes=zf.read(xml_path), shared_strings=shared_strings)
            all_rows.extend(parsed)

    if not all_rows:
        raise RuntimeError("No valid hourly rows were parsed from workbook.")

    df = pd.DataFrame(
        [
            {
                "timestamp": r.timestamp,
                "v_bus": r.v_bus,
                "i_inc": r.i_inc,
                "p_total": r.p_total,
                "i_f_1": r.i_f_1,
                "i_f_2": r.i_f_2,
                "i_f_3": r.i_f_3,
                "source_sheet": r.source_sheet,
                "source_row": r.source_row,
            }
            for r in all_rows
        ]
    )
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"], keep="first").reset_index(drop=True)
    return df


def build_qc_summary(df: pd.DataFrame, source_xlsx: Path, output_csv: Path) -> dict:
    channel_cols = ["v_bus", "i_inc", "p_total", "i_f_1", "i_f_2", "i_f_3"]
    qc_channels = {
        c: {
            "missing_rate": float(df[c].isna().mean()),
            "min": float(df[c].min()),
            "max": float(df[c].max()),
            "mean": float(df[c].mean()),
        }
        for c in channel_cols
    }
    qc = {
        "source_file": str(source_xlsx),
        "output_file": str(output_csv),
        "rows": int(len(df)),
        "start_timestamp": str(df["timestamp"].min()),
        "end_timestamp": str(df["timestamp"].max()),
        "sheets_used": sorted(df["source_sheet"].unique().tolist()),
        "channels": qc_channels,
    }
    return qc


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Mallam BSP workbook into analysis-ready CSV for screening pipeline.")
    parser.add_argument("--input", default="MALLAM BSP HOURLY READINGS, 2024.xlsx", help="Path to source workbook (.xlsx)")
    parser.add_argument("--output", default="data/substation_scada_33_11kv.csv", help="Output analysis CSV path")
    parser.add_argument(
        "--provenance",
        default="manuscript/artifacts/research/data_provenance.yaml",
        help="Output provenance/QC YAML path",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    prov_path = Path(args.provenance)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prov_path.parent.mkdir(parents=True, exist_ok=True)

    df = ingest_workbook(input_path)

    analysis_df = df[["timestamp", "v_bus", "i_inc", "p_total", "i_f_1", "i_f_2", "i_f_3"]].copy()
    analysis_df.to_csv(output_path, index=False)

    qc = build_qc_summary(df, source_xlsx=input_path, output_csv=output_path)
    prov_path.write_text(yaml.safe_dump(qc, sort_keys=False), encoding="utf-8")

    print(f"Ingested {len(analysis_df)} rows from {input_path} -> {output_path}")
    print(f"Wrote provenance report: {prov_path}")


if __name__ == "__main__":
    main()
