import { Sidebar } from './Sidebar';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className={`flex min-h-screen ${inter.className}`}>
            <Sidebar />
            <main className="flex-1 overflow-auto bg-slate-50 dark:bg-slate-950 p-6 md:p-10">
                <div className="max-w-7xl mx-auto space-y-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
