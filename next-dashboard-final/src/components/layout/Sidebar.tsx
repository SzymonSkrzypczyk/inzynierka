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

import { ModeToggle } from '@/components/mode-toggle';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

export function Sidebar() {
    const router = useRouter();
    const currentLimit = router.query.limit || "500";

    const handleLimitChange = (value: string) => {
        router.push({
            pathname: router.pathname,
            query: { ...router.query, limit: value },
        });
    };

    return (
        <div className="flex bg-slate-100 dark:bg-slate-900 h-screen w-64 flex-col border-r">
            <div className="flex h-16 items-center justify-between px-6 border-b">
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    Space Weather
                </h1>
                <ModeToggle />
            </div>
            <nav className="flex-1 space-y-1 p-4 overflow-y-auto">
                {navItems.map((item) => {
                    const isActive = router.pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={{
                                pathname: item.href,
                                query: router.query.limit ? { limit: router.query.limit } : {}
                            }}
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
            <div className="p-4 border-t space-y-4">
                <div className="space-y-2">
                    <label className="text-[10px] uppercase font-bold text-slate-500 px-1">Data Limit</label>
                    <Select value={String(currentLimit)} onValueChange={handleLimitChange}>
                        <SelectTrigger className="h-8 text-xs">
                            <SelectValue placeholder="Select limit" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="100">100 points</SelectItem>
                            <SelectItem value="500">500 points</SelectItem>
                            <SelectItem value="1000">1000 points</SelectItem>
                            <SelectItem value="2000">2000 points</SelectItem>
                            <SelectItem value="5000">5000 points</SelectItem>
                            <SelectItem value="10000">10000 points</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                {Number(currentLimit) >= 5000 && (
                    <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded p-2 text-[10px] text-orange-600 dark:text-orange-400">
                        <strong>Performance Note:</strong> Displaying large datasets may slow down chart interactions. Use the range selector to zoom.
                    </div>
                )}
                <div className="text-[10px] text-slate-500 text-center">
                    © 2026 Space Weather Dashboard
                </div>
            </div>
        </div>
    );
}
