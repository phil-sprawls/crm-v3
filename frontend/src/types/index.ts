export interface Account {
  uid: string;
  team?: string;
  business_it_area?: string;
  vp?: string;
  team_admin?: string;
  use_case?: string;
  use_case_status?: string;
  databricks?: string;
  month_onboarded_db?: string;
  snowflake?: string;
  month_onboarded_sf?: string;
  north_star_domain?: string;
  business_or_it?: string;
  centerwell_or_insurance?: string;
  git_repo?: string;
  unique_identifier?: string;
  associated_ado_items?: string;
  team_artifacts?: string;
  current_tech_stack?: string;
  ad_groups?: string;
  notes?: string;
  csm?: string;
  health?: string;
  health_reason?: string;
}

export interface UseCase {
  id?: number;
  account_uid: string;
  problem?: string;
  solution?: string;
  value?: string;
  leader?: string;
  status?: string;
  enablement_tier?: string;
  platform?: string;
}

export interface Update {
  id?: number;
  account_uid: string;
  description?: string;
  author?: string;
  platform?: string;
  date?: string;
}

export interface Platform {
  id?: number;
  account_uid: string;
  platform_name?: string;
  onboarding_status?: string;
}

export interface PrimaryITPartner {
  id?: number;
  account_uid: string;
  primary_it_partner?: string;
}
