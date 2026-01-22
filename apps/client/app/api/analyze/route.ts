import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db/drizzle";
import { analyses, teams, teamMembers } from "@/lib/db/schema";
import { auth } from "@/auth";
import { eq } from "drizzle-orm";

const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
    try {
        const session = await auth();

        // 로그인 필수
        if (!session?.user?.id) {
            return NextResponse.json(
                { success: false, error: "login_required" },
                { status: 401 }
            );
        }

        // 구독 상태 확인
        const userId = parseInt(session.user.id);
        const teamResult = await db
            .select({ planName: teams.planName })
            .from(teamMembers)
            .innerJoin(teams, eq(teamMembers.teamId, teams.id))
            .where(eq(teamMembers.userId, userId))
            .limit(1);

        const planName = teamResult[0]?.planName;
        const isPaidUser = planName && ["basic", "pro"].includes(planName);
        const userPlan = planName || "free";

        const contentType = request.headers.get("content-type") || "";
        let pythonApiUrl = "";
        let requestBody: any;
        let headers: any = {};

        if (contentType.includes("application/json")) {
            // URL Analysis
            const jsonBody = await request.json();
            pythonApiUrl = `${PYTHON_API_URL}/analyze-url`;
            requestBody = JSON.stringify({ ...jsonBody, plan: userPlan });
            headers = { "Content-Type": "application/json" };
        } else {
            // Image Upload
            const formData = await request.formData();
            // Pass plan as query parameter for file upload endpoint
            pythonApiUrl = `${PYTHON_API_URL}/analyze?plan=${userPlan}`;
            requestBody = formData;
            // fetch automatically sets Content-Type for FormData
        }

        console.log(`Forwarding request to Python API: ${pythonApiUrl} (Plan: ${userPlan})`);

        const response = await fetch(pythonApiUrl, {
            method: "POST",
            body: requestBody,
            headers: headers,
        });

        console.log(`Python API response status: ${response.status}`);

        const responseText = await response.text();
        console.log(`Python API raw response: ${responseText}`);

        if (!response.ok) {
            console.error(`Python API error: ${response.status} - ${responseText}`);
            throw new Error(`Python API responded with status: ${response.status}. Details: ${responseText}`);
        }

        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error("Failed to parse Python API response:", e);
            throw new Error(`Invalid JSON from Python API: ${responseText}`);
        }

        console.log("Python API response data:", data);

        if (data.success) {
            // 무료 사용자의 경우 AI 마케팅 컨설팅, IA, Redesign 제거
            if (!isPaidUser) {
                data.marketing_consultation = null;
                data.ia_structure = null;
                data.redesign_suggestion = null;
                data.subscription_limited = true; // 프론트엔드에 제한 알림
            }

            // Save to database
            const insertedId = await db.insert(analyses).values({
                userId: userId,
                originalImage: data.original_image,
                saliencyMap: data.saliency_map,
                report: data.report,
                iaStructure: isPaidUser ? data.ia_structure : null,
                redesignSuggestion: isPaidUser ? data.redesign_suggestion : null,
                marketingConsultation: isPaidUser ? data.marketing_consultation : null,
                metrics: data.metrics,
            }).returning({ id: analyses.id });

            if (insertedId && insertedId[0]) {
                data.id = insertedId[0].id;
            }
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error("Error forwarding request to Python API:", error);
        return NextResponse.json(
            { success: false, error: "Failed to process analysis" },
            { status: 500 }
        );
    }
}
