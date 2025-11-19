# IT Platform CRM - Data Dictionary

**Database**: PostgreSQL  
**Last Updated**: 2025-10-24  
**Total Tables**: 8

---

## All Tables - Column Reference

| Table Name | Column Name | Data Type | Nullable | Key | Description |
|------------|-------------|-----------|----------|-----|-------------|
| accounts | uid | VARCHAR | No | PK | Unique identifier for the account (Primary Key) |
| accounts | team | VARCHAR | Yes | | Team or group name |
| accounts | business_it_area | VARCHAR | Yes | | Business or IT functional area |
| accounts | vp | VARCHAR | Yes | | Vice President or executive sponsor |
| accounts | team_admin | VARCHAR | Yes | | Team administrator or point of contact |
| accounts | use_case | VARCHAR | Yes | | Primary use case description |
| accounts | use_case_status | VARCHAR | Yes | | Status of the primary use case |
| accounts | databricks | VARCHAR | Yes | | Databricks onboarding status |
| accounts | month_onboarded_db | DATE | Yes | | Month when onboarded to Databricks |
| accounts | snowflake | VARCHAR | Yes | | Snowflake onboarding status |
| accounts | month_onboarded_sf | DATE | Yes | | Month when onboarded to Snowflake |
| accounts | north_star_domain | VARCHAR | Yes | | North star domain or strategic area |
| accounts | business_or_it | VARCHAR | Yes | | Classification as Business or IT team |
| accounts | centerwell_or_insurance | VARCHAR | Yes | | Centerwell or Insurance classification |
| accounts | git_repo | VARCHAR | Yes | | Git repository URL |
| accounts | unique_identifier | VARCHAR | Yes | | Additional unique identifier for the team |
| accounts | associated_ado_items | VARCHAR | Yes | | Associated Azure DevOps work items (URLs or IDs) |
| accounts | team_artifacts | VARCHAR | Yes | | Links to team documentation or artifacts |
| accounts | current_tech_stack | VARCHAR | Yes | | Current technology stack description |
| accounts | ad_groups | VARCHAR | Yes | | Active Directory groups associated with team |
| accounts | notes | VARCHAR | Yes | | General notes about the account |
| accounts | csm | VARCHAR | Yes | | Customer Success Manager assigned |
| accounts | health | VARCHAR | Yes | | Account health status (Green/Yellow/Red) |
| accounts | health_reason | VARCHAR | Yes | | Explanation for current health status |
| use_cases | id | INTEGER | No | PK | Auto-incrementing primary key |
| use_cases | account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| use_cases | problem | VARCHAR | Yes | | Problem statement or business challenge |
| use_cases | solution | VARCHAR | Yes | | Solution description |
| use_cases | value | VARCHAR | Yes | | Business value or expected outcome |
| use_cases | leader | VARCHAR | Yes | | Use case leader or owner |
| use_cases | status | VARCHAR | Yes | | Current status of the use case |
| use_cases | enablement_tier | VARCHAR | Yes | | Enablement tier (e.g., Self-Service, Guided, Managed) |
| use_cases | platform | VARCHAR | Yes | | Platform used for this use case (Databricks, Snowflake, etc.) |
| updates | id | INTEGER | No | PK | Auto-incrementing primary key |
| updates | account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| updates | description | VARCHAR | Yes | | Update description or activity note |
| updates | author | VARCHAR | Yes | | Person who created the update |
| updates | platform | VARCHAR | Yes | | Platform related to this update |
| updates | date | DATE | Yes | | Date of the update |
| platforms_crm | id | INTEGER | No | PK | Auto-incrementing primary key |
| platforms_crm | account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| platforms_crm | platform_name | VARCHAR | Yes | | Platform name (Databricks, Snowflake, Power Platform, Fabric) |
| platforms_crm | onboarding_status | VARCHAR | Yes | | Onboarding status for this platform |
| primary_it_partners | id | INTEGER | No | PK | Auto-incrementing primary key |
| primary_it_partners | account_uid | VARCHAR | No | FK | Foreign key to accounts.uid |
| primary_it_partners | primary_it_partner | VARCHAR | Yes | | Name of the primary IT partner assigned to the account |
| intake_requests | id | INTEGER | No | PK | Auto-incrementing primary key |
| intake_requests | title | VARCHAR | No | | Short title/summary of the request |
| intake_requests | description | VARCHAR | Yes | | Detailed description of the request |
| intake_requests | has_it_partner | BOOLEAN | No | | Whether the requester has an IT partner (default: false) |
| intake_requests | dri_contact | VARCHAR | Yes | | Directly Responsible Individual contact information |
| intake_requests | submitted_for | VARCHAR | Yes | | Team or person the request is submitted for |
| intake_requests | functional_area | VARCHAR | Yes | | Functional area (Finance, Marketing, Sales, Operations, HR, IT, Product, Engineering, Customer Success, Legal, R&D, Supply Chain) |
| intake_requests | help_types | VARCHAR | Yes | | JSON array of help types (consultation, build, new_environment, enhancement, cloud_storage) |
| intake_requests | platform | VARCHAR | Yes | | Target platform (Databricks, Snowflake, Power Platform, Fabric) |
| intake_requests | additional_details | TEXT | Yes | | JSON object containing conditional form responses based on help_types |
| intake_requests | created_at | TIMESTAMP | No | | Timestamp when request was created (auto-generated UTC) |
| intake_requests | updated_at | TIMESTAMP | No | | Timestamp when request was last updated (auto-generated UTC) |
| request_states | id | INTEGER | No | PK | Auto-incrementing primary key |
| request_states | name | VARCHAR | No | | State name (e.g., New, In Progress, Completed) |
| request_states | color | VARCHAR | Yes | | Hex color code for UI display (e.g., #10b981) |
| request_states | description | VARCHAR | Yes | | Description of what this state represents |
| request_states | created_at | TIMESTAMP | No | | Timestamp when state was created (auto-generated UTC) |
| request_state_assignments | id | INTEGER | No | PK | Auto-incrementing primary key |
| request_state_assignments | request_id | INTEGER | No | FK | Foreign key to intake_requests.id |
| request_state_assignments | state_id | INTEGER | No | FK | Foreign key to request_states.id |
| request_state_assignments | assigned_at | TIMESTAMP | No | | Timestamp when state was assigned to request (auto-generated UTC) |

---

## Table Relationships

| Parent Table | Child Table | Relationship Type | Foreign Key | Description |
|--------------|-------------|-------------------|-------------|-------------|
| accounts | use_cases | One-to-Many | use_cases.account_uid | One account has many use cases |
| accounts | updates | One-to-Many | updates.account_uid | One account has many updates |
| accounts | platforms_crm | One-to-Many | platforms_crm.account_uid | One account has many platform records |
| accounts | primary_it_partners | One-to-One | primary_it_partners.account_uid | One account has one primary IT partner |
| intake_requests | request_state_assignments | One-to-Many | request_state_assignments.request_id | One request can have many state assignments |
| request_states | request_state_assignments | One-to-Many | request_state_assignments.state_id | One state can be assigned to many requests |
| intake_requests | request_states | Many-to-Many | Via request_state_assignments | Requests and states have many-to-many relationship |

---

## Additional Details JSON Schema (intake_requests.additional_details)

| Help Type | Field Name | Data Type | Description |
|-----------|------------|-----------|-------------|
| consultation | consultation_help_with | JSON Array | Array of consultation topics selected |
| consultation | use_case_details | Text | Detailed description of use case |
| new_environment | env_preferences | JSON Array | Environment preferences (ASA, Databricks, Prefect, Snowflake) |
| new_environment | languages | JSON Array | Languages needed (SQL, Python, Other) |
| new_environment | other_language | Text | Other language specification if selected |
| new_environment | primary_function | JSON Array | Primary functions (Analytics/Reporting, Machine Learning, ETL/ELT, Workflow Orchestration) |
| new_environment | integrations_text | Text | Description of integration needs |
| enhancement | environment_name | Text | Name of environment to enhance |
| enhancement | platform_preferences | JSON Array | Platform preferences for enhancement |
| enhancement | integrations_description | Text | Description of integration needs |
| enhancement | asa_spark_pool | JSON Array | Spark Pool operations (Create, Delete) |
| enhancement | asa_dedicated_sql_pool | JSON Array | Dedicated SQL Pool operations (Create, Delete) |
| enhancement | asa_shir | JSON Array | SHIR operations (Create, Delete, Scale) |
| enhancement | asa_manage_access | JSON Array | Access management needs (Dedicated SQL Pool Schema, Pipeline, Dataflow) |
| enhancement | asa_other_resources | Text | Other ASA resource needs description |
| cloud_storage | describe_data | Text | Description of data to store |
| cloud_storage | who_accessing | Text | Description of who needs access to data |
| cloud_storage | how_consumed | Text | Description of how data will be consumed |

---

## Reference Data Values

### Functional Areas (intake_requests.functional_area)

| Value |
|-------|
| Finance |
| Marketing |
| Sales |
| Operations |
| HR |
| IT |
| Product |
| Engineering |
| Customer Success |
| Legal |
| R&D |
| Supply Chain |

### Platforms

| Value |
|-------|
| Databricks |
| Snowflake |
| Power Platform |
| Fabric |

### Help Types (intake_requests.help_types)

| Value | Display Label |
|-------|---------------|
| consultation | Consultation/Questions |
| build | Build Something |
| new_environment | New Environment |
| enhancement | Environment Enhancement |
| cloud_storage | Cloud Storage for Downstream Consumers |

### Default Request States

| Name | Color | Description |
|------|-------|-------------|
| New | #6b7280 | Initial state for new requests |
| In Review | #3b82f6 | Request is being reviewed |
| Assigned | #8b5cf6 | Request has been assigned to someone |
| In Progress | #eab308 | Work is in progress |
| Blocked | #ef4444 | Request is blocked |
| Completed | #10b981 | Request is complete |
| Rejected | #f97316 | Request was rejected |

---

## Notes

- **Cascade Deletions**: When an account is deleted, all related records in use_cases, updates, platforms_crm, and primary_it_partners are manually deleted by the application
- **JSON Fields**: The help_types and additional_details fields in intake_requests store JSON data as VARCHAR/TEXT
- **Timestamps**: All timestamp fields use UTC timezone (datetime.utcnow())
- **Optional Fields**: Most fields are nullable to allow flexibility in data entry
- **Primary Keys**: All tables use auto-incrementing integer PKs except accounts which uses a string UID
- **Audit Trail**: intake_requests and request_state_assignments include timestamp fields for tracking
