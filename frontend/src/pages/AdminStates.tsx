import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import axios from 'axios';
import { ArrowLeft, Edit, Trash2, Plus } from 'lucide-react';

const API_BASE_URL = (() => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  if (hostname.includes('azurewebsites.net')) {
    return 'https://crm-backend-dev.azurewebsites.net';
  }
  
  return 'http://localhost:8000';
})();

interface RequestState {
  id?: number;
  name: string;
  color: string;
  description: string;
}

export function AdminStates() {
  const navigate = useNavigate();
  const [states, setStates] = useState<RequestState[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingState, setEditingState] = useState<RequestState | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    color: '#3b82f6',
    description: ''
  });

  const loadStates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/request-states`);
      setStates(response.data);
    } catch (error) {
      console.error('Error loading states:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStates();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingState?.id) {
        await axios.put(`${API_BASE_URL}/api/request-states/${editingState.id}`, formData);
      } else {
        await axios.post(`${API_BASE_URL}/api/request-states`, formData);
      }
      
      setFormData({ name: '', color: '#3b82f6', description: '' });
      setEditingState(null);
      setShowForm(false);
      await loadStates();
    } catch (error) {
      console.error('Error saving state:', error);
      alert('Failed to save state. Please try again.');
    }
  };

  const handleEdit = (state: RequestState) => {
    setFormData({
      name: state.name,
      color: state.color,
      description: state.description
    });
    setEditingState(state);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this state? This will remove it from all requests.')) {
      return;
    }
    
    try {
      await axios.delete(`${API_BASE_URL}/api/request-states/${id}`);
      await loadStates();
    } catch (error) {
      console.error('Error deleting state:', error);
      alert('Failed to delete state. Please try again.');
    }
  };

  const handleCancel = () => {
    setFormData({ name: '', color: '#3b82f6', description: '' });
    setEditingState(null);
    setShowForm(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate('/admin/intake-triage')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold">Manage Request States</h1>
      </div>

      <div className="flex justify-end">
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          Add New State
        </Button>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>{editingState ? 'Edit State' : 'Create New State'}</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium mb-1">
                  State Name <span className="text-red-500">*</span>
                </label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  placeholder="e.g., Pending Approval"
                />
              </div>

              <div>
                <label htmlFor="color" className="block text-sm font-medium mb-1">
                  Color <span className="text-red-500">*</span>
                </label>
                <div className="flex gap-2 items-center">
                  <input
                    type="color"
                    id="color"
                    name="color"
                    value={formData.color}
                    onChange={handleChange}
                    className="h-10 w-20 rounded border border-input cursor-pointer"
                  />
                  <Input
                    value={formData.color}
                    onChange={handleChange}
                    name="color"
                    placeholder="#3b82f6"
                    pattern="^#[0-9A-Fa-f]{6}$"
                    className="flex-1"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={2}
                  className="w-full px-3 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
                  placeholder="Brief description of this state"
                />
              </div>

              <div className="flex gap-2 justify-end">
                <Button type="button" variant="outline" onClick={handleCancel}>
                  Cancel
                </Button>
                <Button type="submit">
                  {editingState ? 'Update State' : 'Create State'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Existing States</CardTitle>
        </CardHeader>
        <CardContent>
          {states.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">No states created yet.</p>
          ) : (
            <div className="space-y-2">
              {states.map(state => (
                <div
                  key={state.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
                >
                  <div className="flex items-center gap-3">
                    <div 
                      className="h-8 w-8 rounded-full flex-shrink-0" 
                      style={{ backgroundColor: state.color }}
                    />
                    <div>
                      <div className="font-medium">{state.name}</div>
                      {state.description && (
                        <div className="text-sm text-muted-foreground">{state.description}</div>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(state)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => state.id && handleDelete(state.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
