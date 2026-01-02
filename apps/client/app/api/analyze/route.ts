import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db/drizzle";
import { analyses } from "@/lib/db/schema";
import { auth } from "@/auth";

export async function POST(request: NextRequest) {
    try {
        const session = await auth();
        const formData = await request.formData();

        // Forward the request to the Python API service
        // Assuming the Python service runs on localhost:8000
        const pythonApiUrl = "http://localhost:8000/analyze";

        const response = await fetch(pythonApiUrl, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Python API responded with status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            // Save to database
            await db.insert(analyses).values({
                userId: session?.user?.id ? parseInt(session.user.id) : null,
                originalImage: data.original_image,
                saliencyMap: data.saliency_map,
                report: data.report,
            });
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error("Error forwarding request to Python API:", error);
        return NextResponse.json(
            { success: false, error: "Failed to process image analysis" },
            { status: 500 }
        );
    }
}
