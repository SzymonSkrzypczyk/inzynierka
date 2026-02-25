import Link from 'next/link';
import { useRouter } from 'next/router';
import { cn } from '@/lib/utils';
import {
    Activity,
    Magnet,
    Zap,
    Sun,
    BarChart3,
    Home
} from 'lucide-react';

const navItems = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Geomagnetism', href: '/geomagnetism', icon: Activity },
    { name: 'Magnetic Field', href: '/magnetic-field', icon: Magnet },
    { name: 'Protons', href: '/protons', icon: Zap },
    { name: 'X-Ray', href: '/x-ray', icon: Sun },
    { name: 'Solar Regions', href: '/solar-regions', icon: BarChart3 },
];

export function Sidebar() {
    const router = useRouter();

    return (
        <div className="flex bg-slate-100 dark:bg-slate-900 h-screen w-64 flex-col border-r">
            <div className="flex h-16 items-center px-6 border-b">
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    Space Weather
                </h1>
            </div>
            <nav className="flex-1 space-y-1 p-4 overflow-y-auto">
                {navItems.map((item) => {
                    const isActive = router.pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center space-x-3 px-3 py-2 rounded-md transition-colors",
                                isActive
                                    ? "bg-slate-200 dark:bg-slate-800 text-blue-600 dark:text-blue-400 font-medium"
                                    : "text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800"
                            )}
                        >
                            <item.icon className="h-5 w-5" />
                            <span>{item.name}</span>
                        </Link>
                    );
                })}
            </nav>
            <div className="p-4 border-t text-xs text-slate-500 text-center">
                © 2026 Space Weather Dashboard
            </div>
        </div>
    );
}
