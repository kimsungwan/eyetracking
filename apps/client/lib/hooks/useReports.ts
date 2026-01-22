import useSWR from "swr";
import { fetcher } from "@/lib/fetcher";

export interface AnalysisReport {
    id: number;
    originalImage: string;
    saliencyMap: string;
    report: string;
    iaStructure?: any;
    redesignSuggestion?: any;
    marketingConsultation?: any;
    metrics?: {
        basic?: {
            clutter_score: number;
            focus_ratio: number;
            hotspot_count: number;
        };
        advanced?: {
            acs: number;
            vci: number;
            cle: number;
        };
    };
    createdAt: string;
}

interface UseReportsResponse {
    success: boolean;
    data: AnalysisReport[];
}

export function useReports() {
    const { data, error, mutate } = useSWR<UseReportsResponse>(
        "/api/reports",
        fetcher
    );

    return {
        reports: data?.data || [],
        isLoading: !data && !error,
        isError: !!error,
        error,
        mutate,
    };
}
