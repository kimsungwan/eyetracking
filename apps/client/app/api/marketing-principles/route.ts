import { NextResponse } from "next/server";

const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

export async function GET() {
    try {
        const pythonApiUrl = `${PYTHON_API_URL}/marketing-principles`;
        const response = await fetch(pythonApiUrl);

        if (!response.ok) {
            throw new Error(`Python API responded with status: ${response.status}`);
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error("Error fetching marketing principles:", error);
        return NextResponse.json(
            { success: false, error: "Failed to fetch marketing principles" },
            { status: 500 }
        );
    }
}
