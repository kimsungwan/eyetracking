"use client";

import { useState } from "react";
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Label } from "@saas/ui";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

interface AnalysisUploadFormProps {
    onAnalysisComplete: (data: any) => void;
}

export function AnalysisUploadForm({ onAnalysisComplete }: AnalysisUploadFormProps) {
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        setIsUploading(true);
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Call Next.js API Proxy
            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData,
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                throw new Error("Analysis failed");
            }

            const data = await response.json();
            console.log("Analysis data:", data);

            if (data.success) {
                toast.success("Analysis complete!");

                // Redirect to Next.js Admin Dashboard
                // We'll pass the result as query params so the dashboard can potentially display it
                const params = new URLSearchParams({
                    original: data.original_image, // Note: API returns 'original_image' not 'original_image_url' based on main.py
                    saliency: data.saliency_map,   // Note: API returns 'saliency_map' not 'saliency_map_url'
                    report: data.report
                });

                // Get current language from URL or default to 'en'
                const pathSegments = window.location.pathname.split('/');
                const lng = pathSegments[1] || 'en';

                const redirectUrl = `/${lng}/admin/reports?${params.toString()}`;
                console.log("Redirecting to:", redirectUrl);
                window.location.href = redirectUrl;
            } else {
                console.error("Analysis failed with data:", data);
                toast.error(data.error || "Analysis failed");
            }
        } catch (error) {
            console.error(error);
            toast.error("Failed to connect to analysis server.");
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>Upload Image for Analysis</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="image">Image File</Label>
                        <Input
                            id="image"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            disabled={isUploading}
                        />
                    </div>
                    <Button type="submit" className="w-full" disabled={!file || isUploading}>
                        {isUploading ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Analyzing...
                            </>
                        ) : (
                            "Analyze"
                        )}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
