"use client";

import { useSearchParams, useRouter } from "next/navigation";
import dynamic from "next/dynamic";

const ReportView = dynamic(
    () => import("@/components/analysis/report-view").then((mod) => mod.ReportView),
    {
        ssr: false,
        loading: () => (
            <div className="space-y-4 animate-pulse">
                <div className="h-64 bg-muted rounded-lg" />
                <div className="h-32 bg-muted rounded-lg" />
            </div>
        ),
    }
);
import { Card, CardContent, CardHeader, CardTitle, Table, TableBody, TableCell, TableHead, TableHeader, TableRow, Button, Badge } from "@saas/ui";
import { ArrowLeft, Eye, Trash2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import useSWR from "swr";
import { fetcher } from "@/lib/fetcher";
import { ReportsTableSkeleton } from "@/components/skeletons/reports-skeleton";
import { ConfirmDialog } from "@/components/ui/confirm-dialog";

interface AnalysisReport {
    id: number;
    originalImage: string;
    saliencyMap: string;
    report: string;
    iaStructure?: any;
    redesignSuggestion?: any;
    marketingConsultation?: any;
    createdAt: string;
}

export default function ReportsPage({
    params,
}: {
    params: Promise<{ lng: string }>;
}) {
    const searchParams = useSearchParams();
    const router = useRouter();
    // const [reports, setReports] = useState<AnalysisReport[]>([]); // Replaced by SWR
    // const [loading, setLoading] = useState(true); // Replaced by SWR
    const [selectedReport, setSelectedReport] = useState<AnalysisReport | null>(null);
    const [deleteId, setDeleteId] = useState<number | null>(null);

    const { data, error, mutate } = useSWR<{ success: boolean; data: AnalysisReport[] }>("/api/reports", fetcher);

    const reports = data?.data || [];
    const loading = !data && !error;

    const original = searchParams.get("original");
    const saliency = searchParams.get("saliency");
    const report = searchParams.get("report");

    const id = searchParams.get("id");

    // useEffect(() => {
    //     fetchReports();
    // }, []);

    useEffect(() => {
        if (id && reports.length > 0) {
            const reportId = parseInt(id);
            const found = reports.find(r => r.id === reportId);
            if (found) {
                setSelectedReport(found);
            }
        } else if (original && saliency && report) {
            setSelectedReport({
                id: 0, // Temp ID
                originalImage: original,
                saliencyMap: saliency,
                report: report,
                createdAt: new Date().toISOString(),
            });
        }
    }, [id, reports, original, saliency, report]);

    // const fetchReports = async () => { ... } // Removed in favor of SWR

    const handleDelete = async (id: number) => {
        // Optimistic update
        mutate(
            { ...data!, data: reports.filter((r) => r.id !== id) },
            false // Do not revalidate immediately
        );

        try {
            const res = await fetch(`/api/reports/${id}`, {
                method: "DELETE",
            });
            const resData = await res.json();
            if (resData.success) {
                // If the deleted report was selected, clear selection
                if (selectedReport?.id === id) {
                    setSelectedReport(null);
                }
                // Trigger revalidation to ensure data consistency
                mutate();
            } else {
                alert("Failed to delete report: " + resData.error);
                // Revert optimistic update
                mutate();
            }
        } catch (error) {
            console.error("Error deleting report:", error);
            alert("An error occurred while deleting the report.");
            // Revert optimistic update
            mutate();
        }
    };

    const [activeTab, setActiveTab] = useState<'report' | 'ai'>('report');

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

                <div className="flex space-x-1 rounded-xl bg-muted p-1">
                    <button
                        onClick={() => setActiveTab('report')}
                        className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 ${activeTab === 'report'
                            ? 'bg-white text-blue-700 shadow'
                            : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                            } ${activeTab === 'report' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:bg-muted-foreground/10'}`}
                    >
                        Full Report
                    </button>
                    <button
                        onClick={() => setActiveTab('ai')}
                        className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 ${activeTab === 'ai'
                            ? 'bg-white text-blue-700 shadow'
                            : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                            } ${activeTab === 'ai' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:bg-muted-foreground/10'}`}
                    >
                        AI Insights & Generative UI
                    </button>
                </div>

                {activeTab === 'report' ? (
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
                ) : (

                    <div className="grid gap-6 md:grid-cols-2">
                        {/* Marketing Consultant Report (Full Width) */}
                        <Card className="md:col-span-2 border-indigo-200 bg-indigo-50/30">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-indigo-700">
                                    <span className="text-xl">🧠</span> Marketing AI Consultant
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {selectedReport.marketingConsultation ? (
                                    (selectedReport.marketingConsultation as any).error ? (
                                        <div className="p-6 bg-red-50 text-red-700 rounded-lg border border-red-200">
                                            <h4 className="font-bold flex items-center gap-2">
                                                <span>⚠️</span> Analysis Failed
                                            </h4>
                                            <p className="mt-2 text-sm">{(selectedReport.marketingConsultation as any).error}</p>
                                        </div>
                                    ) : (
                                        <>
                                            {console.log("Marketing Data:", selectedReport.marketingConsultation)}
                                            {/* Diagnosis */}
                                            <div className="bg-white p-4 rounded-lg border border-indigo-100 shadow-sm">
                                                <h4 className="font-semibold text-indigo-900 mb-2">Diagnosis</h4>
                                                <p className="text-slate-700 leading-relaxed">
                                                    {(selectedReport.marketingConsultation as any).diagnosis}
                                                </p>
                                            </div>

                                            <div className="grid md:grid-cols-2 gap-4">
                                                {/* Critique */}
                                                <div className="bg-white p-4 rounded-lg border border-red-100 shadow-sm">
                                                    <h4 className="font-semibold text-red-900 mb-2">Critique</h4>
                                                    <p className="text-slate-700 text-sm">
                                                        {(selectedReport.marketingConsultation as any).critique}
                                                    </p>
                                                </div>

                                                {/* Applied Theories */}
                                                <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm">
                                                    <h4 className="font-semibold text-blue-900 mb-2">Applied Theories</h4>
                                                    <div className="flex flex-wrap gap-2">
                                                        {(selectedReport.marketingConsultation as any).applied_theories?.map((theory: string, i: number) => (
                                                            <Badge key={i} variant="secondary" className="bg-blue-100 text-blue-700 hover:bg-blue-200">
                                                                {theory}
                                                            </Badge>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Action Plan */}
                                            <div className="bg-white p-4 rounded-lg border border-green-100 shadow-sm">
                                                <h4 className="font-semibold text-green-900 mb-3">Action Plan</h4>
                                                <ul className="space-y-2">
                                                    {(selectedReport.marketingConsultation as any).action_plan?.map((step: string, i: number) => (
                                                        <li key={i} className="flex items-start gap-2 text-slate-700 text-sm">
                                                            <span className="bg-green-100 text-green-700 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                                                {i + 1}
                                                            </span>
                                                            {step}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </>
                                    )
                                ) : (
                                    <div className="text-muted-foreground text-center py-10">
                                        Marketing consultation data not available.
                                    </div>
                                )}
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Information Architecture (IA)</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="bg-slate-50 p-4 rounded-lg border min-h-[300px] overflow-auto font-mono text-sm">
                                    {selectedReport.iaStructure ? (
                                        <IATreeNode node={selectedReport.iaStructure} />
                                    ) : (
                                        <div className="text-muted-foreground text-center mt-10">IA Structure not available</div>
                                    )}
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Generative UI Redesign</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {selectedReport.redesignSuggestion ? (
                                    <>
                                        <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded-r-lg">
                                            <h4 className="text-purple-700 font-semibold mb-2">AI Critique</h4>
                                            <p className="text-purple-900 text-sm">
                                                {(selectedReport.redesignSuggestion as any).critique}
                                            </p>
                                        </div>

                                        <div>
                                            <h4 className="font-semibold mb-2">Suggested Improvements</h4>
                                            <p className="text-sm text-muted-foreground">
                                                {(selectedReport.redesignSuggestion as any).redesign_description}
                                            </p>
                                        </div>

                                        <div>
                                            <h4 className="font-semibold mb-2">Image Generation Prompt</h4>
                                            <div className="bg-slate-100 p-3 rounded text-xs text-slate-600 font-mono break-all">
                                                {(selectedReport.redesignSuggestion as any).image_gen_prompt}
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <div className="text-muted-foreground text-center mt-10">Redesign suggestion not available</div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                )
                }
            </div >
        );
    }

    return (
        <>
            <DeleteConfirmDialogWrapper deleteId={deleteId} setDeleteId={setDeleteId} handleDelete={handleDelete} />
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
                            <ReportsTableSkeleton />
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
                                                <div className="flex justify-end gap-2">
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        onClick={() => setSelectedReport(item)}
                                                        aria-label="View report"
                                                    >
                                                        <Eye className="h-4 w-4 mr-1" />
                                                        View
                                                    </Button>
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            setDeleteId(item.id);
                                                        }}
                                                        aria-label="Delete report"
                                                    >
                                                        <Trash2 className="h-4 w-4 mr-1" />
                                                        Delete
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </CardContent>
                </Card>
            </div>
        </>
    );
}

function DeleteConfirmDialogWrapper({ deleteId, setDeleteId, handleDelete }: { deleteId: number | null, setDeleteId: (id: number | null) => void, handleDelete: (id: number) => void }) {
    return (
        <ConfirmDialog
            open={deleteId !== null}
            onOpenChange={(open) => !open && setDeleteId(null)}
            title="Delete Report"
            description="Are you sure you want to delete this report? This action cannot be undone."
            onConfirm={() => {
                if (deleteId !== null) {
                    handleDelete(deleteId);
                }
            }}
            confirmText="Delete"
            cancelText="Cancel"
            variant="destructive"
        />
    );
}

function IATreeNode({ node }: { node: any }) {
    if (!node) return null;
    return (
        <ul className="pl-4 border-l border-slate-200">
            <li className="mt-2">
                <span className="font-semibold text-slate-700">{node.label}</span>
                <span className="text-xs text-slate-400 ml-2">({node.type})</span>
                {node.children && node.children.length > 0 && (
                    <div className="ml-2">
                        {node.children.map((child: any, i: number) => (
                            <IATreeNode key={i} node={child} />
                        ))}
                    </div>
                )}
            </li>
        </ul>
    );
}
