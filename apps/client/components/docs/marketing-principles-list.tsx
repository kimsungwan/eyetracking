"use client";

import { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogTrigger,
    Badge
} from "@saas/ui";
import { DocImage } from "@/components/docs/doc-image";
import {
    LayoutGrid,
    Brain,
    Eye,
    MousePointerClick,
    Users,
    Zap,
    Palette,
    ArrowRight,
    Search,
    Filter,
    Lightbulb,
    Target,
    BookOpen
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Principle {
    id: string;
    concept: string;
    category: string;
    definition: string;
    image?: string;
    visual_triggers: string[];
    actionable_advice?: string[];
    case_study?: string;
    expected_impact?: string;
}

interface MarketingPrinciplesListProps {
    principles: Principle[];
}

const CATEGORY_CONFIG: Record<string, { icon: any; color: string; bg: string; text: string }> = {
    "Cognitive Psychology": {
        icon: Brain,
        color: "text-purple-600 dark:text-purple-400",
        bg: "bg-purple-50 dark:bg-purple-900/30",
        text: "text-purple-600 dark:text-purple-400"
    },
    "Visual Perception": {
        icon: Eye,
        color: "text-blue-600 dark:text-blue-400",
        bg: "bg-blue-50 dark:bg-blue-900/30",
        text: "text-blue-600 dark:text-blue-400"
    },
    "Behavioral Economics": {
        icon: Zap,
        color: "text-orange-600 dark:text-orange-400",
        bg: "bg-orange-50 dark:bg-orange-900/30",
        text: "text-orange-600 dark:text-orange-400"
    },
    "User Behavior": {
        icon: MousePointerClick,
        color: "text-emerald-600 dark:text-emerald-400",
        bg: "bg-emerald-50 dark:bg-emerald-900/30",
        text: "text-emerald-600 dark:text-emerald-400"
    },
    "Social Psychology": {
        icon: Users,
        color: "text-rose-600 dark:text-rose-400",
        bg: "bg-rose-50 dark:bg-rose-900/30",
        text: "text-rose-600 dark:text-rose-400"
    },
    "Color Psychology": {
        icon: Palette,
        color: "text-pink-600 dark:text-pink-400",
        bg: "bg-pink-50 dark:bg-pink-900/30",
        text: "text-pink-600 dark:text-pink-400"
    },
    "General": {
        icon: LayoutGrid,
        color: "text-gray-600 dark:text-gray-400",
        bg: "bg-gray-50 dark:bg-gray-800",
        text: "text-gray-600 dark:text-gray-400"
    },
    "UX Law": {
        icon: LayoutGrid,
        color: "text-indigo-600 dark:text-indigo-400",
        bg: "bg-indigo-50 dark:bg-indigo-900/30",
        text: "text-indigo-600 dark:text-indigo-400"
    },
    "Productivity": {
        icon: Zap,
        color: "text-yellow-600 dark:text-yellow-400",
        bg: "bg-yellow-50 dark:bg-yellow-900/30",
        text: "text-yellow-600 dark:text-yellow-400"
    },
    "Design Psychology": {
        icon: Palette,
        color: "text-cyan-600 dark:text-cyan-400",
        bg: "bg-cyan-50 dark:bg-cyan-900/30",
        text: "text-cyan-600 dark:text-cyan-400"
    }
};

export function MarketingPrinciplesList({ principles }: MarketingPrinciplesListProps) {
    const [activeCategory, setActiveCategory] = useState("All");
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedPrinciple, setSelectedPrinciple] = useState<Principle | null>(null);

    console.log("[MarketingPrinciplesList] Rendered. Selected Principle:", selectedPrinciple?.concept);

    const categories = ["All", ...Array.from(new Set(principles.map((p) => p.category)))];

    const filteredPrinciples = principles.filter((p) => {
        const matchesCategory = activeCategory === "All" || p.category === activeCategory;
        const matchesSearch =
            p.concept.toLowerCase().includes(searchQuery.toLowerCase()) ||
            p.definition.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesCategory && matchesSearch;
    });

    return (
        <div className="space-y-8">
            {/* Search and Filters */}
            <div className="flex flex-col gap-6">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <span className="text-xs font-bold uppercase tracking-wider text-primary mb-1 block">Knowledge Base</span>
                        <h2 className="text-3xl font-bold tracking-tight">Explore Principles</h2>
                    </div>
                    <div className="relative w-full md:w-96">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <Search className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <input
                            className="block w-full pl-10 pr-3 py-2.5 rounded-xl border border-input bg-background text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                            placeholder="Search laws, biases, or methods..."
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                </div>

                <div className="flex gap-3 overflow-x-auto pb-2 no-scrollbar mask-linear-fade">
                    {categories.map((category) => (
                        <button
                            key={category}
                            onClick={() => setActiveCategory(category)}
                            className={cn(
                                "flex h-9 items-center justify-center px-6 rounded-full text-sm font-medium transition-colors whitespace-nowrap",
                                activeCategory === category
                                    ? "bg-primary text-primary-foreground shadow-md shadow-primary/25"
                                    : "bg-background border border-input text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                            )}
                        >
                            {category}
                        </button>
                    ))}
                </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredPrinciples.map((item) => {
                    const config = CATEGORY_CONFIG[item.category] || CATEGORY_CONFIG["General"];
                    const Icon = config.icon;

                    return (
                        <div
                            key={item.id}
                            className="group bg-card rounded-2xl shadow-sm border border-border p-6 flex flex-col hover:shadow-md transition-all duration-300 hover:-translate-y-1 cursor-pointer"
                            onClick={() => {
                                setTimeout(() => {
                                    setSelectedPrinciple(item);
                                }, 0);
                            }}
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className={cn("h-12 w-12 rounded-xl flex items-center justify-center", config.bg, config.text)}>
                                    <Icon className="h-7 w-7" />
                                </div>
                                <span className="text-xs font-semibold text-muted-foreground bg-muted px-2 py-1 rounded">
                                    {item.category}
                                </span>
                            </div>

                            <h3 className="text-lg font-bold mb-2 group-hover:text-primary transition-colors">
                                {item.concept}
                            </h3>

                            <p className="text-sm text-muted-foreground leading-relaxed mb-6 flex-1 line-clamp-3">
                                {item.definition}
                            </p>

                            {item.image && (
                                <div className="mb-4 rounded-lg overflow-hidden h-32 relative hidden group-hover:block transition-all duration-500 animate-in fade-in zoom-in-95">
                                    <DocImage src={item.image} alt={item.concept} />
                                </div>
                            )}

                            <button
                                className="w-full py-2.5 rounded-lg border border-input text-sm font-semibold hover:bg-accent hover:text-accent-foreground transition-colors flex items-center justify-center gap-2 group-hover:border-primary/30 group-hover:text-primary mt-auto"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    e.preventDefault();
                                    console.log("[MarketingPrinciplesList] Clicked Learn More for:", item.concept);
                                    // Delay to prevent Radix from detecting this as an outside click
                                    setTimeout(() => {
                                        setSelectedPrinciple(item);
                                    }, 0);
                                }}
                            >
                                Learn More
                                <ArrowRight className="h-4 w-4" />
                            </button>
                        </div>
                    );
                })}
            </div>

            {filteredPrinciples.length === 0 && (
                <div className="text-center py-20 text-muted-foreground">
                    No principles found matching your criteria.
                </div>
            )}

            {/* Detail Modal */}
            <Dialog
                open={!!selectedPrinciple}
                onOpenChange={(open) => {
                    console.log("[MarketingPrinciplesList] Dialog onOpenChange:", open);
                    if (!open) setSelectedPrinciple(null);
                }}
            >
                <DialogContent
                    className="max-w-3xl max-h-[90vh] overflow-y-auto"
                    onPointerDownOutside={(e) => {
                        // Prevent closing when clicking outside during the same event loop
                        console.log("[MarketingPrinciplesList] onPointerDownOutside prevented");
                        e.preventDefault();
                    }}
                    onInteractOutside={(e) => {
                        console.log("[MarketingPrinciplesList] onInteractOutside prevented");
                        e.preventDefault();
                    }}
                >
                    {selectedPrinciple && (
                        <>
                            <DialogHeader>
                                <div className="flex items-center gap-2 mb-2">
                                    <Badge variant="outline" className="text-xs font-medium">
                                        {selectedPrinciple.category}
                                    </Badge>
                                </div>
                                <DialogTitle className="text-2xl font-bold">{selectedPrinciple.concept}</DialogTitle>
                                <DialogDescription className="text-base mt-2">
                                    {selectedPrinciple.definition}
                                </DialogDescription>
                            </DialogHeader>

                            <div className="space-y-6 mt-4">
                                {selectedPrinciple.image && (
                                    <div className="rounded-xl overflow-hidden border border-border">
                                        <DocImage src={selectedPrinciple.image} alt={selectedPrinciple.concept} />
                                    </div>
                                )}

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {selectedPrinciple.actionable_advice && (
                                        <div className="bg-muted/50 p-4 rounded-xl space-y-3">
                                            <h4 className="font-semibold flex items-center gap-2 text-primary">
                                                <Lightbulb className="h-4 w-4" />
                                                Actionable Advice
                                            </h4>
                                            <ul className="text-sm space-y-2 list-disc list-inside text-muted-foreground">
                                                {selectedPrinciple.actionable_advice.map((advice, i) => (
                                                    <li key={i}>{advice}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    <div className="space-y-6">
                                        {selectedPrinciple.visual_triggers && (
                                            <div className="space-y-2">
                                                <h4 className="font-semibold flex items-center gap-2 text-sm">
                                                    <Eye className="h-4 w-4" />
                                                    Visual Triggers
                                                </h4>
                                                <div className="flex flex-wrap gap-2">
                                                    {selectedPrinciple.visual_triggers.map((trigger, i) => (
                                                        <Badge key={i} variant="secondary" className="text-xs">
                                                            {trigger}
                                                        </Badge>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        {selectedPrinciple.expected_impact && (
                                            <div className="space-y-2">
                                                <h4 className="font-semibold flex items-center gap-2 text-sm">
                                                    <Target className="h-4 w-4" />
                                                    Expected Impact
                                                </h4>
                                                <p className="text-sm text-muted-foreground font-medium">
                                                    {selectedPrinciple.expected_impact}
                                                </p>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {selectedPrinciple.case_study && (
                                    <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-800">
                                        <h4 className="font-semibold flex items-center gap-2 text-blue-700 dark:text-blue-400 mb-2">
                                            <BookOpen className="h-4 w-4" />
                                            Case Study
                                        </h4>
                                        <p className="text-sm text-blue-900 dark:text-blue-100 italic">
                                            "{selectedPrinciple.case_study}"
                                        </p>
                                    </div>
                                )}
                            </div>
                        </>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
