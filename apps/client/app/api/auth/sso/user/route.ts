import { auth } from "@/auth";
import { NextResponse } from "next/server";

export async function GET() {
    const session = await auth();

    if (!session || !session.user) {
        return NextResponse.json(
            { code: 401, message: "Unauthorized" },
            { status: 401 }
        );
    }

    // Return data in the format vue-element-admin expects
    // The default mock data in vue-element-admin uses code 20000 for success
    return NextResponse.json({
        code: 20000,
        data: {
            roles: [session.user.role || "admin"], // Vue admin expects an array of roles
            name: session.user.name,
            avatar: session.user.image || "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            introduction: `User ID: ${session.user.id}`,
        },
    });
}
