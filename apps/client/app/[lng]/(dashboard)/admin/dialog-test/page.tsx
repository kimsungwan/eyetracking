"use client";

import { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from "@saas/ui";

export default function DialogTestPage() {
    const [isOpen, setIsOpen] = useState(false);

    console.log("[DialogTestPage] Rendered. isOpen:", isOpen);

    return (
        <div className="p-10">
            <h1 className="text-3xl font-bold mb-6">Dialog Test Page</h1>

            <p className="mb-4">Current state: <strong>{isOpen ? "OPEN" : "CLOSED"}</strong></p>

            <button
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
                onClick={() => {
                    console.log("[DialogTestPage] Button clicked, setting isOpen to true");
                    setIsOpen(true);
                }}
            >
                Open Dialog
            </button>

            <Dialog open={isOpen} onOpenChange={(open) => {
                console.log("[DialogTestPage] onOpenChange:", open);
                setIsOpen(open);
            }}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Test Dialog</DialogTitle>
                        <DialogDescription>
                            If you can see this, the Dialog is working!
                        </DialogDescription>
                    </DialogHeader>
                    <div className="p-4 mt-4 bg-green-100 rounded-lg text-green-800 font-bold text-center text-xl">
                        ✅ SUCCESS! Dialog is visible!
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
