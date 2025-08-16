"""Financial analysis utilities for banking services."""

def _money(x, currency=""):
    """Format monetary values with comma separators and currency."""
    try:
        num = float(x)
        s = f"{num:,.0f}"
    except Exception:
        return str(x)
    return (s + (f" {currency}" if currency else "")).strip()


def _render_ifrs_html(data):
    """Generate an HTML report from IFRS data dictionary."""
    meta = data.get('report_meta', {})
    entity = meta.get('entity', 'Illustrative Bank')
    period = meta.get('period', 'FY20XX')
    currency = meta.get('currency', 'CU')

    def table(rows, left="Item", right="Amount"):
        """Generate an HTML table from rows of data."""
        rows = rows or [["—", "—"]]
        tr = "\n".join(
            f"<tr><td>{str(name)}</td><td class='text-end'>{_money(val, currency)}</td></tr>" 
            for name, val in rows
        )
        return f"""
            <table class='table table-sm mb-0'>
                <thead><tr><th>{left}</th><th class='text-end'>{right}</th></tr></thead>
                <tbody>{tr}</tbody>
            </table>"""

    sofp = data.get('sofp', {})
    pnl_oci = data.get('pnl_oci', {})
    eqc = data.get('equity_changes', [])
    cfs = data.get('cash_flows', {})

    def card(title, inner):
        """Generate a Bootstrap card with title and content."""
        return f"""
            <div class='card shadow-sm border-0 rounded-3 mb-3'>
                <div class='card-header bg-white'>
                    <h2 class='h6 m-0'>{title}</h2>
                </div>
                <div class='card-body'>{inner}</div>
            </div>"""

    html = f"""<!doctype html>
<html lang='en'>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>{entity} – IFRS Financial Statements</title>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>
    <style>
        body {{ background: #f7f7fb }}
        .note-head {{ font-weight: 600 }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}
    </style>
</head>
<body>
    <div class='container my-4'>
        <div class='mb-3 d-flex align-items-center justify-content-between'>
            <div>
                <div class='h4 m-0'>{entity}</div>
                <div class='text-muted'>IFRS Financial Statements – {period}</div>
                <div class='small text-muted'>Currency: {currency}</div>
            </div>
            <div class='small text-muted'>Generated Report</div>
        </div>

        {card("Statement of Financial Position (SoFP)", 
             f"<div class='grid-2'><div><div class='note-head mb-1'>Assets</div>{table(sofp.get('assets'))}</div><div><div class='note-head mb-1'>Liabilities</div>{table(sofp.get('liabilities'))}<hr/><div class='note-head mb-1'>Equity</div>{table(sofp.get('equity'))}</div></div>")}
        
        {card("Statement of Profit or Loss and Other Comprehensive Income",
             f"<div class='grid-2'><div><div class='note-head mb-1'>Profit or loss</div>{table(pnl_oci.get('pnl'))}</div><div><div class='note-head mb-1'>Other comprehensive income</div>{table(pnl_oci.get('oci'))}</div></div>")}
        
        {card("Statement of Changes in Equity", table(eqc, "Movement", "Amount"))}
        
        {card("Statement of Cash Flows (Indirect)",
             f"<div class='grid-2'><div><div class='note-head mb-1'>Operating activities</div>{table(cfs.get('operating'))}</div><div><div class='note-head mb-1'>Investing activities</div>{table(cfs.get('investing'))}<hr/><div class='note-head mb-1'>Financing activities</div>{table(cfs.get('financing'))}</div></div>")}

        {card("Notes – Basis & policies",
             "<p class='text-muted small'>IFRS basis (IFRS 18 khi áp dụng), chính sách trọng yếu (IFRS 9/7/13/15/16...).</p>")}
        
        {card("Notes – Financial instruments (IFRS 9)",
             "<p class='text-muted small'>Phân loại: amortised cost, FVOCI, FVTPL; SPPI; tái phân loại.</p>")}
        
        {card("Notes – ECL",
             "<p class='text-muted small'>Staging 1/2/3; PD/LGD/EAD; reconciliation; write-off & recoveries.</p>")}
        
        {card("Notes – Risk (IFRS 7)",
             "<p class='text-muted small'>Tín dụng, thanh khoản (maturity), thị trường (IR/FX), capital management.</p>")}
        
        {card("Notes – Fair value (IFRS 13)",
             "<p class='text-muted small'>Level 1–3; kỹ thuật định giá; input không quan sát được.</p>")}

        <p class='small text-muted mt-3'>*Illustrative only – không phải tư vấn/kế toán.</p>
    </div>
</body>
</html>"""
    
    return html
