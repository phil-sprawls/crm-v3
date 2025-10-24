import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import { Button } from '../components/Button';
import axios from 'axios';
import { formatDistanceToNow } from 'date-fns';
import { Eye, Tag, X, Search } from 'lucide-react';

const API_BASE_URL = (() => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  if (hostname.includes('replit.dev')) {
    return `${protocol}//${hostname}:8000`;
  }
  
  if (hostname.includes('azurewebsites.net')) {
    return 'https://crm-backend-dev.azurewebsites.net';
  }
  
  return 'http://localhost:7006';
})();

interface IntakeRequest {
  id: number;
  title: string;
  description: string;
  has_it_partner: boolean;
  dri_contact: string;
  submitted_for: string;
  functional_area: string;
  help_types: string;
  platform: string;
  created_at: string;
  updated_at: string;
}

interface RequestState {
  id: number;
  name: string;
  color: string;
  description: string;
}

export function IntakeTriage() {
  const navigate = useNavigate();
  const [requests, setRequests] = useState<IntakeRequest[]>([]);
  const [allStates, setAllStates] = useState<RequestState[]>([]);
  const [requestStates, setRequestStates] = useState<Record<number, RequestState[]>>({});
  const [loading, setLoading] = useState(true);
  const [selectedRequest, setSelectedRequest] = useState<IntakeRequest | null>(null);
  const [showStateSelector, setShowStateSelector] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const loadRequests = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/intake-requests`);
      setRequests(response.data);
      
      for (const request of response.data) {
        loadRequestStates(request.id);
      }
    } catch (error) {
      console.error('Error loading requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/request-states`);
      setAllStates(response.data);
    } catch (error) {
      console.error('Error loading states:', error);
    }
  };

  const loadRequestStates = async (requestId: number) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/intake-requests/${requestId}/states`);
      setRequestStates(prev => ({
        ...prev,
        [requestId]: response.data
      }));
    } catch (error) {
      console.error('Error loading request states:', error);
    }
  };

  useEffect(() => {
    loadRequests();
    loadStates();
  }, []);

  const parseHelpTypes = (helpTypesJson: string): string[] => {
    try {
      return JSON.parse(helpTypesJson || '[]');
    } catch {
      return [];
    }
  };

  const formatHelpTypes = (helpTypes: string[]): string => {
    const labels: Record<string, string> = {
      consultation: 'Consultation/Questions',
      build: 'Build Something',
      new_environment: 'New Environment',
      enhancement: 'Environment Enhancement',
      cloud_storage: 'Cloud Storage'
    };
    
    return helpTypes.map(ht => labels[ht] || ht).join(', ');
  };

  const assignState = async (stateId: number) => {
    if (!selectedRequest) return;
    
    try {
      await axios.post(`${API_BASE_URL}/api/intake-requests/${selectedRequest.id}/states/${stateId}`);
      await loadRequestStates(selectedRequest.id);
      setShowStateSelector(false);
      setSelectedRequest(null);
    } catch (error) {
      console.error('Error assigning state:', error);
    }
  };

  const removeState = async (requestId: number, stateId: number) => {
    try {
      await axios.delete(`${API_BASE_URL}/api/intake-requests/${requestId}/states/${stateId}`);
      await loadRequestStates(requestId);
    } catch (error) {
      console.error('Error removing state:', error);
    }
  };

  const filteredRequests = requests.filter(request => {
    if (!searchTerm) return true;
    
    const searchLower = searchTerm.toLowerCase();
    const helpTypes = parseHelpTypes(request.help_types);
    const formattedHelpTypes = formatHelpTypes(helpTypes).toLowerCase();
    
    return (
      request.title.toLowerCase().includes(searchLower) ||
      (request.description || '').toLowerCase().includes(searchLower) ||
      (request.functional_area || '').toLowerCase().includes(searchLower) ||
      (request.platform || '').toLowerCase().includes(searchLower) ||
      (request.submitted_for || '').toLowerCase().includes(searchLower) ||
      (request.dri_contact || '').toLowerCase().includes(searchLower) ||
      formattedHelpTypes.includes(searchLower)
    );
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Intake Triage</h1>
        <Button onClick={() => navigate('/admin/states')}>
          Manage States
        </Button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search requests by title, area, platform, help type..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      {filteredRequests.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            {searchTerm ? 'No requests match your search.' : 'No requests submitted yet.'}
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredRequests.map(request => {
            const states = requestStates[request.id] || [];
            const helpTypes = parseHelpTypes(request.help_types);
            
            return (
              <Card key={request.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 space-y-3">
                      <div>
                        <h3 className="text-xl font-semibold">{request.title}</h3>
                        <p className="text-sm text-muted-foreground mt-1">
                          Submitted {formatDistanceToNow(new Date(request.created_at), { addSuffix: true })}
                        </p>
                      </div>

                      {request.description && (
                        <p className="text-muted-foreground line-clamp-2">{request.description}</p>
                      )}

                      <div className="flex flex-wrap gap-4 text-sm">
                        {request.functional_area && (
                          <div>
                            <span className="font-medium">Area:</span> {request.functional_area}
                          </div>
                        )}
                        {request.platform && (
                          <div>
                            <span className="font-medium">Platform:</span> {request.platform}
                          </div>
                        )}
                        {request.submitted_for && (
                          <div>
                            <span className="font-medium">For:</span> {request.submitted_for}
                          </div>
                        )}
                        {request.dri_contact && (
                          <div>
                            <span className="font-medium">DRI:</span> {request.dri_contact}
                          </div>
                        )}
                      </div>

                      {helpTypes.length > 0 && (
                        <div className="text-sm">
                          <span className="font-medium">Help Needed:</span> {formatHelpTypes(helpTypes)}
                        </div>
                      )}

                      <div className="flex flex-wrap gap-2 mt-3">
                        {states.map(state => (
                          <div
                            key={state.id}
                            className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium"
                            style={{ 
                              backgroundColor: `${state.color}20`,
                              color: state.color,
                              border: `1px solid ${state.color}40`
                            }}
                          >
                            {state.name}
                            <button
                              onClick={() => removeState(request.id, state.id)}
                              className="ml-1 hover:opacity-70"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          </div>
                        ))}
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            setSelectedRequest(request);
                            setShowStateSelector(true);
                          }}
                        >
                          <Tag className="h-4 w-4 mr-1" />
                          Add State
                        </Button>
                      </div>
                    </div>

                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setSelectedRequest(request)}
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      View Details
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {selectedRequest && !showStateSelector && (
        <div 
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" 
          onClick={() => setSelectedRequest(null)}
          style={{ overflow: 'hidden', overscrollBehavior: 'contain' }}
        >
          <div 
            className="max-w-2xl w-full max-h-[80vh] flex flex-col bg-card rounded-lg border shadow-sm" 
            onClick={e => e.stopPropagation()}
          >
            <div className="flex-shrink-0 border-b p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold leading-none tracking-tight">{selectedRequest.title}</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    Submitted {formatDistanceToNow(new Date(selectedRequest.created_at), { addSuffix: true })}
                  </p>
                </div>
                <Button size="sm" variant="outline" onClick={() => setSelectedRequest(null)}>
                  Close
                </Button>
              </div>
            </div>
            <div 
              className="flex-1 overflow-y-scroll p-6 space-y-4 min-h-0" 
              style={{ 
                maxHeight: 'calc(80vh - 100px)',
                WebkitOverflowScrolling: 'touch',
                overscrollBehavior: 'contain'
              }}
            >
              {selectedRequest.description && (
                <div>
                  <h4 className="font-medium mb-1">Description</h4>
                  <p className="text-muted-foreground">{selectedRequest.description}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Functional Area</h4>
                  <p className="text-muted-foreground">{selectedRequest.functional_area || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Platform</h4>
                  <p className="text-muted-foreground">{selectedRequest.platform || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Submitted For</h4>
                  <p className="text-muted-foreground">{selectedRequest.submitted_for || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">DRI Contact</h4>
                  <p className="text-muted-foreground">{selectedRequest.dri_contact || 'N/A'}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Has IT Partner</h4>
                  <p className="text-muted-foreground">{selectedRequest.has_it_partner ? 'Yes' : 'No'}</p>
                </div>
              </div>

              <div>
                <h4 className="font-medium mb-2">Help Needed</h4>
                <p className="text-muted-foreground">{formatHelpTypes(parseHelpTypes(selectedRequest.help_types))}</p>
              </div>

              {selectedRequest.additional_details && (() => {
                try {
                  const details = JSON.parse(selectedRequest.additional_details);
                  const entries = Object.entries(details);
                  if (entries.length > 0) {
                    return (
                      <div>
                        <h4 className="font-medium mb-2">Additional Details</h4>
                        <div className="space-y-2 bg-muted/30 p-4 rounded-lg">
                          {entries.map(([key, value]) => (
                            <div key={key}>
                              <p className="text-sm font-medium capitalize">{key.replace(/_/g, ' ')}</p>
                              <p className="text-sm text-muted-foreground mt-0.5">
                                {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value)}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  }
                } catch (e) {
                  return null;
                }
                return null;
              })()}

              <div>
                <h4 className="font-medium mb-2">Current States</h4>
                <div className="flex flex-wrap gap-2">
                  {(requestStates[selectedRequest.id] || []).map(state => (
                    <div
                      key={state.id}
                      className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium"
                      style={{ 
                        backgroundColor: `${state.color}20`,
                        color: state.color,
                        border: `1px solid ${state.color}40`
                      }}
                    >
                      {state.name}
                    </div>
                  ))}
                  {(requestStates[selectedRequest.id] || []).length === 0 && (
                    <p className="text-sm text-muted-foreground">No states assigned yet</p>
                  )}
                </div>
              </div>

              <div className="pt-2 border-t">
                <p className="text-xs text-muted-foreground">
                  Last updated: {formatDistanceToNow(new Date(selectedRequest.updated_at), { addSuffix: true })}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {showStateSelector && selectedRequest && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" onClick={() => setShowStateSelector(false)}>
          <Card className="max-w-md w-full" onClick={e => e.stopPropagation()}>
            <CardHeader>
              <CardTitle>Add State</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {allStates.map(state => {
                  const isAssigned = (requestStates[selectedRequest.id] || []).some(s => s.id === state.id);
                  
                  return (
                    <button
                      key={state.id}
                      onClick={() => assignState(state.id)}
                      disabled={isAssigned}
                      className="w-full p-3 text-left rounded-lg border-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:bg-muted/50"
                      style={{ borderColor: state.color }}
                    >
                      <div className="flex items-center gap-2">
                        <div 
                          className="h-4 w-4 rounded-full" 
                          style={{ backgroundColor: state.color }}
                        />
                        <div>
                          <div className="font-medium">{state.name}</div>
                          {state.description && (
                            <div className="text-sm text-muted-foreground">{state.description}</div>
                          )}
                        </div>
                        {isAssigned && (
                          <div className="ml-auto text-sm text-muted-foreground">Already assigned</div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
              <div className="mt-4">
                <Button variant="outline" onClick={() => setShowStateSelector(false)} className="w-full">
                  Cancel
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
