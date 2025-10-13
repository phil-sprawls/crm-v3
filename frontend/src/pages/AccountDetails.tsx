import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Account, UseCase, Update, Platform, PrimaryITPartner } from '../types';
import { accountsApi } from '../lib/api';
import { Button } from '../components/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import { ArrowLeft } from 'lucide-react';

export function AccountDetails() {
  const { uid } = useParams<{ uid: string }>();
  const navigate = useNavigate();
  const [account, setAccount] = useState<Account | null>(null);
  const [useCases, setUseCases] = useState<UseCase[]>([]);
  const [updates, setUpdates] = useState<Update[]>([]);
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [primaryITPartner, setPrimaryITPartner] = useState<PrimaryITPartner | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (uid) {
      loadAccountData(uid);
    }
  }, [uid]);

  const loadAccountData = async (accountUid: string) => {
    try {
      const [accountRes, useCasesRes, updatesRes, platformsRes] = await Promise.all([
        accountsApi.getOne(accountUid),
        accountsApi.getUseCases(accountUid),
        accountsApi.getUpdates(accountUid),
        accountsApi.getPlatforms(accountUid),
      ]);

      setAccount(accountRes.data);
      setUseCases(useCasesRes.data);
      setUpdates(updatesRes.data);
      setPlatforms(platformsRes.data);

      try {
        const partnerRes = await accountsApi.getPrimaryITPartner(accountUid);
        setPrimaryITPartner(partnerRes.data);
      } catch (error) {
        console.log('No primary IT partner found');
      }
    } catch (error) {
      console.error('Error loading account data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading account details...</div>;
  }

  if (!account) {
    return <div className="text-center py-8">Account not found</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold">{account.team}</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">UID</label>
              <p className="text-sm">{account.uid}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Team</label>
              <p className="text-sm">{account.team || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Business/IT Area</label>
              <p className="text-sm">{account.business_it_area || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">VP</label>
              <p className="text-sm">{account.vp || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Team Admin</label>
              <p className="text-sm">{account.team_admin || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Primary IT Partner</label>
              <p className="text-sm">{primaryITPartner?.primary_it_partner || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">CSM</label>
              <p className="text-sm">{account.csm || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Health</label>
              <p className="text-sm">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                  account.health === 'Green' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  account.health === 'Yellow' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                  account.health === 'Red' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                  'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                }`}>
                  {account.health || '-'}
                </span>
              </p>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-muted-foreground">Health Reason</label>
              <p className="text-sm">{account.health_reason || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Business or IT</label>
              <p className="text-sm">{account.business_or_it || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Centerwell or Insurance</label>
              <p className="text-sm">{account.centerwell_or_insurance || '-'}</p>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-muted-foreground">Current Tech Stack</label>
              <p className="text-sm">{account.current_tech_stack || '-'}</p>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium text-muted-foreground">Notes</label>
              <p className="text-sm">{account.notes || '-'}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Platforms</CardTitle>
        </CardHeader>
        <CardContent>
          {platforms.length > 0 ? (
            <div className="space-y-2">
              {platforms.map((platform) => (
                <div key={platform.id} className="flex justify-between items-center p-3 border rounded-lg">
                  <span className="font-medium">{platform.platform_name}</span>
                  <span className="text-sm text-muted-foreground">{platform.onboarding_status}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground">No platforms configured</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Use Cases</CardTitle>
        </CardHeader>
        <CardContent>
          {useCases.length > 0 ? (
            <div className="space-y-4">
              {useCases.map((useCase) => (
                <div key={useCase.id} className="border-l-4 border-primary pl-4 py-2">
                  <h4 className="font-medium">{useCase.problem}</h4>
                  <p className="text-sm text-muted-foreground mt-1">{useCase.solution}</p>
                  <div className="mt-2 flex gap-4 text-xs text-muted-foreground">
                    <span>Status: {useCase.status}</span>
                    <span>Platform: {useCase.platform}</span>
                    <span>Leader: {useCase.leader}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground">No use cases defined</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Recent Updates</CardTitle>
        </CardHeader>
        <CardContent>
          {updates.length > 0 ? (
            <div className="space-y-3">
              {updates.map((update) => (
                <div key={update.id} className="p-3 bg-muted rounded-lg">
                  <p className="text-sm">{update.description}</p>
                  <div className="mt-2 flex justify-between text-xs text-muted-foreground">
                    <span>By: {update.author}</span>
                    <span>{update.date ? new Date(update.date).toLocaleDateString() : '-'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground">No updates available</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
