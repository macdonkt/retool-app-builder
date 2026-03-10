# Tiller Transaction Query Builder — Reverse Engineered Plan

## What This App Does

A **Tiller Finance dashboard** that pulls transaction data from a Google Sheets Tiller spreadsheet into Retool DB, then lets the user query and explore that data using natural language → SQL generation powered by AI.

---

## Data Sources

| Resource | Type | Purpose |
|---|---|---|
| `Google_sheets_Tiller` | Google Sheets | Source of truth — Tiller's `Transactions` sheet (spreadsheet ID: `1fokhoSVGss2ivA_8gnuDMR_IZBOvzksnArKeFHkzQWA`) |
| `retool_db` | Retool DB (Postgres) | Local copy of transactions; the target for syncing and querying |

---

## Queries

| Query | Type | What It Does | Status |
|---|---|---|---|
| `query1` | GoogleSheetsQuery | Fetches rows from the Tiller `Transactions` sheet | Working |
| `syncToRetoolDB` | JavascriptQuery | Syncs Google Sheets rows into Retool DB | **Stub** — only updates status/timestamp, no actual insert |
| `truncateTransactions` | RetoolTableQuery | Clears the `transactions` table in Retool DB before sync | Working |
| `queryResults` | SqlQueryUnified | Runs `{{ currentSQL.value }}` against Retool DB | Working |
| `loadViewQuery` | JavascriptQuery | Loads a saved view's SQL into `currentSQL` state | Working |

---

## State Variables

| Variable | Purpose |
|---|---|
| `currentSQL` | Holds the active SQL query text |
| `sqlExplanation` | Holds the AI-generated explanation of the SQL |
| `lastSyncTime` | ISO timestamp of last Google Sheets sync |
| `syncStatus` | Human-readable status message for sync |

> `savedViews` variable removed — replaced by `saved_views` DB table.

---

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  # Transaction Query Builder                             │
│  [Sync Now]  Last synced: ...  Status: ...              │
├──────────────┬───────────────────────┬──────────────────┤
│ ### Saved    │ ### Query Builder     │ ### AI           │
│ Views        │                       │ Refinement       │
│              │ [natural language     │                  │
│ [Table of    │  input]               │ [refinement      │
│  saved views]│ [Generate SQL]        │  instructions]   │
│              │                       │                  │
│ [Save View]  │ [SQL text area]       │ [refinement      │
│              │ [explanation text]    │  input]          │
│              │ [Edit SQL] [Run Query]│ [Refine Query]   │
├──────────────┴───────────────────────┴──────────────────┤
│ ### Results                      Row count: ...         │
│ [Results table]                                         │
│ [debug text]                                            │
└─────────────────────────────────────────────────────────┘
```

**Modal:** `saveViewModal` — Name + Description inputs, Cancel/Save buttons

---

## Feature Status

### Working
- Load saved view → populate `currentSQL` + `sqlExplanation` from `savedViews` variable
- Run query → execute `currentSQL.value` against Retool DB, show in results table
- UI layout: three-panel design (saved views | query builder | AI refinement)

### Stubs / Not Implemented
1. **Sync from Google Sheets** — `syncToRetoolDB` does not insert rows. Needs a bulk upsert query to write `query1.data` rows into a `transactions` table in Retool DB.
2. **Generate SQL (AI)** — `generateSQLButton` has empty event handlers. Needs an AI query (Claude/OpenAI) that takes `naturalLanguageInput.value` and generates SQL against the transactions schema.
3. **Refine Query (AI)** — `refineButton` with `refinementInput` and `refinementInstructions` — likely another AI call to modify the current SQL based on user instructions.

---

## What Needs to Be Built (v2)

### Page 1: Query Builder (fix existing stubs)

1. **Real incremental sync**
   - `syncToRetoolDB` JS query: for each row in `query1.data`, upsert into `transactions` on `transaction_id`
   - Uses a `SqlQueryUnified` upsert query: `INSERT INTO transactions (...) VALUES ... ON CONFLICT (transaction_id) DO UPDATE SET ...`
   - Updates `lastSyncTime` and `syncStatus` with row count on success

2. **AI Generate SQL** — REST query to Claude API (`claude-sonnet-4-6`)
   - Resource: REST API with base URL `https://api.anthropic.com`
   - System prompt describes the `transactions` table schema
   - User message: `naturalLanguageInput.value`
   - On success: parse response → set `currentSQL.value` + `sqlExplanation.value`
   - On error: show error toast

3. **AI Refine Query** — Second REST query to Claude API
   - Takes `currentSQL.value` + `refinementInput.value` + `refinementInstructions.value`
   - Returns updated SQL + updated explanation

4. **Save Views to DB**
   - Replace in-memory `savedViews` variable with DB-backed queries
   - `loadSavedViews` — SELECT from `saved_views` table, populates the sidebar table
   - `saveViewQuery` — INSERT/UPDATE into `saved_views` on submit
   - `deleteViewQuery` — DELETE from `saved_views` (add delete button to sidebar table)
   - `loadViewQuery` — sets `currentSQL` + `sqlExplanation` from selected row

5. **Results table formatting**
   - Date column: formatted date
   - Amount column: currency formatting, red for negative
   - Category: tag/badge style

### Page 2: Summary / Charts

Components:
- Date range picker (start/end date inputs) to filter all charts
- **Spending by Category** — bar or donut chart, SQL: `SELECT category, SUM(amount) FROM transactions WHERE date BETWEEN ... GROUP BY category ORDER BY SUM(amount)`
- **Monthly Spending Trend** — line chart, SQL: `SELECT month, SUM(amount) FROM transactions WHERE amount < 0 GROUP BY month ORDER BY month`
- **Top Merchants** — table, SQL: `SELECT description, COUNT(*), SUM(amount) FROM transactions GROUP BY description ORDER BY SUM(amount) LIMIT 20`
- **Income vs Expenses** — stat cards: total income (positive amounts), total expenses (negative amounts), net
- **Account Balances by Institution** — bar chart grouped by institution

## Claude API Configuration

- **Resource name**: `claude_api` (REST resource, base URL: `https://api.anthropic.com`)
- **Headers**: `x-api-key: {{anthropic_api_key}}`, `anthropic-version: 2023-06-01`, `content-type: application/json`
- **Model**: `claude-sonnet-4-6`
- **Endpoint**: `POST /v1/messages`

**System prompt for `generateSQL`:**
```
You are a SQL expert. The user has a PostgreSQL table called `transactions` with these columns:
date (DATE), description (TEXT), category (TEXT), amount (NUMERIC — negative = expense, positive = income),
account (TEXT), account_number (TEXT), institution (TEXT), month (TEXT), week (TEXT),
transaction_id (TEXT), check_number (TEXT), full_description (TEXT), labels (TEXT), hide (BOOLEAN).

Return a JSON object with two fields:
- "sql": a valid PostgreSQL SELECT query
- "explanation": a plain English explanation of what the query does

Return only valid JSON, no markdown, no code blocks.
```

---

## Retool DB Schema

```sql
CREATE TABLE transactions (
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
  transaction_id TEXT UNIQUE NOT NULL,  -- upsert key
  check_number TEXT,
  full_description TEXT,
  labels TEXT,
  hide BOOLEAN DEFAULT FALSE,
  synced_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE saved_views (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  sql TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Decisions

| # | Decision |
|---|---|
| AI model | REST call to Claude API |
| Saved views | Persist to `saved_views` Retool DB table |
| Sync behavior | Incremental upsert by `transaction_id` |
| Tiller columns | All ~14 columns |
| Pages | Two pages: Query Builder + Summary/Charts |
