import { Metadata } from "next";
import { MarketingPrinciplesList } from "@/components/docs/marketing-principles-list";

export const metadata: Metadata = {
    title: "Marketing Principles & UX Psychology | Admin Docs",
    description: "Comprehensive guide to marketing principles, cognitive psychology effects, and UX laws used in our AI analysis.",
    keywords: ["Marketing Principles", "UX Psychology", "Cognitive Bias", "Hick's Law", "Color Psychology", "Gestalt Principles"],
};

async function getPrinciples() {
    try {
        // Use BASE_URL for server-side fetch (required in Server Components)
        const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || process.env.VERCEL_URL
            ? `https://${process.env.VERCEL_URL}`
            : "http://localhost:3000";

        const res = await fetch(`${baseUrl}/api/marketing-principles`, {
            cache: "no-store",
        });
        if (!res.ok) return [];
        const json = await res.json();
        return json.success ? json.data : [];
    } catch (e) {
        console.error(e);
        return [];
    }
}

export default async function MarketingDocsPage() {
    const principles = await getPrinciples();

    return (
        <div className="container mx-auto py-10">
            <MarketingPrinciplesList principles={principles} />
        </div>
    );
}
