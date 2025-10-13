import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { accountsApi } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import { ArrowLeft } from 'lucide-react';

export function EditAccount() {
  const { uid } = useParams<{ uid: string }>();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    uid: '',
    team: '',
    business_it_area: '',
    vp: '',
    team_admin: '',
    use_case: '',
    use_case_status: '',
    databricks: '',
    month_onboarded_db: '',
    snowflake: '',
    month_onboarded_sf: '',
    north_star_domain: '',
    business_or_it: '',
    centerwell_or_insurance: '',
    git_repo: '',
    unique_identifier: '',
    associated_ado_items: '',
    team_artifacts: '',
    current_tech_stack: '',
    ad_groups: '',
    notes: '',
    csm: '',
    health: '',
    health_reason: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (uid) {
      loadAccount(uid);
    }
  }, [uid]);

  const loadAccount = async (accountUid: string) => {
    try {
      const response = await accountsApi.getOne(accountUid);
      const account = response.data;
      setFormData({
        uid: account.uid || '',
        team: account.team || '',
        business_it_area: account.business_it_area || '',
        vp: account.vp || '',
        team_admin: account.team_admin || '',
        use_case: account.use_case || '',
        use_case_status: account.use_case_status || '',
        databricks: account.databricks || '',
        month_onboarded_db: account.month_onboarded_db || '',
        snowflake: account.snowflake || '',
        month_onboarded_sf: account.month_onboarded_sf || '',
        north_star_domain: account.north_star_domain || '',
        business_or_it: account.business_or_it || '',
        centerwell_or_insurance: account.centerwell_or_insurance || '',
        git_repo: account.git_repo || '',
        unique_identifier: account.unique_identifier || '',
        associated_ado_items: account.associated_ado_items || '',
        team_artifacts: account.team_artifacts || '',
        current_tech_stack: account.current_tech_stack || '',
        ad_groups: account.ad_groups || '',
        notes: account.notes || '',
        csm: account.csm || '',
        health: account.health || '',
        health_reason: account.health_reason || '',
      });
    } catch (error) {
      console.error('Error loading account:', error);
      alert('Failed to load account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uid) return;
    
    setSaving(true);
    try {
      await accountsApi.update(uid, formData);
      navigate(`/accounts/${uid}`);
    } catch (error) {
      console.error('Error updating account:', error);
      alert('Failed to update account. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading account...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate(`/accounts/${uid}`)}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold">Edit Account</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="uid" className="block text-sm font-medium mb-1">
                  UID
                </label>
                <Input
                  id="uid"
                  name="uid"
                  value={formData.uid}
                  disabled
                  className="bg-muted"
                />
              </div>
              <div>
                <label htmlFor="unique_identifier" className="block text-sm font-medium mb-1">
                  Unique Identifier
                </label>
                <Input
                  id="unique_identifier"
                  name="unique_identifier"
                  value={formData.unique_identifier}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="team" className="block text-sm font-medium mb-1">
                  Team
                </label>
                <Input
                  id="team"
                  name="team"
                  value={formData.team}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="business_it_area" className="block text-sm font-medium mb-1">
                  Business/IT Area
                </label>
                <Input
                  id="business_it_area"
                  name="business_it_area"
                  value={formData.business_it_area}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="vp" className="block text-sm font-medium mb-1">
                  VP
                </label>
                <Input
                  id="vp"
                  name="vp"
                  value={formData.vp}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="team_admin" className="block text-sm font-medium mb-1">
                  Team Admin
                </label>
                <Input
                  id="team_admin"
                  name="team_admin"
                  value={formData.team_admin}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="csm" className="block text-sm font-medium mb-1">
                  CSM
                </label>
                <Input
                  id="csm"
                  name="csm"
                  value={formData.csm}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="health" className="block text-sm font-medium mb-1">
                  Health
                </label>
                <select
                  id="health"
                  name="health"
                  value={formData.health}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="Green">Green</option>
                  <option value="Yellow">Yellow</option>
                  <option value="Red">Red</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label htmlFor="health_reason" className="block text-sm font-medium mb-1">
                  Health Reason
                </label>
                <Input
                  id="health_reason"
                  name="health_reason"
                  value={formData.health_reason}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="north_star_domain" className="block text-sm font-medium mb-1">
                  North Star Domain
                </label>
                <Input
                  id="north_star_domain"
                  name="north_star_domain"
                  value={formData.north_star_domain}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="business_or_it" className="block text-sm font-medium mb-1">
                  Business or IT
                </label>
                <select
                  id="business_or_it"
                  name="business_or_it"
                  value={formData.business_or_it}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="Business">Business</option>
                  <option value="IT">IT</option>
                </select>
              </div>
              <div>
                <label htmlFor="centerwell_or_insurance" className="block text-sm font-medium mb-1">
                  Centerwell or Insurance
                </label>
                <select
                  id="centerwell_or_insurance"
                  name="centerwell_or_insurance"
                  value={formData.centerwell_or_insurance}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="Centerwell">Centerwell</option>
                  <option value="Insurance">Insurance</option>
                </select>
              </div>
              <div>
                <label htmlFor="use_case" className="block text-sm font-medium mb-1">
                  Use Case
                </label>
                <Input
                  id="use_case"
                  name="use_case"
                  value={formData.use_case}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="use_case_status" className="block text-sm font-medium mb-1">
                  Use Case Status
                </label>
                <select
                  id="use_case_status"
                  name="use_case_status"
                  value={formData.use_case_status}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="Planning">Planning</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
              <div>
                <label htmlFor="databricks" className="block text-sm font-medium mb-1">
                  Databricks
                </label>
                <select
                  id="databricks"
                  name="databricks"
                  value={formData.databricks}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="y">Yes</option>
                  <option value="n">No</option>
                </select>
              </div>
              <div>
                <label htmlFor="month_onboarded_db" className="block text-sm font-medium mb-1">
                  Month Onboarded (Databricks)
                </label>
                <Input
                  id="month_onboarded_db"
                  name="month_onboarded_db"
                  type="date"
                  value={formData.month_onboarded_db}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="snowflake" className="block text-sm font-medium mb-1">
                  Snowflake
                </label>
                <select
                  id="snowflake"
                  name="snowflake"
                  value={formData.snowflake}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select...</option>
                  <option value="y">Yes</option>
                  <option value="n">No</option>
                </select>
              </div>
              <div>
                <label htmlFor="month_onboarded_sf" className="block text-sm font-medium mb-1">
                  Month Onboarded (Snowflake)
                </label>
                <Input
                  id="month_onboarded_sf"
                  name="month_onboarded_sf"
                  type="date"
                  value={formData.month_onboarded_sf}
                  onChange={handleChange}
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="current_tech_stack" className="block text-sm font-medium mb-1">
                  Current Tech Stack
                </label>
                <Input
                  id="current_tech_stack"
                  name="current_tech_stack"
                  value={formData.current_tech_stack}
                  onChange={handleChange}
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="ad_groups" className="block text-sm font-medium mb-1">
                  AD Groups
                </label>
                <Input
                  id="ad_groups"
                  name="ad_groups"
                  value={formData.ad_groups}
                  onChange={handleChange}
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="git_repo" className="block text-sm font-medium mb-1">
                  Git Repository
                </label>
                <Input
                  id="git_repo"
                  name="git_repo"
                  type="url"
                  value={formData.git_repo}
                  onChange={handleChange}
                  placeholder="https://github.com/..."
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="associated_ado_items" className="block text-sm font-medium mb-1">
                  ADO Items
                </label>
                <Input
                  id="associated_ado_items"
                  name="associated_ado_items"
                  type="url"
                  value={formData.associated_ado_items}
                  onChange={handleChange}
                  placeholder="https://dev.azure.com/..."
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="team_artifacts" className="block text-sm font-medium mb-1">
                  Team Artifacts
                </label>
                <Input
                  id="team_artifacts"
                  name="team_artifacts"
                  type="url"
                  value={formData.team_artifacts}
                  onChange={handleChange}
                  placeholder="https://..."
                />
              </div>
              <div className="md:col-span-2">
                <label htmlFor="notes" className="block text-sm font-medium mb-1">
                  Notes
                </label>
                <textarea
                  id="notes"
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  rows={3}
                  className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                />
              </div>
            </div>
            <div className="flex justify-end gap-4 mt-6">
              <Button type="button" variant="outline" onClick={() => navigate(`/accounts/${uid}`)}>
                Cancel
              </Button>
              <Button type="submit" disabled={saving}>
                {saving ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
