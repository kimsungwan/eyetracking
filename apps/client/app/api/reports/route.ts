import { NextResponse } from "next/server";
import { db } from "@/lib/db/drizzle";
import { analyses } from "@/lib/db/schema";
import { desc, eq } from "drizzle-orm";
import { auth } from "@/auth";

export async function GET() {
    try {
        const session = await auth();

        if (!session?.user?.id) {
            return NextResponse.json(
                { success: false, error: "Unauthorized" },
                { status: 401 }
            );
        }

        const results = await db
            .select()
            .from(analyses)
            .where(eq(analyses.userId, parseInt(session.user.id)))
            .orderBy(desc(analyses.createdAt));

        return NextResponse.json({ success: true, data: results });
    } catch (error) {
        console.error("Error fetching reports:", error);
        return NextResponse.json(
            { success: false, error: "Failed to fetch reports" },
            { status: 500 }
        );
    }
}
