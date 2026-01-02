"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { ReportView } from "@/components/analysis/report-view";
import { Card, CardContent, CardHeader, CardTitle, Table, TableBody, TableCell, TableHead, TableHeader, TableRow, Button, Badge } from "@saas/ui";
import { ArrowLeft, Eye } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

interface AnalysisReport {
    id: number;
    originalImage: string;
    saliencyMap: string;
    report: string;
    createdAt: string;
}

export default function ReportsPage({
    params,
}: {
    params: Promise<{ lng: string }>;
}) {
    const searchParams = useSearchParams();
    const router = useRouter();
    const [reports, setReports] = useState<AnalysisReport[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedReport, setSelectedReport] = useState<AnalysisReport | null>(null);

    const original = searchParams.get("original");
    const saliency = searchParams.get("saliency");
    const report = searchParams.get("report");

    useEffect(() => {
        fetchReports();
    }, []);

    useEffect(() => {
        if (original && saliency && report) {
            setSelectedReport({
                id: 0, // Temp ID
                originalImage: original,
                saliencyMap: saliency,
                report: report,
                createdAt: new Date().toISOString(),
            });
        }
    }, [original, saliency, report]);

    const fetchReports = async () => {
        try {
            const res = await fetch("/api/reports");
            const data = await res.json();
            if (data.success) {
                setReports(data.data);
            }
        } catch (error) {
            console.error("Failed to fetch reports:", error);
        } finally {
            setLoading(false);
        }
    };

    if (selectedReport) {
        return (
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Analysis Report</h1>
                        <p className="text-muted-foreground">
                            Detailed analysis results.
                        </p>
                    </div>
                    <Button variant="outline" onClick={() => {
                        setSelectedReport(null);
                        router.push("/admin/reports"); // Clear query params
                    }}>
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to List
                    </Button>
                </div>

                <ReportView
                    data={{
                        original_image: selectedReport.originalImage,
                        saliency_map: selectedReport.saliencyMap,
                        report: selectedReport.report,
                    }}
                    onReset={() => {
                        setSelectedReport(null);
                        router.push("/analyze");
                    }}
                />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Reports History</h1>
                    <p className="text-muted-foreground">
                        View and manage your generated analysis reports.
                    </p>
                </div>
                <Button asChild>
                    <Link href="/analyze">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        New Analysis
                    </Link>
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Analyses</CardTitle>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="text-center py-8 text-muted-foreground">Loading history...</div>
                    ) : reports.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">
                            You haven't generated any reports yet. Go to the Analyze page to start.
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>ID</TableHead>
                                    <TableHead>Date</TableHead>
                                    <TableHead>Image</TableHead>
                                    <TableHead className="text-right">Action</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {reports.map((item) => (
                                    <TableRow key={item.id}>
                                        <TableCell>{item.id}</TableCell>
                                        <TableCell>{new Date(item.createdAt).toLocaleString()}</TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                <img src={item.originalImage} alt="Thumbnail" className="h-10 w-10 object-cover rounded border" />
                                                <span className="text-xs text-muted-foreground truncate max-w-[200px]">{item.originalImage.split('/').pop()}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button size="sm" variant="ghost" onClick={() => setSelectedReport(item)}>
                                                <Eye className="h-4 w-4 mr-2" />
                                                View
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
