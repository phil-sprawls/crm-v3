import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import { MessageCircle, Hammer, PlusCircle, Settings, Cloud, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

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

const HELP_OPTIONS = [
  {
    id: 'consultation',
    label: 'Consultation/Questions',
    description: 'Get expert advice and answers to your questions',
    icon: MessageCircle,
    color: 'blue'
  },
  {
    id: 'build',
    label: 'Build Something',
    description: 'Create a new solution or application',
    icon: Hammer,
    color: 'orange'
  },
  {
    id: 'new_environment',
    label: 'New Environment',
    description: 'Set up a new development or production environment',
    icon: PlusCircle,
    color: 'green'
  },
  {
    id: 'enhancement',
    label: 'Environment Enhancement',
    description: 'Improve or modify existing environments',
    icon: Settings,
    color: 'purple'
  },
  {
    id: 'cloud_storage',
    label: 'Cloud Storage for Downstream Consumers',
    description: 'Set up data storage for downstream applications',
    icon: Cloud,
    color: 'cyan'
  }
];

export function IntakeForm() {
  const navigate = useNavigate();
  const [functionalAreas, setFunctionalAreas] = useState<string[]>([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    has_it_partner: false,
    dri_contact: '',
    submitted_for: '',
    functional_area: '',
    platform: '',
  });
  const [selectedHelpTypes, setSelectedHelpTypes] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    axios.get(`${API_BASE_URL}/api/functional-areas`)
      .then(response => setFunctionalAreas(response.data))
      .catch(error => console.error('Error loading functional areas:', error));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'radio') {
      setFormData({
        ...formData,
        [name]: value === 'true',
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const toggleHelpType = (id: string) => {
    setSelectedHelpTypes(prev => 
      prev.includes(id) 
        ? prev.filter(t => t !== id)
        : [...prev, id]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selectedHelpTypes.length === 0) {
      setErrorMessage('Please select at least one option for "What Can We Help You With"');
      setShowErrorModal(true);
      return;
    }
    
    setSubmitting(true);
    try {
      await axios.post(`${API_BASE_URL}/api/intake-requests`, {
        ...formData,
        help_types: JSON.stringify(selectedHelpTypes),
      });
      
      setShowSuccessModal(true);
    } catch (error) {
      console.error('Error submitting request:', error);
      setErrorMessage('Failed to submit request. Please try again.');
      setShowErrorModal(true);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-8">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold">Submit a Request</h1>
        <p className="text-muted-foreground text-lg">
          Tell us how we can help you with your platform needs
        </p>
      </div>

      <Card className="border-2">
        <CardHeader className="bg-muted/50">
          <CardTitle className="text-xl">How to Submit a Request</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <ol className="list-decimal list-inside space-y-2 text-muted-foreground">
            <li>Fill out all required fields marked with an asterisk (*)</li>
            <li>Select one or more options for what type of help you need</li>
            <li>Provide as much detail as possible in the description</li>
            <li>Submit the form and our team will review your request</li>
            <li>You'll receive an email confirmation once your request is reviewed</li>
          </ol>
        </CardContent>
      </Card>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Request Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium mb-1">
                  Request Title <span className="text-red-500">*</span>
                </label>
                <Input
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  placeholder="Brief summary of your request"
                />
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
                  rows={4}
                  className="w-full px-3 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
                  placeholder="Provide detailed information about your request"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="dri_contact" className="block text-sm font-medium mb-1">
                    DRI Contact
                  </label>
                  <Input
                    id="dri_contact"
                    name="dri_contact"
                    value={formData.dri_contact}
                    onChange={handleChange}
                    placeholder="Name (email@company.com)"
                  />
                </div>

                <div>
                  <label htmlFor="submitted_for" className="block text-sm font-medium mb-1">
                    Submitted For
                  </label>
                  <Input
                    id="submitted_for"
                    name="submitted_for"
                    value={formData.submitted_for}
                    onChange={handleChange}
                    placeholder="Team or person name"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="functional_area" className="block text-sm font-medium mb-1">
                    Functional Area <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="functional_area"
                    name="functional_area"
                    value={formData.functional_area}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    <option value="">Select an area...</option>
                    {functionalAreas.map(area => (
                      <option key={area} value={area}>{area}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="platform" className="block text-sm font-medium mb-1">
                    Platform
                  </label>
                  <select
                    id="platform"
                    name="platform"
                    value={formData.platform}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    <option value="">Select a platform...</option>
                    <option value="Databricks">Databricks</option>
                    <option value="Snowflake">Snowflake</option>
                    <option value="Power Platform">Power Platform</option>
                    <option value="Fabric">Fabric</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Do you have an IT Partner? <span className="text-red-500">*</span>
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="has_it_partner"
                      value="true"
                      checked={formData.has_it_partner === true}
                      onChange={handleChange}
                      required
                      className="mr-2"
                    />
                    Yes
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="has_it_partner"
                      value="false"
                      checked={formData.has_it_partner === false}
                      onChange={handleChange}
                      className="mr-2"
                    />
                    No
                  </label>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>What Can We Help You With? <span className="text-red-500">*</span></CardTitle>
            <p className="text-sm text-muted-foreground">Select all that apply</p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {HELP_OPTIONS.map(option => {
                const Icon = option.icon;
                const isSelected = selectedHelpTypes.includes(option.id);
                
                return (
                  <div
                    key={option.id}
                    onClick={() => toggleHelpType(option.id)}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      isSelected
                        ? 'border-primary bg-primary/5 shadow-md'
                        : 'border-border hover:border-primary/50 hover:bg-muted/50'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg bg-${option.color}-100 dark:bg-${option.color}-900/20`}>
                        <Icon className={`h-6 w-6 text-${option.color}-600 dark:text-${option.color}-400`} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold">{option.label}</h3>
                          {isSelected && (
                            <div className="h-5 w-5 bg-primary rounded-full flex items-center justify-center">
                              <svg className="h-3 w-3 text-primary-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                              </svg>
                            </div>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground mt-1">{option.description}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        <div className="flex gap-4 justify-end">
          <Button type="button" variant="outline" onClick={() => navigate('/')}>
            Cancel
          </Button>
          <Button type="submit" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Request'}
          </Button>
        </div>
      </form>

      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="max-w-md w-full">
            <CardContent className="pt-6 pb-6 text-center space-y-4">
              <div className="flex justify-center">
                <div className="h-16 w-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                  <CheckCircle className="h-10 w-10 text-green-600 dark:text-green-400" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-semibold">Request Submitted Successfully!</h3>
                <p className="text-muted-foreground">
                  Our team will review your request soon. You'll receive an email confirmation once it has been reviewed.
                </p>
              </div>
              <Button onClick={() => navigate('/')} className="w-full">
                Return to Home
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {showErrorModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="max-w-md w-full">
            <CardContent className="pt-6 pb-6 text-center space-y-4">
              <div className="flex justify-center">
                <div className="h-16 w-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
                  <AlertCircle className="h-10 w-10 text-red-600 dark:text-red-400" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-semibold">Unable to Submit Request</h3>
                <p className="text-muted-foreground">{errorMessage}</p>
              </div>
              <Button onClick={() => setShowErrorModal(false)} className="w-full">
                OK
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
