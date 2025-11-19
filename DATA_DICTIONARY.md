# IT Platform CRM - Data Dictionary

**Database**: PostgreSQL  
**Last Updated**: 2025-10-24  
**Total Tables**: 8

---

## Table of Contents
1. [accounts](#1-accounts)
2. [use_cases](#2-use_cases)
3. [updates](#3-updates)
4. [platforms_crm](#4-platforms_crm)
5. [primary_it_partners](#5-primary_it_partners)
6. [intake_requests](#6-intake_requests)
7. [request_states](#7-request_states)
8. [request_state_assignments](#8-request_state_assignments)
9. [Relationships Diagram](#relationships-diagram)

---

## 1. accounts

**Purpose**: Main table storing team/account information for platform onboarding tracking.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| uid | VARCHAR | No | PK | Unique identifier for the account (Primary Key) |
| team | VARCHAR | Yes | | Team or group name |
| business_it_area | VARCHAR | Yes | | Business or IT functional area |
| vp | VARCHAR | Yes | | Vice President or executive sponsor |
| team_admin | VARCHAR | Yes | | Team administrator or point of contact |
| use_case | VARCHAR | Yes | | Primary use case description |
| use_case_status | VARCHAR | Yes | | Status of the primary use case |
| databricks | VARCHAR | Yes | | Databricks onboarding status |
| month_onboarded_db | DATE | Yes | | Month when onboarded to Databricks |
| snowflake | VARCHAR | Yes | | Snowflake onboarding status |
| month_onboarded_sf | DATE | Yes | | Month when onboarded to Snowflake |
| north_star_domain | VARCHAR | Yes | | North star domain or strategic area |
| business_or_it | VARCHAR | Yes | | Classification as Business or IT team |
| centerwell_or_insurance | VARCHAR | Yes | | Centerwell or Insurance classification |
| git_repo | VARCHAR | Yes | | Git repository URL |
| unique_identifier | VARCHAR | Yes | | Additional unique identifier for the team |
| associated_ado_items | VARCHAR | Yes | | Associated Azure DevOps work items (URLs or IDs) |
| team_artifacts | VARCHAR | Yes | | Links to team documentation or artifacts |
| current_tech_stack | VARCHAR | Yes | | Current technology stack description |
| ad_groups | VARCHAR | Yes | | Active Directory groups associated with team |
| notes | VARCHAR | Yes | | General notes about the account |
| csm | VARCHAR | Yes | | Customer Success Manager assigned |
| health | VARCHAR | Yes | | Account health status (Green/Yellow/Red) |
| health_reason | VARCHAR | Yes | | Explanation for current health status |

**Relationships**:
- **One-to-Many** with `use_cases` (one account has many use cases)
- **One-to-Many** with `updates` (one account has many updates)
- **One-to-Many** with `platforms_crm` (one account has many platform onboarding records)
- **One-to-One** with `primary_it_partners` (one account has one primary IT partner)

---

## 2. use_cases

**Purpose**: Stores individual use cases associated with accounts.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| problem | VARCHAR | Yes | | Problem statement or business challenge |
| solution | VARCHAR | Yes | | Solution description |
| value | VARCHAR | Yes | | Business value or expected outcome |
| leader | VARCHAR | Yes | | Use case leader or owner |
| status | VARCHAR | Yes | | Current status of the use case |
| enablement_tier | VARCHAR | Yes | | Enablement tier (e.g., Self-Service, Guided, Managed) |
| platform | VARCHAR | Yes | | Platform used for this use case (Databricks, Snowflake, etc.) |

**Joins**:
```sql
-- Get all use cases for an account
SELECT * FROM use_cases WHERE account_uid = 'ACCOUNT_UID';

-- Get use cases with account details
SELECT u.*, a.team, a.vp 
FROM use_cases u
JOIN accounts a ON u.account_uid = a.uid;
```

---

## 3. updates

**Purpose**: Stores activity updates and progress notes for accounts.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| description | VARCHAR | Yes | | Update description or activity note |
| author | VARCHAR | Yes | | Person who created the update |
| platform | VARCHAR | Yes | | Platform related to this update |
| date | DATE | Yes | | Date of the update |

**Joins**:
```sql
-- Get all updates for an account
SELECT * FROM updates WHERE account_uid = 'ACCOUNT_UID' ORDER BY date DESC;

-- Get recent updates across all accounts
SELECT u.*, a.team 
FROM updates u
JOIN accounts a ON u.account_uid = a.uid
ORDER BY u.date DESC;
```

---

## 4. platforms_crm

**Purpose**: Tracks platform onboarding status for each account (renamed to avoid conflicts with existing database tables).

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| platform_name | VARCHAR | Yes | | Platform name (Databricks, Snowflake, Power Platform, Fabric) |
| onboarding_status | VARCHAR | Yes | | Onboarding status for this platform |

**Joins**:
```sql
-- Get all platforms for an account
SELECT * FROM platforms_crm WHERE account_uid = 'ACCOUNT_UID';

-- Get all accounts onboarded to Databricks
SELECT a.*, p.onboarding_status 
FROM accounts a
JOIN platforms_crm p ON a.uid = p.account_uid
WHERE p.platform_name = 'Databricks';
```

---

## 5. primary_it_partners

**Purpose**: Stores the primary IT partner assignment for each account.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| primary_it_partner | VARCHAR | Yes | | Name of the primary IT partner assigned to the account |

**Joins**:
```sql
-- Get IT partner for an account
SELECT * FROM primary_it_partners WHERE account_uid = 'ACCOUNT_UID';

-- Get all accounts with their IT partners
SELECT a.team, a.vp, p.primary_it_partner 
FROM accounts a
LEFT JOIN primary_it_partners p ON a.uid = p.account_uid;
```

---

## 6. intake_requests

**Purpose**: Stores intake requests submitted by users for platform help and support.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| title | VARCHAR | No | | Short title/summary of the request |
| description | VARCHAR | Yes | | Detailed description of the request |
| has_it_partner | BOOLEAN | No | | Whether the requester has an IT partner (default: false) |
| dri_contact | VARCHAR | Yes | | Directly Responsible Individual contact information |
| submitted_for | VARCHAR | Yes | | Team or person the request is submitted for |
| functional_area | VARCHAR | Yes | | Functional area (Finance, Marketing, Sales, Operations, etc.) |
| help_types | VARCHAR | Yes | | JSON array of help types (consultation, build, new_environment, enhancement, cloud_storage) |
| platform | VARCHAR | Yes | | Target platform (Databricks, Snowflake, Power Platform, Fabric) |
| additional_details | TEXT | Yes | | JSON object containing conditional form responses based on help_types |
| created_at | TIMESTAMP | No | | Timestamp when request was created (auto-generated) |
| updated_at | TIMESTAMP | No | | Timestamp when request was last updated (auto-generated) |

**Additional Details Schema**: The `additional_details` column stores a JSON object with conditional fields based on `help_types`:

**Consultation Fields**:
- `consultation_help_with`: JSON array of consultation topics
- `use_case_details`: Text description of use case

**New Environment Fields**:
- `env_preferences`: JSON array of environment preferences (ASA, Databricks, Prefect, Snowflake)
- `languages`: JSON array of languages (SQL, Python, Other)
- `other_language`: Text for other language if specified
- `primary_function`: JSON array of primary functions (Analytics/Reporting, Machine Learning, ETL/ELT, Workflow Orchestration)
- `integrations_text`: Text description of integration needs

**Enhancement Fields**:
- `environment_name`: Text name of environment to enhance
- `platform_preferences`: JSON array of platform preferences
- `integrations_description`: Text description of integration needs
- `asa_spark_pool`: JSON array of Spark Pool operations (Create, Delete)
- `asa_dedicated_sql_pool`: JSON array of SQL Pool operations (Create, Delete)
- `asa_shir`: JSON array of SHIR operations (Create, Delete, Scale)
- `asa_manage_access`: JSON array of access management needs
- `asa_other_resources`: Text description of other ASA resources

**Cloud Storage Fields**:
- `describe_data`: Text description of data to store
- `who_accessing`: Text description of who needs access
- `how_consumed`: Text description of how data will be consumed

**Relationships**:
- **Many-to-Many** with `request_states` through `request_state_assignments` (one request can have multiple states)

**Joins**:
```sql
-- Get all requests with their states
SELECT ir.*, rs.name as state_name, rs.color as state_color
FROM intake_requests ir
LEFT JOIN request_state_assignments rsa ON ir.id = rsa.request_id
LEFT JOIN request_states rs ON rsa.state_id = rs.id
ORDER BY ir.created_at DESC;

-- Get requests by functional area
SELECT * FROM intake_requests 
WHERE functional_area = 'Finance' 
ORDER BY created_at DESC;
```

---

## 7. request_states

**Purpose**: Stores customizable workflow states for intake requests (e.g., New, In Progress, Completed).

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| name | VARCHAR | No | | State name (e.g., "New", "In Progress", "Completed") |
| color | VARCHAR | Yes | | Hex color code for UI display (e.g., "#10b981") |
| description | VARCHAR | Yes | | Description of what this state represents |
| created_at | TIMESTAMP | No | | Timestamp when state was created (auto-generated) |

**Default States**:
1. New (gray) - Initial state for new requests
2. In Review (blue) - Request is being reviewed
3. Assigned (purple) - Request has been assigned to someone
4. In Progress (yellow) - Work is in progress
5. Blocked (red) - Request is blocked
6. Completed (green) - Request is complete
7. Rejected (orange) - Request was rejected

**Relationships**:
- **Many-to-Many** with `intake_requests` through `request_state_assignments`

**Joins**:
```sql
-- Get all active states
SELECT * FROM request_states ORDER BY name;

-- Get requests with a specific state
SELECT ir.* 
FROM intake_requests ir
JOIN request_state_assignments rsa ON ir.id = rsa.request_id
JOIN request_states rs ON rsa.state_id = rs.id
WHERE rs.name = 'In Progress';
```

---

## 8. request_state_assignments

**Purpose**: Junction table creating many-to-many relationship between intake requests and request states. Allows multiple states per request and tracks assignment timestamps.

| Column Name | Data Type | Nullable | Key | Description |
|------------|-----------|----------|-----|-------------|
| id | INTEGER | No | PK | Auto-incrementing primary key |
| request_id | INTEGER | No | FK | Foreign key to intake_requests.id |
| state_id | INTEGER | No | FK | Foreign key to request_states.id |
| assigned_at | TIMESTAMP | No | | Timestamp when state was assigned to request (auto-generated) |

**Relationships**:
- **Many-to-One** with `intake_requests` (many assignments belong to one request)
- **Many-to-One** with `request_states` (many assignments use one state)

**Joins**:
```sql
-- Get all states for a specific request
SELECT rs.name, rs.color, rsa.assigned_at
FROM request_state_assignments rsa
JOIN request_states rs ON rsa.state_id = rs.id
WHERE rsa.request_id = 1
ORDER BY rsa.assigned_at DESC;

-- Get all requests with a specific state
SELECT ir.*, rsa.assigned_at
FROM intake_requests ir
JOIN request_state_assignments rsa ON ir.id = rsa.request_id
WHERE rsa.state_id = 3;

-- Remove a state from a request
DELETE FROM request_state_assignments 
WHERE request_id = 1 AND state_id = 2;
```

---

## Relationships Diagram

```
┌─────────────────┐
│    accounts     │
│  (uid: PK)      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────┬─────────┬──────────┐
    │         │         │          │
    ▼         ▼         ▼          ▼
┌─────────┐ ┌────────┐ ┌──────────────┐ ┌─────────────────────┐
│use_cases│ │updates │ │platforms_crm │ │primary_it_partners  │
│         │ │        │ │              │ │                     │
└─────────┘ └────────┘ └──────────────┘ └─────────────────────┘

┌──────────────────┐         ┌─────────────────────────┐         ┌────────────────┐
│intake_requests   │         │request_state_assignments│         │request_states  │
│  (id: PK)        │ ◄───N:M─┤ (junction table)        ├───N:M──►│  (id: PK)      │
└──────────────────┘         └─────────────────────────┘         └────────────────┘
```

**Cardinality Legend**:
- `1:N` = One-to-Many
- `N:M` = Many-to-Many (through junction table)
- `1:1` = One-to-One

---

## Functional Area Values

Standard values for `intake_requests.functional_area`:
- Finance
- Marketing
- Sales
- Operations
- HR
- IT
- Product
- Engineering
- Customer Success
- Legal
- R&D
- Supply Chain

---

## Platform Values

Standard values for platform fields across tables:
- Databricks
- Snowflake
- Power Platform
- Fabric

---

## Help Type Values

Standard values stored in `intake_requests.help_types` (JSON array):
- `consultation` - Consultation/Questions
- `build` - Build Something
- `new_environment` - New Environment Setup
- `enhancement` - Environment Enhancement
- `cloud_storage` - Cloud Storage for Downstream Consumers

---

## Notes

1. **Cascade Deletions**: When an account is deleted, all related records in `use_cases`, `updates`, `platforms_crm`, and `primary_it_partners` are manually deleted by the application.

2. **JSON Fields**: The `help_types` and `additional_details` fields in `intake_requests` store JSON data as VARCHAR/TEXT.

3. **Timestamps**: All timestamp fields use UTC timezone (`datetime.utcnow()`).

4. **Optional Fields**: Most fields are nullable (optional) to allow flexibility in data entry.

5. **Primary Keys**: All tables use auto-incrementing integer primary keys except `accounts` which uses a string UID.

6. **Audit Trail**: `intake_requests` and `request_state_assignments` include timestamp fields for tracking when records were created/assigned.
