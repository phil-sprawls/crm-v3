import { useEffect, useState } from 'react';
import { Account, UseCase, Update, Platform } from '../types';
import { accountsApi, useCasesApi, updatesApi, platformsApi } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';

export function Admin() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccountUid, setSelectedAccountUid] = useState('');
  
  const [useCases, setUseCases] = useState<UseCase[]>([]);
  const [updates, setUpdates] = useState<Update[]>([]);
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  
  const [newUseCase, setNewUseCase] = useState<Partial<UseCase>>({});
  const [newUpdate, setNewUpdate] = useState<Partial<Update>>({});
  const [newPlatform, setNewPlatform] = useState<Partial<Platform>>({});
  const [accountUpdate, setAccountUpdate] = useState<Partial<Account>>({});

  const [editingUseCase, setEditingUseCase] = useState<UseCase | null>(null);
  const [editingUpdate, setEditingUpdate] = useState<Update | null>(null);
  const [editingPlatform, setEditingPlatform] = useState<Platform | null>(null);

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (selectedAccountUid) {
      loadAccountData();
    }
  }, [selectedAccountUid]);

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

  const loadAccountData = async () => {
    if (!selectedAccountUid) return;
    try {
      const [useCasesRes, updatesRes, platformsRes] = await Promise.all([
        accountsApi.getUseCases(selectedAccountUid),
        accountsApi.getUpdates(selectedAccountUid),
        accountsApi.getPlatforms(selectedAccountUid)
      ]);
      setUseCases(useCasesRes.data);
      setUpdates(updatesRes.data);
      setPlatforms(platformsRes.data);
    } catch (error) {
      console.error('Error loading account data:', error);
    }
  };

  const handleAddUseCase = async () => {
    if (!selectedAccountUid) return;
    try {
      await useCasesApi.create({ ...newUseCase, account_uid: selectedAccountUid } as UseCase);
      setNewUseCase({});
      alert('Use case added successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error adding use case:', error);
      alert('Failed to add use case');
    }
  };

  const handleUpdateUseCase = async () => {
    if (!editingUseCase || !editingUseCase.id) return;
    try {
      await useCasesApi.update(editingUseCase.id, editingUseCase);
      setEditingUseCase(null);
      alert('Use case updated successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error updating use case:', error);
      alert('Failed to update use case');
    }
  };

  const handleDeleteUseCase = async (id: number) => {
    if (!confirm('Are you sure you want to delete this use case?')) return;
    try {
      await useCasesApi.delete(id);
      alert('Use case deleted successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error deleting use case:', error);
      alert('Failed to delete use case');
    }
  };

  const handleAddUpdate = async () => {
    if (!selectedAccountUid) return;
    try {
      await updatesApi.create({ ...newUpdate, account_uid: selectedAccountUid } as Update);
      setNewUpdate({});
      alert('Update added successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error adding update:', error);
      alert('Failed to add update');
    }
  };

  const handleUpdateUpdate = async () => {
    if (!editingUpdate || !editingUpdate.id) return;
    try {
      await updatesApi.update(editingUpdate.id, editingUpdate);
      setEditingUpdate(null);
      alert('Update updated successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error updating update:', error);
      alert('Failed to update update');
    }
  };

  const handleDeleteUpdate = async (id: number) => {
    if (!confirm('Are you sure you want to delete this update?')) return;
    try {
      await updatesApi.delete(id);
      alert('Update deleted successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error deleting update:', error);
      alert('Failed to delete update');
    }
  };

  const handleAddPlatform = async () => {
    if (!selectedAccountUid) return;
    try {
      await platformsApi.create({ ...newPlatform, account_uid: selectedAccountUid } as Platform);
      setNewPlatform({});
      alert('Platform added successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error adding platform:', error);
      alert('Failed to add platform');
    }
  };

  const handleUpdatePlatform = async () => {
    if (!editingPlatform || !editingPlatform.id) return;
    try {
      await platformsApi.update(editingPlatform.id, editingPlatform);
      setEditingPlatform(null);
      alert('Platform updated successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error updating platform:', error);
      alert('Failed to update platform');
    }
  };

  const handleDeletePlatform = async (id: number) => {
    if (!confirm('Are you sure you want to delete this platform?')) return;
    try {
      await platformsApi.delete(id);
      alert('Platform deleted successfully');
      loadAccountData();
    } catch (error) {
      console.error('Error deleting platform:', error);
      alert('Failed to delete platform');
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
          <CardTitle>Platforms</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {platforms.length > 0 && (
            <div className="space-y-2 mb-4">
              <h3 className="font-semibold">Existing Platforms</h3>
              {platforms.map((platform) => (
                <div key={platform.id} className="border rounded-md p-3">
                  {editingPlatform?.id === platform.id ? (
                    <div className="space-y-3">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Platform Name</label>
                          <select
                            className="w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                            value={editingPlatform!.platform_name || ''}
                            onChange={(e) => editingPlatform && setEditingPlatform({ ...editingPlatform, platform_name: e.target.value })}
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
                            value={editingPlatform!.onboarding_status || ''}
                            onChange={(e) => editingPlatform && setEditingPlatform({ ...editingPlatform, onboarding_status: e.target.value })}
                          >
                            <option value="">Select Status</option>
                            <option value="Not Started">Not Started</option>
                            <option value="Planning">Planning</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button onClick={handleUpdatePlatform}>Save</Button>
                        <Button variant="outline" onClick={() => setEditingPlatform(null)}>Cancel</Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{platform.platform_name}</p>
                        <p className="text-sm text-muted-foreground">Status: {platform.onboarding_status}</p>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => setEditingPlatform(platform)}>Edit</Button>
                        <Button variant="outline" onClick={() => handleDeletePlatform(platform.id!)}>Delete</Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          <h3 className="font-semibold">Add New Platform</h3>
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

      <Card>
        <CardHeader>
          <CardTitle>Updates</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {updates.length > 0 && (
            <div className="space-y-2 mb-4">
              <h3 className="font-semibold">Existing Updates</h3>
              {updates.map((update) => (
                <div key={update.id} className="border rounded-md p-3">
                  {editingUpdate?.id === update.id ? (
                    <div className="space-y-3">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Description</label>
                          <Input
                            value={editingUpdate!.description || ''}
                            onChange={(e) => editingUpdate && setEditingUpdate({ ...editingUpdate, description: e.target.value })}
                            placeholder="Enter update description"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Author</label>
                          <Input
                            value={editingUpdate!.author || ''}
                            onChange={(e) => editingUpdate && setEditingUpdate({ ...editingUpdate, author: e.target.value })}
                            placeholder="Enter author name"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Platform</label>
                          <Input
                            value={editingUpdate!.platform || ''}
                            onChange={(e) => editingUpdate && setEditingUpdate({ ...editingUpdate, platform: e.target.value })}
                            placeholder="Enter platform"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Date</label>
                          <Input
                            type="date"
                            value={editingUpdate!.date || ''}
                            onChange={(e) => editingUpdate && setEditingUpdate({ ...editingUpdate, date: e.target.value })}
                          />
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button onClick={handleUpdateUpdate}>Save</Button>
                        <Button variant="outline" onClick={() => setEditingUpdate(null)}>Cancel</Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{update.description}</p>
                        <p className="text-sm text-muted-foreground">
                          By {update.author} on {update.date} ({update.platform})
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => setEditingUpdate(update)}>Edit</Button>
                        <Button variant="outline" onClick={() => handleDeleteUpdate(update.id!)}>Delete</Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          <h3 className="font-semibold">Add New Update</h3>
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
          <CardTitle>Use Cases</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {useCases.length > 0 && (
            <div className="space-y-2 mb-4">
              <h3 className="font-semibold">Existing Use Cases</h3>
              {useCases.map((useCase) => (
                <div key={useCase.id} className="border rounded-md p-3">
                  {editingUseCase?.id === useCase.id ? (
                    <div className="space-y-3">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Problem</label>
                          <Input
                            value={editingUseCase!.problem || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, problem: e.target.value })}
                            placeholder="Enter problem statement"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Solution</label>
                          <Input
                            value={editingUseCase!.solution || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, solution: e.target.value })}
                            placeholder="Enter solution"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Value</label>
                          <Input
                            value={editingUseCase!.value || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, value: e.target.value })}
                            placeholder="Enter value proposition"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Leader</label>
                          <Input
                            value={editingUseCase!.leader || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, leader: e.target.value })}
                            placeholder="Enter leader name"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Status</label>
                          <Input
                            value={editingUseCase!.status || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, status: e.target.value })}
                            placeholder="Enter status"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Platform</label>
                          <Input
                            value={editingUseCase!.platform || ''}
                            onChange={(e) => editingUseCase && setEditingUseCase({ ...editingUseCase, platform: e.target.value })}
                            placeholder="Enter platform"
                          />
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button onClick={handleUpdateUseCase}>Save</Button>
                        <Button variant="outline" onClick={() => setEditingUseCase(null)}>Cancel</Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{useCase.problem}</p>
                        <p className="text-sm text-muted-foreground">
                          Solution: {useCase.solution} | Leader: {useCase.leader} | Status: {useCase.status}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => setEditingUseCase(useCase)}>Edit</Button>
                        <Button variant="outline" onClick={() => handleDeleteUseCase(useCase.id!)}>Delete</Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          <h3 className="font-semibold">Add New Use Case</h3>
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
    </div>
  );
}
