import { Lightbulb, Eye, CheckCircle, ExternalLink } from "lucide-react";

export default function SciencePage() {
    return (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div className="text-center mb-16">
                <div className="inline-block bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-5 py-2 rounded-full text-sm font-semibold uppercase tracking-wider mb-6">
                    Science
                </div>
                <h1 className="text-4xl font-bold text-foreground sm:text-5xl mb-6">
                    Science Behind Our Predictions
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Combining cognitive science, deep learning, and rigorous validation
                </p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
                {/* Cognitive Ergonomics */}
                <div className="bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all flex flex-col">
                    <div className="text-center mb-6">
                        <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
                            <Lightbulb className="h-12 w-12 text-white" />
                        </div>
                    </div>
                    <h3 className="text-2xl font-bold text-center mb-4 text-foreground">Cognitive Ergonomics</h3>
                    <p className="text-muted-foreground text-center mb-6 text-lg">
                        Study how perception, memory, and decision-making interact with interfaces to reduce cognitive load and prevent errors.
                    </p>
                    <div className="bg-muted/50 rounded-xl p-6 mb-6 flex-1">
                        <div className="flex items-start">
                            <CheckCircle className="h-6 w-6 text-green-500 mr-3 mt-1 flex-shrink-0" />
                            <div>
                                <h4 className="font-semibold text-foreground mb-2">Key Benefits</h4>
                                <ul className="space-y-2 text-muted-foreground">
                                    <li>Reveals hidden cognitive friction</li>
                                    <li>Supports safer, intuitive workflows</li>
                                    <li>Aligns UX with human limits</li>
                                    <li>Identifies decision bottlenecks</li>
                                    <li>Reduces user errors</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div className="text-center space-x-4">
                        <a href="https://iea.cc/about/what-is-ergonomics/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-semibold">
                            IEA Guide <ExternalLink className="ml-1 h-4 w-4" />
                        </a>
                        <a href="https://oshwiki.osha.europa.eu/en/themes/cognitive-ergonomics" target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-semibold">
                            OSHwiki <ExternalLink className="ml-1 h-4 w-4" />
                        </a>
                    </div>
                </div>

                {/* Deep Saliency Models */}
                <div className="bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all flex flex-col">
                    <div className="text-center mb-6">
                        <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
                            <Eye className="h-12 w-12 text-white" />
                        </div>
                    </div>
                    <h3 className="text-2xl font-bold text-center mb-4 text-foreground">Deep Saliency Models</h3>
                    <p className="text-muted-foreground text-center mb-6 text-lg">
                        Deep neural networks trained on eye-tracking datasets predict where users look first, generating pixel-level attention heatmaps.
                    </p>
                    <div className="bg-muted/50 rounded-xl p-6 mb-6 flex-1">
                        <div className="flex items-start">
                            <CheckCircle className="h-6 w-6 text-green-500 mr-3 mt-1 flex-shrink-0" />
                            <div>
                                <h4 className="font-semibold text-foreground mb-2">Key Benefits</h4>
                                <ul className="space-y-2 text-muted-foreground">
                                    <li>Scales to thousands of screens</li>
                                    <li>Instant feedback</li>
                                    <li>Pixel-level predictions</li>
                                    <li>Works across design styles</li>
                                    <li>State-of-the-art deep learning</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div className="text-center space-x-4">
                        <a href="https://arxiv.org/abs/1610.01563" target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-semibold">
                            DeepGaze II <ExternalLink className="ml-1 h-4 w-4" />
                        </a>
                        <a href="https://arxiv.org/abs/2010.12913" target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-semibold">
                            Review <ExternalLink className="ml-1 h-4 w-4" />
                        </a>
                    </div>
                </div>

                {/* Validation */}
                <div className="bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all flex flex-col">
                    <div className="text-center mb-6">
                        <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
                            <CheckCircle className="h-12 w-12 text-white" />
                        </div>
                    </div>
                    <h3 className="text-2xl font-bold text-center mb-4 text-foreground">Validation</h3>
                    <p className="text-muted-foreground text-center mb-6 text-lg">
                        Our predictions achieve <strong className="text-indigo-600">90%+ similarity</strong> to real eye-tracking using standard saliency metrics.
                    </p>
                    <div className="bg-muted/50 rounded-xl p-6 mb-6 flex-1">
                        <div className="flex items-start">
                            <CheckCircle className="h-6 w-6 text-green-500 mr-3 mt-1 flex-shrink-0" />
                            <div>
                                <h4 className="font-semibold text-foreground mb-2">Key Benefits</h4>
                                <ul className="space-y-2 text-muted-foreground">
                                    <li>Quantitative evidence</li>
                                    <li>Builds trust with teams</li>
                                    <li>Validated against benchmarks</li>
                                    <li>Continuously improved</li>
                                    <li>Industry-standard metrics</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div className="text-center space-x-4">
                        <a href="https://saliency.tuebingen.ai/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-semibold">
                            MIT/Tübingen Benchmark <ExternalLink className="ml-1 h-4 w-4" />
                        </a>
                    </div>
                </div>
            </div>
        </main>
    );
}
