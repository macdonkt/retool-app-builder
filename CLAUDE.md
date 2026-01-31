# Retool App Builder

Build production-ready Retool apps from natural language instructions. Output valid JSON files for direct import into Retool.

## Output Format

Save all generated files to the `apps/` folder.

When building apps, always output:

1. **Primary**: `apps/{app-name}.json` - Clean, valid JSON ready for Retool import
   - No comments (JSON doesn't support them)
   - Complete app structure: components, queries, event handlers, pages, modules
   - Standard components only unless custom components are specified

2. **Secondary** (when needed): `apps/{app-name}-instructions.md` - Setup documentation for:
   - Workflow creation steps (workflows can't be included in app JSON)
   - Resource/data source configuration
   - External dependencies or permissions
   - Post-import configuration steps

If no workflows or external setup is needed, output only the JSON.

## Critical Rules

- **Never edit production apps directly** - Always duplicate for testing
- **Validate JSON before import** - Ensure structure is complete and valid
- **Avoid legacy components** - Use current components for security/features
- **Handle errors** - Include error states in event handlers
- **Test with sample data** - Verify bindings work before deployment

## Resources

- **JSON Reference**: See `RETOOL_JSON_REFERENCE.md` for complete technical specs (Transit encoding, widget templates, query types, positioning, event handlers)
- **Retool Docs**: https://docs.retool.com
- **LLM-Optimized Docs**: https://docs.retool.com/llms.txt
- **Retool CLI**: https://github.com/tryretool/retool-cli (export/import apps)
- **Components**: 100+ UI elements (tables, forms, charts, inputs, modals, etc.)
- **Queries**: REST, GraphQL, SQL/NoSQL, JavaScript transformers, AI integrations

**Important**: Always consult `RETOOL_JSON_REFERENCE.md` when planning and building apps for correct JSON structure, widget types, and Transit encoding format.

## App Patterns

### CRUD Dashboard
Table + forms for data management with filters, modals, and actions.

**Example request**:
"Generate a Retool app JSON for a product management dashboard:
- Table showing products from `get_products` query (columns: id, name, price, stock)
- Filters for name search and price range
- Add/Edit modals with form validation
- Delete button with confirmation
- Success notifications and refresh functionality"

### Form with Validation
Input collection with validation rules, submission handling, and feedback.

**Example request**:
"Generate a Retool app JSON for a customer feedback form:
- Text input (name), email input, textarea (feedback), rating selector (1-5)
- Validation: required fields, email format check
- Submit triggers `submit_feedback` query
- Success toast and form reset on completion"

### AI Integration
User input processed by LLM with results display and history tracking.

**Example request**:
"Generate a Retool app JSON for an AI text analyzer:
- Textarea for user input
- Button triggers `analyze_text` AI query for sentiment/keywords
- Results displayed in formatted text component
- Loading states and error handling
- History table from `get_history` query"

### Multi-Page App
Navigation between pages with URL params for state management.

### Mobile App
Native mobile components with camera, GPS, offline support.

## Requirements Gathering

Before building, clarify these details:

1. **Purpose**: What does the app do? (dashboard, form, reporting, automation)
   - Web, mobile, or both?
   - Specific pattern preference?

2. **Data Sources**:
   - What databases/APIs? (Postgres, REST, Google Sheets, etc.)
   - Key queries needed? (fetch, create, update, delete)
   - Sample columns/fields?

3. **UI Components**:
   - Main components? (tables, forms, charts, modals)
   - Layout structure? (single page, multi-page, modules)
   - Mobile-specific features?

4. **Interactions**:
   - User actions and buttons?
   - Validation rules?
   - Conditional logic? (show/hide based on role/state)

5. **Integrations**:
   - AI/LLM features?
   - External APIs or notifications?
   - Retool Workflows needed?

6. **Testing**:
   - Sample data available?
   - Edge cases to handle?

## Workflow Dependencies

Retool Workflows are separate backend automations - they cannot be included in app JSON exports.

When an app requires workflows:

1. **In the JSON**: Include queries that reference the workflow by name
2. **In the instructions markdown**: Provide step-by-step setup:
   - Navigate to Retool Workflows in UI
   - Create workflow matching the referenced name
   - Configure triggers (HTTP, schedule, etc.)
   - Add action blocks (queries, JS/Python code, branches)
   - Set inputs/outputs to match app query parameters
   - Test integration and verify in workflow logs

Common workflow triggers: form submissions, scheduled syncs, external webhooks, complex multi-step automations.

## Technical Notes

**Data Binding**:
- Use `{{ }}` for dynamic values
- Access query data: `queryName.data`
- Ensure queries run before components bind to them

**JSON Export Limitations**:
- Runtime state may not persist
- Custom components must exist in target instance
- Very new features may lag in export support

**Mobile Considerations**:
- Platform-specific permissions required
- Test with Retool Mobile preview
- Hardware integrations (camera, GPS) need explicit setup

**Performance**:
- Use query caching for frequently accessed data
- Implement server-side pagination for large datasets
- Monitor AI/LLM usage costs
