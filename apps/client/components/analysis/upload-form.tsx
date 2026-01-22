"use client";

import { useState, useEffect } from "react";
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Label, Tabs, TabsContent, TabsList, TabsTrigger } from "@saas/ui";
import { Loader2, AlertCircle } from "lucide-react";
import { toast } from "sonner";

const PROGRESS_MESSAGES = [
    "이미지 업로드 중...",
    "시각적 주의 분석 중...",
    "히트맵 생성 중...",
    "UX 리포트 작성 중...",
    "AI 인사이트 분석 중...",
    "결과 저장 중...",
];

interface AnalysisUploadFormProps {
    onAnalysisComplete: (data: any) => void;
}

export function AnalysisUploadForm({ onAnalysisComplete }: AnalysisUploadFormProps) {
    const [file, setFile] = useState<File | null>(null);
    const [url, setUrl] = useState("");
    const [activeTab, setActiveTab] = useState("upload");
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [progressStep, setProgressStep] = useState(0);

    // Rotate through progress messages
    useEffect(() => {
        if (!isUploading) {
            setProgressStep(0);
            return;
        }

        const interval = setInterval(() => {
            setProgressStep((prev) =>
                prev < PROGRESS_MESSAGES.length - 1 ? prev + 1 : prev
            );
        }, 3000);

        return () => clearInterval(interval);
    }, [isUploading]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleResponse = async (response: Response) => {
        console.log("Response status:", response.status, response.statusText);

        let data;
        try {
            const text = await response.text();
            console.log("Raw response:", text);
            data = JSON.parse(text);
        } catch (e) {
            console.error("Failed to parse JSON response:", e);
            throw new Error(`Server responded with ${response.status} ${response.statusText} but returned invalid JSON`);
        }

        console.log("Analysis data:", data);

        // 로그인 필요 에러 처리
        if (data.error === "login_required") {
            toast.error("로그인이 필요합니다.");
            window.location.href = "/sign-in";
            return;
        }

        // 기타 API 에러 처리
        if (!response.ok || !data.success) {
            console.error("Analysis failed. Response:", response.status, data);
            const errorMessage = data.error || `Analysis failed (${response.status}: ${response.statusText})`;
            toast.error(`Error: ${errorMessage}`);
            setError(errorMessage);
            return;
        }

        // 성공 처리
        if (data.subscription_limited) {
            toast.success("분석 완료! (AI 컨설팅, IA, Redesign은 유료 플랜에서 이용 가능합니다)");
        } else {
            toast.success("Analysis complete!");
        }

        // Redirect to Next.js Admin Dashboard
        const params = new URLSearchParams();
        if (data.id) {
            params.append("id", data.id.toString());
        } else {
            params.append("original", data.original_image);
            params.append("saliency", data.saliency_map);
            params.append("report", data.report);
        }

        const pathSegments = window.location.pathname.split('/');
        const lng = pathSegments[1] || 'en';

        const redirectUrl = `/${lng}/admin/reports?${params.toString()}`;
        console.log("Redirecting to:", redirectUrl);
        window.location.href = redirectUrl;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        if (activeTab === "upload" && !file) return;
        if (activeTab === "url" && !url) return;

        setIsUploading(true);

        try {
            let response;
            if (activeTab === "upload" && file) {
                const formData = new FormData();
                formData.append("file", file);
                response = await fetch("/api/analyze", {
                    method: "POST",
                    body: formData,
                });
            } else {
                response = await fetch("/api/analyze", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ url }),
                });
            }

            await handleResponse(response);

        } catch (error: any) {
            console.error("Analysis error:", error);
            const msg = `Failed to connect to analysis server: ${error.message || "Unknown error"}`;
            toast.error(msg);
            setError(msg);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>Start Analysis</CardTitle>
            </CardHeader>
            <CardContent>
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                    <TabsList className="grid w-full grid-cols-2 mb-4">
                        <TabsTrigger value="upload">Image Upload</TabsTrigger>
                        <TabsTrigger value="url">URL Analysis</TabsTrigger>
                    </TabsList>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="bg-red-50 text-red-600 p-3 rounded-md flex items-start gap-2 text-sm border border-red-200">
                                <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                                <span>{error}</span>
                            </div>
                        )}

                        <TabsContent value="upload" className="space-y-4">
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
                        </TabsContent>

                        <TabsContent value="url" className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="url">Webpage URL</Label>
                                <Input
                                    id="url"
                                    type="url"
                                    placeholder="https://example.com"
                                    value={url}
                                    onChange={(e) => setUrl(e.target.value)}
                                    disabled={isUploading}
                                />
                            </div>
                        </TabsContent>

                        <Button type="submit" className="w-full" disabled={isUploading || (activeTab === "upload" && !file) || (activeTab === "url" && !url)}>
                            {isUploading ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    {PROGRESS_MESSAGES[progressStep]}
                                </>
                            ) : (
                                "Analyze"
                            )}
                        </Button>
                    </form>
                </Tabs>
            </CardContent>
        </Card>
    );
}
