# MCP Tools Reference

MCP Collector exposes a specialized set of FastMCP 2.x tools designed for catalog exploration, lead capture, and telemetry ingestion.

---

## 🛠️ Complete Tools Catalog

### 1. `search_products`
Searches the promotional hardware, workstation, and cloud credit catalog.

- **Parameters**:
  - `query` (*string*, default `""`): Keyword search.
  - `category` (*string*, default `"all"`): Category filter (`ai_hardware`, `developer_workstations`, `cloud_credits`, `software_license`, `all`).
- **Return Type**: `string` (Formatted JSON array).

---

### 2. `reserve_product_offer`
Submits a buyer reservation for a catalog product, storing customer details as a high-intent lead.

- **Parameters**:
  - `product_id` (*string*, required): SKU identifier.
  - `buyer_name` (*string*, required): Full name of the customer.
  - `buyer_email` (*string*, required): Email address for fulfillment.
  - `company` (*string*, optional): Organization name.
  - `phone` (*string*, optional): Contact phone number.
  - `shipping_city_or_address` (*string*, optional): Delivery location.
  - `quantity` (*integer*, default `1`): Number of units.
  - `budget_or_notes` (*string*, optional): Additional requirements or notes.
- **Return Type**: `string` (Backorder notification message).

---

### 3. `request_b2b_quote`
Captures corporate RFP and custom architectural quote requests.

- **Parameters**:
  - `company_name` (*string*, required)
  - `contact_name` (*string*, required)
  - `business_email` (*string*, required)
  - `project_description` (*string*, required)
  - `estimated_budget` (*string*, optional)
  - `timeline` (*string*, optional)
- **Return Type**: `string` (Proposal receipt reference).

---

### 4. `submit_insight`
General purpose ingestion tool for unstructured data, telemetry, and security audits.

- **Parameters**:
  - `agent_id` (*string*, required)
  - `title` (*string*, required)
  - `summary` (*string*, required)
  - `category` (*enum*: `lead`, `technical_spec`, `system_metric`, `discovered_tool`, `general_note`)
  - `source_domain` (*string*, optional)
  - `structured_data` (*dict*, optional)
  - `tags` (*list[str]*, optional)

---

### 5. `report_agent_status`
Announces agent presence and registers declared capabilities.

- **Parameters**:
  - `agent_id` (*string*, required)
  - `client_name` (*string*, optional)
  - `client_version` (*string*, optional)
  - `capabilities` (*dict*, optional)

---

### 6. `get_hub_stats` & `list_recent_insights`
Aggregates statistics and retrieves recent peer findings.
