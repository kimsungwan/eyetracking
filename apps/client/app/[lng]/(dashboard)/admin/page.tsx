import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    Badge,
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@saas/ui";
import { Eye, FileText, Users, TrendingUp } from "lucide-react";

export default async function AdminDashboardPage({
    params,
}: {
    params: Promise<{ lng: string }>;
}) {
    const { lng } = await params;

    // Mock data for dashboard
    const stats = [
        {
            title: "Total Analyses",
            value: "1,234",
            change: "+12%",
            icon: Eye,
            color: "text-blue-500",
        },
        {
            title: "Reports Generated",
            value: "856",
            change: "+8%",
            icon: FileText,
            color: "text-green-500",
        },
        {
            title: "Active Users",
            value: "342",
            change: "+23%",
            icon: Users,
            color: "text-purple-500",
        },
        {
            title: "Conversion Rate",
            value: "4.2%",
            change: "+2.1%",
            icon: TrendingUp,
            color: "text-orange-500",
        },
    ];

    const recentAnalyses = [
        {
            id: 1,
            filename: "homepage-redesign.png",
            date: "2026-01-02",
            status: "completed",
            score: 85,
        },
        {
            id: 2,
            filename: "landing-page-v2.jpg",
            date: "2026-01-02",
            status: "completed",
            score: 72,
        },
        {
            id: 3,
            filename: "checkout-flow.png",
            date: "2026-01-01",
            status: "processing",
            score: null,
        },
        {
            id: 4,
            filename: "mobile-app-screen.png",
            date: "2026-01-01",
            status: "completed",
            score: 91,
        },
        {
            id: 5,
            filename: "dashboard-ui.jpg",
            date: "2025-12-31",
            status: "completed",
            score: 68,
        },
    ];

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
                <p className="text-muted-foreground">
                    Welcome back! Here's an overview of your UX analysis activity.
                </p>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {stats.map((stat) => (
                    <Card key={stat.title}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                            <stat.icon className={`h-4 w-4 ${stat.color}`} />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stat.value}</div>
                            <p className="text-xs text-muted-foreground">
                                <span className="text-green-500">{stat.change}</span> from last
                                month
                            </p>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Tabs Section */}
            <Tabs defaultValue="recent" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="recent">Recent Analyses</TabsTrigger>
                    <TabsTrigger value="popular">Top Performing</TabsTrigger>
                    <TabsTrigger value="pending">Pending</TabsTrigger>
                </TabsList>

                <TabsContent value="recent">
                    <Card>
                        <CardHeader>
                            <CardTitle>Recent Analyses</CardTitle>
                            <CardDescription>
                                Your latest UX analysis submissions and their results.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Filename</TableHead>
                                        <TableHead>Date</TableHead>
                                        <TableHead>Status</TableHead>
                                        <TableHead className="text-right">Score</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {recentAnalyses.map((analysis) => (
                                        <TableRow key={analysis.id}>
                                            <TableCell className="font-medium">
                                                {analysis.filename}
                                            </TableCell>
                                            <TableCell>{analysis.date}</TableCell>
                                            <TableCell>
                                                <Badge
                                                    variant={
                                                        analysis.status === "completed"
                                                            ? "success"
                                                            : "warning"
                                                    }
                                                >
                                                    {analysis.status}
                                                </Badge>
                                            </TableCell>
                                            <TableCell className="text-right">
                                                {analysis.score !== null ? (
                                                    <span
                                                        className={
                                                            analysis.score >= 80
                                                                ? "text-green-500"
                                                                : analysis.score >= 60
                                                                    ? "text-yellow-500"
                                                                    : "text-red-500"
                                                        }
                                                    >
                                                        {analysis.score}
                                                    </span>
                                                ) : (
                                                    <span className="text-muted-foreground">—</span>
                                                )}
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="popular">
                    <Card>
                        <CardHeader>
                            <CardTitle>Top Performing</CardTitle>
                            <CardDescription>
                                Analyses with the highest attention scores.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">
                                No data available yet. Start analyzing to see your top
                                performers!
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="pending">
                    <Card>
                        <CardHeader>
                            <CardTitle>Pending Analyses</CardTitle>
                            <CardDescription>
                                Analyses currently being processed.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">
                                No pending analyses at the moment.
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
