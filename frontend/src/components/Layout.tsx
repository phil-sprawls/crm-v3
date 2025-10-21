import { Link, Outlet } from 'react-router-dom';
import { ThemeToggle } from './ThemeToggle';

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-xl font-bold">
              IT Platform CRM
            </Link>
            <div className="flex gap-4">
              <Link to="/" className="text-sm font-medium hover:underline">
                Accounts
              </Link>
              <Link to="/intake" className="text-sm font-medium hover:underline">
                Submit Request
              </Link>
              <Link to="/admin/intake-triage" className="text-sm font-medium hover:underline">
                Intake Triage
              </Link>
              <Link to="/admin" className="text-sm font-medium hover:underline">
                Admin
              </Link>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
