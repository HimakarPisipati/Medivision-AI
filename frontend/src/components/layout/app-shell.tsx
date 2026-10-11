import { useState, useEffect } from 'react';
import { Link, useRouterState } from '@tanstack/react-router';
import {
  Activity,
  LayoutDashboard,
  ScanLine,
  ChartNoAxesCombined,
  BookOpen,
  PanelLeftClose,
  PanelLeftOpen,
  ChevronRight,
  CircleHelp,
  Menu,
  Sun,
  Moon,
} from 'lucide-react';
import type { ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { BackendStatus } from '@/components/shared/common';

const navigation = [
  { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { to: '/analyze', label: 'Analyze X-Ray', icon: ScanLine },
  { to: '/model-insights', label: 'Model Insights', icon: ChartNoAxesCombined },
  { to: '/about', label: 'About the Project', icon: BookOpen },
] as const;

export function AppShell({ children }: { children: ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isDark, setIsDark] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false;
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') return true;
    if (saved === 'light') return false;
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  const pathname = useRouterState({ select: state => state.location.pathname });
  const title = navigation.find(item => item.to === pathname)?.label || 'Overview';

  return (
    <TooltipProvider delayDuration={150}>
      <div className="app-shell">
        {mobileOpen && (
          <div
            className="mobile-backdrop"
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
        )}
        <aside
          className={`sidebar ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`}
          aria-label="Main navigation"
        >
          <Link
            to="/dashboard"
            className="brand"
            aria-label="MediVision AI overview"
            onClick={() => setMobileOpen(false)}
          >
            <div className="brand-icon">
              <Activity size={24} />
            </div>
            {!collapsed && (
              <div className="brand-copy">
                <div className="brand-name">
                  MediVision <span>AI</span>
                </div>
                <div className="brand-subtitle">Intelligent Imaging. Explainable AI.</div>
              </div>
            )}
          </Link>

          {!collapsed && <div className="nav-section-label">Workspace</div>}
          <nav className={`side-nav ${collapsed ? 'mt-12' : ''}`}>
            {navigation.map(item => (
              <Tooltip key={item.to}>
                <TooltipTrigger asChild>
                  <Link
                    to={item.to}
                    onClick={() => setMobileOpen(false)}
                    aria-label={item.label}
                    className={`nav-item ${pathname === item.to ? 'active' : ''}`}
                    aria-current={pathname === item.to ? 'page' : undefined}
                  >
                    <item.icon size={18} />
                    {!collapsed && <span className="nav-copy">{item.label}</span>}
                  </Link>
                </TooltipTrigger>
                <TooltipContent side="right">{item.label}</TooltipContent>
              </Tooltip>
            ))}
          </nav>
        </aside>

        <div className={`main-shell ${collapsed ? 'collapsed' : ''}`}>
          <header className="topbar">
            <div className="breadcrumb">
              <Button
                variant="ghost"
                size="icon"
                title={collapsed ? 'Expand navigation' : 'Collapse navigation'}
                aria-label={collapsed ? 'Expand navigation' : 'Collapse navigation'}
                className="hidden sm:inline-flex"
                onClick={() => setCollapsed(!collapsed)}
              >
                {collapsed ? <PanelLeftOpen /> : <PanelLeftClose />}
              </Button>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Open navigation"
                className="mobile-only"
                onClick={() => {
                  setCollapsed(false);
                  setMobileOpen(!mobileOpen);
                }}
              >
                <Menu />
              </Button>
              <span className="root-crumb">Workspace</span>
              <ChevronRight size={12} className="root-crumb" />
              <strong>{title}</strong>
            </div>

            <div className="topbar-right">
              <BackendStatus />

              {/* Theme Toggle Button */}
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={toggleTheme}
                    aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
                    title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
                  >
                    {isDark ? <Sun size={17} className="text-ai" /> : <Moon size={17} />}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>{isDark ? 'Light mode' : 'Dark mode'}</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <Button asChild size="icon" variant="ghost" className="help-button">
                    <Link to="/about" aria-label="About MediVision AI">
                      <CircleHelp size={17} />
                    </Link>
                  </Button>
                </TooltipTrigger>
                <TooltipContent>About MediVision AI</TooltipContent>
              </Tooltip>
            </div>
          </header>

          <main className="workspace">{children}</main>
        </div>
      </div>
    </TooltipProvider>
  );
}
