# Tiller Finance Dashboard v2 — Setup Instructions

Complete setup guide for `tiller-dashboard-v2.json`. Follow these steps in order before importing.

---

## Overview

This app requires four things set up in Retool before the import will work:
1. Two Retool DB tables (`transactions`, `saved_views`)
2. A Google Sheets resource connected to your Tiller spreadsheet
3. A REST API resource pointing to the Claude (Anthropic) API
4. The app import itself, then resource reconnection

---

## Step 1: Create Retool DB Tables

Go to **Resources → Retool Database** in the left sidebar (or via the top nav).

### Create `transactions` table

Open the Retool DB editor and run:

```sql
CREATE TABLE IF NOT EXISTS transactions (
  id SERIAL PRIMARY KEY,
  date DATE,
  description TEXT,
  category TEXT,
  amount NUMERIC(12, 2),
  account TEXT,
  account_number TEXT,
  institution TEXT,
  month TEXT,
  week TEXT,
  transaction_id TEXT UNIQUE NOT NULL,
  check_number TEXT,
  full_description TEXT,
  labels TEXT,
  hide BOOLEAN DEFAULT FALSE,
  synced_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_id ON transactions(transaction_id);
```

### Create `saved_views` table

```sql
CREATE TABLE IF NOT EXISTS saved_views (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  sql TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Step 2: Connect Google Sheets (Tiller)

### Authenticate Google Sheets in Retool

1. Go to **Resources** in the top nav → **Create new resource**
2. Select **Google Sheets**
3. Name it exactly: `Google_sheets_Tiller`
   > This name must match exactly — the app queries reference this resource name
4. Click **Connect Google Account** and authorize with the Google account that has your Tiller spreadsheet
5. Click **Save**

### Verify Tiller spreadsheet access

Your Tiller spreadsheet ID is: `1fokhoSVGss2ivA_8gnuDMR_IZBOvzksnArKeFHkzQWA`

Confirm that the authorized Google account has access to this spreadsheet at:
`https://docs.google.com/spreadsheets/d/1fokhoSVGss2ivA_8gnuDMR_IZBOvzksnArKeFHkzQWA`

The app reads the **Transactions** sheet tab. Tiller's standard column names are:
`Date`, `Description`, `Category`, `Amount`, `Account`, `Account #`, `Institution`, `Month`, `Week`, `Transaction ID`, `Check Number`, `Full Description`, `Labels`, `Hide`

---

## Step 3: Create Claude API Resource

1. Go to **Resources** → **Create new resource**
2. Select **REST API**
3. Configure:
   - **Name**: `claude_api`
   - **Base URL**: `https://api.anthropic.com`
   - **Headers** (add these two):
     - `anthropic-version` → `2023-06-01`
     - `content-type` → `application/json`
4. Leave authentication as **None** (the app passes the API key dynamically via the UI)
5. Click **Save**

### Get your Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Navigate to **API Keys** → **Create Key**
3. Copy the key (starts with `sk-ant-...`)
4. You will paste this into the app's **Anthropic API Key** field after import

> The app stores the key in browser localStorage so you only need to enter it once per browser.

---

## Step 4: Import the App

1. In Retool, go to **Apps** in the top nav
2. Click **Create new** → **Import app**
3. Upload `tiller-dashboard-v2.json`
4. Name the app (e.g. "Tiller Finance Dashboard")
5. Click **Import**

---

## Step 5: Reconnect Resources After Import

After import, Retool will likely show resource connection errors because the resource UUIDs in the JSON are from the original build environment. Reconnect each query:

### Reconnect Retool DB queries

For each of these queries, open the query in the editor and change the resource to your `retool_db`:
- `loadSavedViews`
- `saveViewQuery`
- `deleteViewQuery`
- `queryResults`
- `upsertTransactions`
- `spendingByCategory`
- `monthlyTrend`
- `topMerchants`
- `incomeVsExpenses`
- `spendingByInstitution`

**How to reconnect:**
1. Open the app in Edit mode
2. Click any query in the left panel
3. In the query editor, click the resource dropdown at the top
4. Select `retool_db`
5. Repeat for each query above

### Reconnect Google Sheets query

Open `fetchTransactions` → set resource to `Google_sheets_Tiller`

### Reconnect Claude REST queries

Open `generateSQL` and `refineSQL` → set resource to `claude_api`

> **Tip**: Use the query list search (magnifying glass icon) to find queries quickly.

---

## Step 6: First Run

1. **Enter your API key**: In the app's sync bar, paste your Anthropic API key into the **Anthropic API Key** field and click **Save Key**

2. **Sync transactions**: Click **Sync from Google Sheets**
   - This fetches all rows from your Tiller Transactions sheet
   - Upserts them into the `transactions` Retool DB table
   - Status updates will show progress
   - First sync may take 10–30 seconds depending on data volume

3. **Test a query**: In the Query Builder, type something like:
   > "Show me all restaurant spending last month"

   Click **Generate SQL with AI** — Claude will produce SQL and an explanation.

4. **Run it**: Click **Run Query** to execute against your transactions data.

---

## Tiller Authentication Notes

Tiller uses Google Sheets as its backend. The connection flow in Retool:

```
Tiller (Bank sync) → Your Google Sheet → Retool Google Sheets resource → App
```

- Tiller automatically syncs your bank transactions to the Google Sheet daily
- Retool reads from that sheet on demand (when you click "Sync from Google Sheets")
- The app then copies the data into Retool DB for fast SQL querying

**Important**: The Google account you authorize in Retool must be the **same Google account** that owns the Tiller spreadsheet. If your Tiller spreadsheet is shared with another account, use the owner account.

**If Google Sheets authorization expires**: Go to **Resources → Google_sheets_Tiller → Edit** and re-authorize.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Sync" shows 0 rows | Verify the `Transactions` sheet tab name matches exactly (case-sensitive) |
| Resource connection error | Reconnect the query to the correct resource (Step 5) |
| Claude API error | Check the API key is correct and has credits |
| SQL parse error from Claude | Claude returned unexpected format — try rephrasing the question |
| `upsertTransactions` fails | The `transactions` table may not exist — re-run Step 1 SQL |
| "No view selected" on Load | Click a row in the Saved Views table first |
| Charts show no data | Run "Apply Date Filter" on the Summary page to trigger the chart queries |

---

## Resource Summary

| Resource Name | Type | Purpose |
|---|---|---|
| `retool_db` | Retool Database (built-in) | Stores transactions + saved views |
| `Google_sheets_Tiller` | Google Sheets | Reads from Tiller spreadsheet |
| `claude_api` | REST API (`https://api.anthropic.com`) | AI SQL generation + refinement |

---

## App Pages

| Page | URL slug | Purpose |
|---|---|---|
| Query Builder | `/query-builder` | Sync, AI SQL gen, run queries, save views |
| Summary & Charts | `/summary` | Spending charts, trends, top merchants, stats |
