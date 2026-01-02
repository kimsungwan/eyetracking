"use client";

import { Button, Card, CardContent, CardHeader, CardTitle } from "@saas/ui";
import { ArrowLeft, Download, ExternalLink } from "lucide-react";

interface ReportViewProps {
    data: {
        original_image: string;
        saliency_map: string;
        report: string;
    };
    onReset: () => void;
}

export function ReportView({ data, onReset }: ReportViewProps) {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <Button variant="outline" onClick={onReset}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Analyze Another
                </Button>
                <Button asChild>
                    <a href={data.report} target="_blank" rel="noopener noreferrer">
                        <Download className="mr-2 h-4 w-4" />
                        Download Report
                    </a>
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Original Image</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <img
                            src={data.original_image}
                            alt="Original"
                            className="w-full h-auto rounded-md border"
                        />
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Saliency Map</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <img
                            src={data.saliency_map}
                            alt="Saliency Map"
                            className="w-full h-auto rounded-md border"
                        />
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
