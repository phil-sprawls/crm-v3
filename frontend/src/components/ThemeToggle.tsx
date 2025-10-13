import { Settings, Sun, Moon, Monitor } from 'lucide-react';
import { useEffect, useState, useRef } from 'react';
import { Button } from './Button';

type Theme = 'light' | 'dark' | 'system';

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>('system');
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme);
    const defaultTheme = savedTheme || 'system';
    setTheme(defaultTheme);
    applyTheme(defaultTheme);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const applyTheme = (newTheme: Theme) => {
    if (newTheme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.classList.toggle('dark', systemTheme === 'dark');
    } else {
      document.documentElement.classList.toggle('dark', newTheme === 'dark');
    }
  };

  const changeTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
    setIsOpen(false);
  };

  useEffect(() => {
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => applyTheme('system');
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);

  return (
    <div className="relative" ref={dropdownRef}>
      <Button 
        variant="outline" 
        size="icon" 
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Settings"
      >
        <Settings className="h-5 w-5" />
      </Button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-background border border-border z-50">
          <div className="py-1">
            <div className="px-4 py-2 text-sm font-medium text-muted-foreground border-b">
              Theme
            </div>
            <button
              onClick={() => changeTheme('light')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-accent flex items-center gap-2 ${
                theme === 'light' ? 'bg-accent' : ''
              }`}
            >
              <Sun className="h-4 w-4" />
              <span>Light</span>
              {theme === 'light' && <span className="ml-auto text-xs">✓</span>}
            </button>
            <button
              onClick={() => changeTheme('dark')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-accent flex items-center gap-2 ${
                theme === 'dark' ? 'bg-accent' : ''
              }`}
            >
              <Moon className="h-4 w-4" />
              <span>Dark</span>
              {theme === 'dark' && <span className="ml-auto text-xs">✓</span>}
            </button>
            <button
              onClick={() => changeTheme('system')}
              className={`w-full text-left px-4 py-2 text-sm hover:bg-accent flex items-center gap-2 ${
                theme === 'system' ? 'bg-accent' : ''
              }`}
            >
              <Monitor className="h-4 w-4" />
              <span>System</span>
              {theme === 'system' && <span className="ml-auto text-xs">✓</span>}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
