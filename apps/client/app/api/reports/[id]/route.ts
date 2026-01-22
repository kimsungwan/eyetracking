import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db/drizzle";
import { analyses } from "@/lib/db/schema";
import { eq } from "drizzle-orm";
import { auth } from "@/auth";

const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const session = await auth();
        if (!session?.user?.id) {
            return NextResponse.json(
                { success: false, error: "Unauthorized" },
                { status: 401 }
            );
        }

        const { id } = await params;
        const reportId = parseInt(id);

        if (isNaN(reportId)) {
            return NextResponse.json(
                { success: false, error: "Invalid report ID" },
                { status: 400 }
            );
        }

        // 1. Fetch the report to get filenames
        const report = await db.query.analyses.findFirst({
            where: eq(analyses.id, reportId),
        });

        if (!report) {
            return NextResponse.json(
                { success: false, error: "Report not found" },
                { status: 404 }
            );
        }

        // Check ownership
        if (report.userId !== parseInt(session.user.id)) {
            return NextResponse.json(
                { success: false, error: "Unauthorized" },
                { status: 403 }
            );
        }

        // 2. Call Python Service to delete files
        // Extract filenames/paths from report object
        // The Python service expects relative paths like "uploads/uuid.png"
        // Our DB stores "uploads/uuid.png" or similar.

        const filesToDelete = [
            report.originalImage,
            report.saliencyMap,
            report.report
        ].filter(Boolean); // Remove null/undefined

        if (filesToDelete.length > 0) {
            try {
                const pythonApiUrl = `${PYTHON_API_URL}/delete-files`;
                await fetch(pythonApiUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ files: filesToDelete }),
                });
                // We don't strictly fail if file deletion fails, but we log it.
            } catch (error) {
                console.error("Failed to delete files from Python service:", error);
            }
        }

        // 3. Delete from Database
        await db.delete(analyses).where(eq(analyses.id, reportId));

        return NextResponse.json({ success: true });

    } catch (error) {
        console.error("Error deleting report:", error);
        return NextResponse.json(
            { success: false, error: "Failed to delete report" },
            { status: 500 }
        );
    }
}
