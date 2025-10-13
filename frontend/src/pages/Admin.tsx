import { useEffect, useState } from 'react';
import { Account, UseCase, Update, Platform } from '../types';
import { accountsApi, useCasesApi, updatesApi, platformsApi } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';

export function Admin() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccountUid, setSelectedAccountUid] = useState('');
  
  const [newUseCase, setNewUseCase] = useState<Partial<UseCase>>({});
  const [newUpdate, setNewUpdate] = useState<Partial<Update>>({});
  const [newPlatform, setNewPlatform] = useState<Partial<Platform>>({});
  const [accountUpdate, setAccountUpdate] = useState<Partial<Account>>({});

  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    try {
      const response = await accountsApi.getAll();
      setAccounts(response.data);
      if (response.data.length > 0) {
        setSelectedAccountUid(response.data[0].uid);
      }
    } catch (error) {
      console.error('Error loading accounts:', error);
    }
  };

  const handleAddUseCase = async () => {
    if (!selectedAccountUid) return;
    try {
      await useCasesApi.create({ ...newUseCase, account_uid: selectedAccountUid } as UseCase);
      setNewUseCase({});
      alert('Use case added successfully');
    } catch (error) {
      console.error('Error adding use case:', error);
      alert('Failed to add use case');
    }
  };

  const handleAddUpdate = async () => {
    if (!selectedAccountUid) return;
    try {
      await updatesApi.create({ ...newUpdate, account_uid: selectedAccountUid } as Update);
      setNewUpdate({});
      alert('Update added successfully');
    } catch (error) {
      console.error('Error adding update:', error);
      alert('Failed to add update');
    }
  };

  const handleAddPlatform = async () => {
    if (!selectedAccountUid) return;
    try {
      await platformsApi.create({ ...newPlatform, account_uid: selectedAccountUid } as Platform);
      setNewPlatform({});
      alert('Platform added successfully');
    } catch (error) {
      console.error('Error adding platform:', error);
      alert('Failed to add platform');
    }
  };

  const handleUpdateAccount = async () => {
    if (!selectedAccountUid) return;
    try {
      await accountsApi.update(selectedAccountUid, accountUpdate);
      setAccountUpdate({});
      alert('Account updated successfully');
      loadAccounts();
    } catch (error) {
      console.error('Error updating account:', error);
      alert('Failed to update account');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Admin Panel</h1>

      <div className="space-y-2">
        <label className="text-sm font-medium">Select Account</label>
        <select
          className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
          value={selectedAccountUid}
          onChange={(e) => setSelectedAccountUid(e.target.value)}
        >
          {accounts.map((account) => (
            <option key={account.uid} value={account.uid}>
              {account.team} ({account.uid})
            </option>
          ))}
        </select>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Update Account Health</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">CSM</label>
              <Input
                value={accountUpdate.csm || ''}
                onChange={(e) => setAccountUpdate({ ...accountUpdate, csm: e.target.value })}
                placeholder="Enter CSM name"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Health</label>
              <select
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={accountUpdate.health || ''}
                onChange={(e) => setAccountUpdate({ ...accountUpdate, health: e.target.value })}
              >
                <option value="">Select Health</option>
                <option value="Green">Green</option>
                <option value="Yellow">Yellow</option>
                <option value="Red">Red</option>
              </select>
            </div>
          </div>
          <div>
            <label className="text-sm font-medium">Health Reason</label>
            <Input
              value={accountUpdate.health_reason || ''}
              onChange={(e) => setAccountUpdate({ ...accountUpdate, health_reason: e.target.value })}
              placeholder="Enter health reason"
            />
          </div>
          <Button onClick={handleUpdateAccount}>Update Account</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Add Use Case</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Problem</label>
              <Input
                value={newUseCase.problem || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, problem: e.target.value })}
                placeholder="Enter problem statement"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Solution</label>
              <Input
                value={newUseCase.solution || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, solution: e.target.value })}
                placeholder="Enter solution"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Value</label>
              <Input
                value={newUseCase.value || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, value: e.target.value })}
                placeholder="Enter value proposition"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Leader</label>
              <Input
                value={newUseCase.leader || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, leader: e.target.value })}
                placeholder="Enter leader name"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Status</label>
              <Input
                value={newUseCase.status || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, status: e.target.value })}
                placeholder="Enter status"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Platform</label>
              <Input
                value={newUseCase.platform || ''}
                onChange={(e) => setNewUseCase({ ...newUseCase, platform: e.target.value })}
                placeholder="Enter platform"
              />
            </div>
          </div>
          <Button onClick={handleAddUseCase}>Add Use Case</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Add Update</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Description</label>
              <Input
                value={newUpdate.description || ''}
                onChange={(e) => setNewUpdate({ ...newUpdate, description: e.target.value })}
                placeholder="Enter update description"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Author</label>
              <Input
                value={newUpdate.author || ''}
                onChange={(e) => setNewUpdate({ ...newUpdate, author: e.target.value })}
                placeholder="Enter author name"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Platform</label>
              <Input
                value={newUpdate.platform || ''}
                onChange={(e) => setNewUpdate({ ...newUpdate, platform: e.target.value })}
                placeholder="Enter platform"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Date</label>
              <Input
                type="date"
                value={newUpdate.date || ''}
                onChange={(e) => setNewUpdate({ ...newUpdate, date: e.target.value })}
              />
            </div>
          </div>
          <Button onClick={handleAddUpdate}>Add Update</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Add Platform</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Platform Name</label>
              <select
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={newPlatform.platform_name || ''}
                onChange={(e) => setNewPlatform({ ...newPlatform, platform_name: e.target.value })}
              >
                <option value="">Select Platform</option>
                <option value="Databricks">Databricks</option>
                <option value="Snowflake">Snowflake</option>
                <option value="Power Platform">Power Platform</option>
                <option value="Fabric">Fabric</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Onboarding Status</label>
              <select
                className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={newPlatform.onboarding_status || ''}
                onChange={(e) => setNewPlatform({ ...newPlatform, onboarding_status: e.target.value })}
              >
                <option value="">Select Status</option>
                <option value="Not Started">Not Started</option>
                <option value="Planning">Planning</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
              </select>
            </div>
          </div>
          <Button onClick={handleAddPlatform}>Add Platform</Button>
        </CardContent>
      </Card>
    </div>
  );
}
