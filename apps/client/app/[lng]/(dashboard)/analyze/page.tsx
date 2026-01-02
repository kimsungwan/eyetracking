"use client";

import { useState } from "react";
import { AnalysisUploadForm } from "@/components/analysis/upload-form";
import { ReportView } from "@/components/analysis/report-view";

export default function AnalyzePage() {
    const [analysisResult, setAnalysisResult] = useState<any>(null);

    return (
        <div className="container mx-auto py-8 space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">AI Analysis</h1>
                <p className="text-muted-foreground">
                    Upload an image to generate a saliency map and analysis report.
                </p>
            </div>

            {analysisResult ? (
                <ReportView
                    data={analysisResult}
                    onReset={() => setAnalysisResult(null)}
                />
            ) : (
                <AnalysisUploadForm onAnalysisComplete={setAnalysisResult} />
            )}
        </div>
    );
}
