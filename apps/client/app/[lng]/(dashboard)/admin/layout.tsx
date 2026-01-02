import { ReactNode } from "react";
import Link from "next/link";
import {
    LayoutDashboard,
    BarChart3,
    Settings,
    Users,
    FileText,
    Eye,
} from "lucide-react";
import { Separator, Button } from "@saas/ui";

interface AdminLayoutProps {
    children: ReactNode;
    params: Promise<{ lng: string }>;
}

const sidebarItems = [
    { icon: LayoutDashboard, label: "Dashboard", href: "/admin" },
    { icon: Eye, label: "Analyze", href: "/analyze" },
    { icon: BarChart3, label: "Reports", href: "/admin/reports" },
    { icon: Users, label: "Users", href: "/admin/users" },
    { icon: FileText, label: "Documentation", href: "/admin/docs" },
    { icon: Settings, label: "Settings", href: "/admin/settings" },
];

export default async function AdminLayout({
    children,
    params,
}: AdminLayoutProps) {
    const { lng } = await params;

    return (
        <div className="flex min-h-screen bg-background">
            {/* Sidebar */}
            <aside className="hidden md:flex w-64 flex-col border-r bg-card">
                <div className="p-6">
                    <h1 className="text-xl font-bold text-foreground">
                        Uvolution<span className="text-primary">AI</span>
                    </h1>
                    <p className="text-sm text-muted-foreground">Admin Dashboard</p>
                </div>
                <Separator />
                <nav className="flex-1 p-4 space-y-1">
                    {sidebarItems.map((item) => (
                        <Link
                            key={item.href}
                            href={`/${lng}${item.href}`}
                            className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                        >
                            <item.icon className="h-4 w-4" />
                            {item.label}
                        </Link>
                    ))}
                </nav>
                <Separator />
                <div className="p-4">
                    <Button variant="outline" className="w-full" asChild>
                        <Link href={`/${lng}`}>← Back to Home</Link>
                    </Button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <div className="p-6 md:p-8">{children}</div>
            </main>
        </div>
    );
}
