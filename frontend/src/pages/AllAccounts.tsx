import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Account } from '../types';
import { accountsApi } from '../lib/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Search } from 'lucide-react';

export function AllAccounts() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [filteredAccounts, setFilteredAccounts] = useState<Account[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (searchTerm === '') {
      setFilteredAccounts(accounts);
    } else {
      const filtered = accounts.filter(
        (account) =>
          account.team?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          account.business_it_area?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          account.vp?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          account.team_admin?.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredAccounts(filtered);
    }
  }, [searchTerm, accounts]);

  const loadAccounts = async () => {
    try {
      const response = await accountsApi.getAll();
      const data = Array.isArray(response.data) ? response.data : [];
      setAccounts(data);
      setFilteredAccounts(data);
    } catch (error) {
      console.error('Error loading accounts:', error);
      setAccounts([]);
      setFilteredAccounts([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading accounts...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">All Accounts</h1>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Search accounts by team, area, VP, or admin..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-muted">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium">Team</th>
              <th className="px-4 py-3 text-left text-sm font-medium">Business/IT Area</th>
              <th className="px-4 py-3 text-left text-sm font-medium">VP</th>
              <th className="px-4 py-3 text-left text-sm font-medium">Admin</th>
              <th className="px-4 py-3 text-left text-sm font-medium">Primary IT Partner</th>
              <th className="px-4 py-3 text-left text-sm font-medium">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {Array.isArray(filteredAccounts) && filteredAccounts.map((account) => (
              <tr key={account.uid} className="hover:bg-muted/50">
                <td className="px-4 py-3 text-sm">{account.team || '-'}</td>
                <td className="px-4 py-3 text-sm">{account.business_it_area || '-'}</td>
                <td className="px-4 py-3 text-sm">{account.vp || '-'}</td>
                <td className="px-4 py-3 text-sm">{account.team_admin || '-'}</td>
                <td className="px-4 py-3 text-sm">-</td>
                <td className="px-4 py-3 text-sm">
                  <Button size="sm" onClick={() => navigate(`/accounts/${account.uid}`)}>
                    View
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredAccounts.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">No accounts found</div>
        )}
      </div>
    </div>
  );
}
