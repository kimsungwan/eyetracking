"use client";

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
import { Eye, Zap, Layers, Brain } from "lucide-react";
import Link from "next/link";
import { useReports, AnalysisReport } from "@/lib/hooks/useReports";

export default function AdminDashboardPage() {
    const { reports, isLoading: loading } = useReports();

    // Get the latest report with metrics
    const latestReport = reports.length > 0 ? reports[0] : null;
    const latestMetrics = latestReport?.metrics;

    // Helper function to get score color
    const getScoreColor = (score: number, inverse: boolean = false) => {
        if (inverse) {
            // Lower is better (like VCI, CLE)
            if (score <= 30) return "text-green-500";
            if (score <= 60) return "text-yellow-500";
            return "text-red-500";
        }
        // Higher is better (like ACS)
        if (score >= 70) return "text-green-500";
        if (score >= 40) return "text-yellow-500";
        return "text-red-500";
    };

    const getScoreLabel = (score: number, inverse: boolean = false) => {
        if (inverse) {
            if (score <= 30) return "매우 좋음";
            if (score <= 60) return "보통";
            return "개선 필요";
        }
        if (score >= 70) return "매우 좋음";
        if (score >= 40) return "보통";
        return "개선 필요";
    };

    const statsCards = [
        {
            title: "총 분석 횟수",
            value: reports.length.toString(),
            description: latestReport
                ? `최근: ${new Date(latestReport.createdAt).toLocaleDateString('ko-KR')}`
                : "분석을 시작해보세요",
            icon: Eye,
            color: "text-blue-500",
        },
        {
            title: "주의 집중 점수 (ACS)",
            value: latestMetrics?.advanced?.acs?.toFixed(1) || "—",
            description: latestMetrics?.advanced?.acs
                ? getScoreLabel(latestMetrics.advanced.acs)
                : "사용자가 디자인에 집중하는 정도",
            icon: Zap,
            color: latestMetrics?.advanced?.acs
                ? getScoreColor(latestMetrics.advanced.acs)
                : "text-orange-500",
        },
        {
            title: "시각 복잡도 (VCI)",
            value: latestMetrics?.advanced?.vci?.toFixed(1) || "—",
            description: latestMetrics?.advanced?.vci
                ? getScoreLabel(latestMetrics.advanced.vci, true)
                : "디자인의 시각적 혼잡도 (낮을수록 좋음)",
            icon: Layers,
            color: latestMetrics?.advanced?.vci
                ? getScoreColor(latestMetrics.advanced.vci, true)
                : "text-purple-500",
        },
        {
            title: "인지 부하 (CLE)",
            value: latestMetrics?.advanced?.cle?.toFixed(1) || "—",
            description: latestMetrics?.advanced?.cle
                ? getScoreLabel(latestMetrics.advanced.cle, true)
                : "사용자가 느끼는 인지적 부담 (낮을수록 좋음)",
            icon: Brain,
            color: latestMetrics?.advanced?.cle
                ? getScoreColor(latestMetrics.advanced.cle, true)
                : "text-indigo-500",
        },
    ];

    const recentAnalyses = reports.slice(0, 5);

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
                <p className="text-muted-foreground">
                    {latestReport
                        ? "최신 분석 결과를 한눈에 확인하세요."
                        : "Welcome back! Start your first analysis to see metrics here."}
                </p>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {loading ? (
                    Array.from({ length: 4 }).map((_, i) => (
                        <Card key={i}>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <div className="h-4 w-24 bg-muted animate-pulse rounded" />
                            </CardHeader>
                            <CardContent>
                                <div className="h-8 w-16 bg-muted animate-pulse rounded mb-2" />
                                <div className="h-3 w-32 bg-muted animate-pulse rounded" />
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    statsCards.map((stat) => (
                        <Card key={stat.title}>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                                <stat.icon className={`h-4 w-4 ${stat.color}`} />
                            </CardHeader>
                            <CardContent>
                                <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
                                <p className="text-xs text-muted-foreground">
                                    {stat.description}
                                </p>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>

            {/* Notice for new users */}
            {!loading && reports.length === 0 && (
                <Card className="border-dashed border-2 bg-muted/30">
                    <CardContent className="flex flex-col items-center justify-center py-10">
                        <Eye className="h-12 w-12 text-muted-foreground mb-4" />
                        <h3 className="text-lg font-semibold mb-2">아직 분석된 레포트가 없습니다</h3>
                        <p className="text-muted-foreground text-center mb-4">
                            첫 번째 분석을 시작하여 UX 메트릭을 확인해보세요.
                        </p>
                        <Link
                            href="/analyze"
                            className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"
                        >
                            분석 시작하기 →
                        </Link>
                    </CardContent>
                </Card>
            )}

            {/* Tabs Section */}
            {reports.length > 0 && (
                <Tabs defaultValue="recent" className="space-y-4">
                    <TabsList>
                        <TabsTrigger value="recent">Recent Analyses</TabsTrigger>
                        <TabsTrigger value="insights">Latest Insights</TabsTrigger>
                    </TabsList>

                    <TabsContent value="recent">
                        <Card>
                            <CardHeader>
                                <CardTitle>최근 분석</CardTitle>
                                <CardDescription>
                                    최근 완료된 UX 분석 목록입니다.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>ID</TableHead>
                                            <TableHead>이미지</TableHead>
                                            <TableHead>날짜</TableHead>
                                            <TableHead>ACS</TableHead>
                                            <TableHead>VCI</TableHead>
                                            <TableHead className="text-right">액션</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {recentAnalyses.map((analysis) => (
                                            <TableRow key={analysis.id}>
                                                <TableCell className="font-medium">
                                                    #{analysis.id}
                                                </TableCell>
                                                <TableCell>
                                                    <img
                                                        src={analysis.originalImage}
                                                        alt="Thumbnail"
                                                        className="h-10 w-10 object-cover rounded border"
                                                    />
                                                </TableCell>
                                                <TableCell>
                                                    {new Date(analysis.createdAt).toLocaleDateString('ko-KR')}
                                                </TableCell>
                                                <TableCell>
                                                    {analysis.metrics?.advanced?.acs ? (
                                                        <span className={getScoreColor(analysis.metrics.advanced.acs)}>
                                                            {analysis.metrics.advanced.acs.toFixed(1)}
                                                        </span>
                                                    ) : (
                                                        <span className="text-muted-foreground">—</span>
                                                    )}
                                                </TableCell>
                                                <TableCell>
                                                    {analysis.metrics?.advanced?.vci ? (
                                                        <span className={getScoreColor(analysis.metrics.advanced.vci, true)}>
                                                            {analysis.metrics.advanced.vci.toFixed(1)}
                                                        </span>
                                                    ) : (
                                                        <span className="text-muted-foreground">—</span>
                                                    )}
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    <Link
                                                        href={`/admin/reports?id=${analysis.id}`}
                                                        className="text-blue-500 hover:underline text-sm"
                                                    >
                                                        View →
                                                    </Link>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="insights">
                        <Card>
                            <CardHeader>
                                <CardTitle>최신 AI 인사이트</CardTitle>
                                <CardDescription>
                                    가장 최근 분석의 마케팅 AI 컨설턴트 결과입니다.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                {!latestReport?.marketingConsultation || (latestReport.marketingConsultation as any).error ? (
                                    <p className="text-muted-foreground">
                                        AI 인사이트가 있는 분석이 없습니다.{" "}
                                        <Link href="/analyze" className="text-blue-500 hover:underline">
                                            분석 시작하기
                                        </Link>
                                    </p>
                                ) : (
                                    <div className="space-y-4">
                                        <div className="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
                                            <h4 className="font-semibold text-indigo-900 mb-2">진단 (Diagnosis)</h4>
                                            <p className="text-sm text-slate-700">
                                                {(latestReport.marketingConsultation as any).diagnosis}
                                            </p>
                                        </div>
                                        <div className="bg-red-50 p-4 rounded-lg border border-red-100">
                                            <h4 className="font-semibold text-red-900 mb-2">비평 (Critique)</h4>
                                            <p className="text-sm text-slate-700">
                                                {(latestReport.marketingConsultation as any).critique}
                                            </p>
                                        </div>
                                        <div className="flex justify-end">
                                            <Link
                                                href={`/admin/reports?id=${latestReport.id}`}
                                                className="text-blue-500 hover:underline text-sm"
                                            >
                                                전체 레포트 보기 →
                                            </Link>
                                        </div>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            )}
        </div>
    );
}
