import { Button } from "@saas/ui";
import { ArrowRight, Check, Lightbulb, Eye, CheckCircle, ExternalLink, Sparkles, Star, Upload, BarChart3, Zap, Play } from "lucide-react";
import PricingCard from './pricing/PricingCard';
import { getStepPayProductCode, getStepPayProducts } from '@/lib/payments/steppay/steppay';
import { createCheckoutAction } from '@/lib/payments/actions';

export const revalidate = 3600;

export default async function HomePage({
  params,
}: {
  params: Promise<{ lng: string }>;
}) {
  const { lng } = await params;

  // Fetch StepPay products
  const productCode = await getStepPayProductCode();
  const stepPayProducts = await getStepPayProducts(productCode);
  const productPrices = stepPayProducts.prices;

  return (
    <main className="overflow-x-hidden">
      {/* Hero Section - Redesigned */}
      <section className="relative py-20 md:py-32 bg-gray-900 overflow-hidden">
        {/* Ambient Background Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-[1000px] pointer-events-none opacity-20 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-orange-500 via-transparent to-transparent z-0" />
        <div className="absolute inset-0 bg-black/40 z-10" />
        <div
          className="absolute inset-0 bg-cover bg-center z-0 opacity-30"
          style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=80")' }}
        />

        <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Text */}
            <div className="flex flex-col gap-6 text-left">
              {/* Version Badge */}
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur border border-white/10 w-fit">
                <span className="size-2 rounded-full bg-orange-400 animate-pulse" />
                <span className="text-xs font-medium text-orange-300 uppercase tracking-wider">Powered by DeepGaze IIE</span>
              </div>

              <h1 className="text-4xl md:text-5xl lg:text-6xl font-black leading-[1.1] tracking-tight text-white">
                Unlock the Power of{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-orange-200">
                  Human Attention.
                </span>
              </h1>

              <p className="text-lg text-gray-300 max-w-lg leading-relaxed">
                Predict user attention with <strong className="text-orange-400">96% accuracy</strong>. Precision eye-tracking analytics for next-gen UX optimization powered by MIT1003 Dataset.
              </p>

              <div className="flex flex-wrap gap-4 pt-4">
                <Button asChild className="h-12 px-8 bg-orange-500 hover:bg-orange-600 text-white rounded-lg text-base font-bold transition-all duration-300 hover:shadow-[0_0_20px_-5px_rgba(249,115,22,0.5)] hover:-translate-y-0.5">
                  <a href={`/${lng}/admin`}>
                    Try It Now
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </a>
                </Button>
                <Button variant="outline" asChild className="h-12 px-8 rounded-lg border-gray-600 hover:border-white bg-transparent text-white font-bold transition-all duration-300 hover:bg-white/5">
                  <a href="#features">
                    <Play className="mr-2 h-4 w-4" />
                    View Demo
                  </a>
                </Button>
              </div>

              {/* Trust Indicators */}
              <div className="flex items-center gap-4 mt-8 text-sm text-gray-400">
                <div className="flex -space-x-2">
                  <div className="size-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 border-2 border-gray-900 flex items-center justify-center">
                    <Star className="h-4 w-4 text-white" />
                  </div>
                  <div className="size-8 rounded-full bg-gradient-to-br from-orange-500 to-red-500 border-2 border-gray-900 flex items-center justify-center">
                    <Zap className="h-4 w-4 text-white" />
                  </div>
                  <div className="size-8 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 border-2 border-gray-900 flex items-center justify-center">
                    <CheckCircle className="h-4 w-4 text-white" />
                  </div>
                </div>
                <p>Trusted by designers worldwide</p>
              </div>
            </div>

            {/* Right Column - Visual */}
            <div className="relative group hidden lg:block">
              <div className="absolute -inset-1 bg-gradient-to-r from-orange-500 to-purple-600 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200" />
              <div className="relative w-full aspect-[4/3] rounded-xl overflow-hidden border border-white/20 bg-gray-800/80 backdrop-blur shadow-2xl">
                <div
                  className="w-full h-full bg-cover bg-center"
                  style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80")' }}
                >
                  <div className="absolute inset-0 bg-gradient-to-t from-gray-900/80 via-transparent to-transparent" />

                  {/* Overlay UI Elements */}
                  <div className="absolute top-4 right-4 bg-gray-900/90 backdrop-blur border border-white/10 p-3 rounded-lg shadow-lg max-w-[160px]">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-gray-400">Attention Score</span>
                      <span className="text-xs text-orange-400 font-bold">96%</span>
                    </div>
                    <div className="w-full h-1.5 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-orange-500 to-orange-400 w-[96%]" />
                    </div>
                  </div>

                  <div className="absolute bottom-6 left-6 flex gap-2">
                    <span className="px-3 py-1 bg-orange-500/20 backdrop-blur border border-orange-500/30 text-orange-400 text-xs font-bold rounded-md">AI Analysis</span>
                    <span className="px-3 py-1 bg-black/40 backdrop-blur border border-white/10 text-white text-xs font-medium rounded-md">Real-time</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-background w-full relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-block bg-gradient-to-r from-orange-500 to-orange-600 text-white px-5 py-2 rounded-full text-sm font-semibold uppercase tracking-wider mb-6">
              How It Works
            </div>
            <h2 className="text-3xl md:text-4xl font-black text-foreground mb-4">
              Three Simple Steps
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Start optimizing your user experience with precision analytics.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            {/* Connecting line for desktop */}
            <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-[2px] bg-gradient-to-r from-transparent via-border to-transparent z-0" />

            {/* Step 1 */}
            <div className="relative z-10 flex flex-col items-center text-center gap-4 group">
              <div className="w-24 h-24 rounded-2xl bg-card border shadow-lg flex items-center justify-center group-hover:border-orange-500/50 group-hover:shadow-[0_0_20px_-5px_rgba(249,115,22,0.3)] transition-all duration-300">
                <Upload className="h-10 w-10 text-orange-500" />
              </div>
              <div className="bg-background px-2">
                <h3 className="text-xl font-bold mb-2 text-foreground">1. Input Your Design</h3>
                <p className="text-muted-foreground text-sm leading-relaxed px-4">Upload your design screenshot or simply enter a URL to start the analysis process.</p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative z-10 flex flex-col items-center text-center gap-4 group">
              <div className="w-24 h-24 rounded-2xl bg-card border shadow-lg flex items-center justify-center group-hover:border-orange-500/50 group-hover:shadow-[0_0_20px_-5px_rgba(249,115,22,0.3)] transition-all duration-300">
                <Eye className="h-10 w-10 text-orange-500" />
              </div>
              <div className="bg-background px-2">
                <h3 className="text-xl font-bold mb-2 text-foreground">2. AI Prediction</h3>
                <p className="text-muted-foreground text-sm leading-relaxed px-4">Our advanced Uvolution AI predicts user attention patterns and generates heatmaps.</p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative z-10 flex flex-col items-center text-center gap-4 group">
              <div className="w-24 h-24 rounded-2xl bg-card border shadow-lg flex items-center justify-center group-hover:border-orange-500/50 group-hover:shadow-[0_0_20px_-5px_rgba(249,115,22,0.3)] transition-all duration-300">
                <BarChart3 className="h-10 w-10 text-orange-500" />
              </div>
              <div className="bg-background px-2">
                <h3 className="text-xl font-bold mb-2 text-foreground">3. Actionable Insights</h3>
                <p className="text-muted-foreground text-sm leading-relaxed px-4">Get comprehensive marketing consulting and AI design generation to optimize your UX.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Redesigned */}
      <section id="features" className="py-20 bg-gradient-to-b from-muted/30 to-background w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
            <div className="max-w-xl">
              <h2 className="text-3xl md:text-4xl font-black text-foreground mb-4">
                Comprehensive Analysis Reports
              </h2>
              <p className="text-lg text-muted-foreground">
                Get actionable insights backed by cognitive science and A/B testing research.
              </p>
            </div>
            <Button variant="ghost" asChild className="text-orange-500 font-bold hover:text-orange-400 group">
              <a href={`/${lng}/admin`}>
                See all features
                <ArrowRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </a>
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Feature Card 1 */}
            <div className="group relative flex flex-col bg-card rounded-2xl border overflow-hidden hover:border-orange-500/40 hover:-translate-y-1 transition-all duration-300 shadow-sm hover:shadow-xl">
              <div className="h-48 w-full bg-gradient-to-br from-orange-500/20 to-purple-500/20 relative flex items-center justify-center">
                <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors" />
                <Eye className="h-16 w-16 text-orange-500/60" />
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="size-10 rounded-lg bg-orange-500/10 flex items-center justify-center mb-4">
                  <Eye className="h-5 w-5 text-orange-500" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Predictive Heatmaps</h3>
                <p className="text-muted-foreground text-sm">
                  See exactly where users will look first. Optimize your layout for maximum attention.
                </p>
              </div>
            </div>

            {/* Feature Card 2 */}
            <div className="group relative flex flex-col bg-card rounded-2xl border overflow-hidden hover:border-orange-500/40 hover:-translate-y-1 transition-all duration-300 shadow-sm hover:shadow-xl">
              <div className="h-48 w-full bg-gradient-to-br from-purple-500/20 to-indigo-500/20 relative flex items-center justify-center">
                <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors" />
                <Sparkles className="h-16 w-16 text-purple-500/60" />
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="size-10 rounded-lg bg-purple-500/10 flex items-center justify-center mb-4">
                  <Sparkles className="h-5 w-5 text-purple-500" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Color Psychology</h3>
                <p className="text-muted-foreground text-sm">
                  Get CTA color recommendations proven to increase conversions by up to 34%.
                </p>
              </div>
            </div>

            {/* Feature Card 3 */}
            <div className="group relative flex flex-col bg-card rounded-2xl border overflow-hidden hover:border-orange-500/40 hover:-translate-y-1 transition-all duration-300 shadow-sm hover:shadow-xl">
              <div className="h-48 w-full bg-gradient-to-br from-emerald-500/20 to-teal-500/20 relative flex items-center justify-center">
                <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors" />
                <BarChart3 className="h-16 w-16 text-emerald-500/60" />
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="size-10 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4">
                  <BarChart3 className="h-5 w-5 text-emerald-500" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">UX Recommendations</h3>
                <p className="text-muted-foreground text-sm">
                  Whitespace analysis, visual hierarchy, CTA placement, mobile-friendliness, and more.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Science Section */}
      <section id="science" className="py-20 bg-gray-50 dark:bg-gray-900 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-block bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-5 py-2 rounded-full text-sm font-semibold uppercase tracking-wider mb-6">
              Science
            </div>
            <h2 className="text-4xl font-bold text-foreground sm:text-5xl mb-6">
              Science Behind Our Predictions
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Combining cognitive science, deep learning, and rigorous validation
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Cognitive Ergonomics */}
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col">
              <div className="text-center mb-6">
                <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-[0_0_20px_-5px_rgba(99,102,241,0.5)] transition-shadow duration-300">
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
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col">
              <div className="text-center mb-6">
                <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-[0_0_20px_-5px_rgba(99,102,241,0.5)] transition-shadow duration-300">
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
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col">
              <div className="text-center mb-6">
                <div className="w-20 h-20 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-[0_0_20px_-5px_rgba(99,102,241,0.5)] transition-shadow duration-300">
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
        </div>
      </section>

      {/* Pricing Section - Redesigned */}
      <section id="pricing" className="py-20 bg-background w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground sm:text-5xl mb-6">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Choose the plan that fits your needs
            </p>
          </div>

          <div className="grid lg:grid-cols-4 md:grid-cols-2 gap-6">
            {/* Free Plan */}
            <div className="flex flex-col bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="pt-6 flex flex-col flex-1">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  Free
                </h2>
                <p className="text-4xl font-bold text-foreground mb-2">
                  ₩0
                </p>
                <p className="text-sm text-muted-foreground mb-6">Forever free</p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">AI Eye-tracking Predictions</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Attention Heatmaps</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">UX Analysis Report</span>
                  </li>
                </ul>
                <Button variant="outline" className="w-full mt-auto" asChild>
                  <a href={`/${lng}/admin`}>Get Started</a>
                </Button>
              </div>
            </div>

            {/* Basic Plan - From StepPay */}
            {productPrices[0] && (
              <div className="flex flex-col bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="pt-6 flex flex-col flex-1">
                  <h2 className="text-2xl font-bold text-foreground mb-2">
                    Basic
                  </h2>
                  <p className="text-4xl font-bold text-foreground mb-2">
                    ₩{productPrices[0].currencyPrice?.KRW?.toLocaleString() || '8,900'}
                  </p>
                  <p className="text-sm text-muted-foreground mb-6">/month</p>
                  <ul className="space-y-3 mb-8">
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI Eye-tracking Predictions</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Attention Heatmaps</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">UX Analysis Report</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI-Powered Marketing Insights</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Information Architecture Analysis</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI Design Recommendations</span>
                    </li>
                    <li className="flex items-start text-muted-foreground">
                      <span className="ml-7 text-sm italic">30 analyses / month</span>
                    </li>
                  </ul>
                  <form action={createCheckoutAction} className="mt-auto">
                    <input type="hidden" name="productCode" value={stepPayProducts.code} />
                    <input type="hidden" name="priceCode" value={productPrices[0].code} />
                    <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white" type="submit">
                      Subscribe
                    </Button>
                  </form>
                </div>
              </div>
            )}

            {/* Pro Plan - From StepPay (Most Popular) */}
            {productPrices[1] && (
              <div className="relative flex flex-col bg-card rounded-2xl border-2 border-orange-500 p-8 shadow-[0_0_20px_-5px_rgba(249,115,22,0.3)] hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-orange-500 to-orange-600 text-white text-xs font-bold px-4 py-1 rounded-full uppercase tracking-wider">
                  Most Popular
                </div>
                <div className="pt-6 flex flex-col flex-1">
                  <h2 className="text-2xl font-bold text-foreground mb-2">
                    Pro
                  </h2>
                  <p className="text-4xl font-bold text-foreground mb-2">
                    ₩{productPrices[1].currencyPrice?.KRW?.toLocaleString() || '12,900'}
                  </p>
                  <p className="text-sm text-muted-foreground mb-6">/month</p>
                  <ul className="space-y-3 mb-8">
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI Eye-tracking Predictions</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Attention Heatmaps</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">UX Analysis Report</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI-Powered Marketing Insights</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Information Architecture Analysis</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">AI Design Recommendations</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground font-semibold">Unlimited Analyses</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Priority Processing</span>
                    </li>
                    <li className="flex items-start">
                      <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">Dedicated Email Support</span>
                    </li>
                  </ul>
                  <form action={createCheckoutAction} className="mt-auto">
                    <input type="hidden" name="productCode" value={stepPayProducts.code} />
                    <input type="hidden" name="priceCode" value={productPrices[1].code} />
                    <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white" type="submit">
                      Subscribe
                    </Button>
                  </form>
                </div>
              </div>
            )}

            {/* Enterprise Plan */}
            <div className="flex flex-col bg-card rounded-2xl border p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="pt-6 flex flex-col flex-1">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  Enterprise
                </h2>
                <p className="text-4xl font-bold text-foreground mb-2">
                  Custom
                </p>
                <p className="text-sm text-muted-foreground mb-6">Contact for pricing</p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Everything in Pro</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Custom Integrations</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Dedicated Support</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">SLA Guarantee</span>
                  </li>
                </ul>
                <Button variant="outline" className="w-full mt-auto" asChild>
                  <a href="mailto:support@uvolution.ai">Contact Us</a>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section - New */}
      <section className="w-full py-20 px-4">
        <div className="max-w-5xl mx-auto rounded-3xl bg-gradient-to-r from-orange-500/20 to-purple-500/20 border border-orange-500/30 p-10 md:p-20 text-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />

          <h2 className="relative z-10 text-3xl md:text-5xl font-black mb-6 text-foreground">
            Ready to optimize your UX?
          </h2>
          <p className="relative z-10 text-lg text-muted-foreground max-w-2xl mx-auto mb-10">
            Join thousands of product teams who are building better experiences with Uvolution AI today.
          </p>
          <div className="relative z-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button asChild className="h-12 px-8 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg shadow-xl hover:shadow-[0_0_20px_-5px_rgba(249,115,22,0.5)] transition-all duration-300">
              <a href={`/${lng}/admin`}>
                Start Analyzing Now
                <ArrowRight className="ml-3 h-5 w-5" />
              </a>
            </Button>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-16 bg-gray-50 dark:bg-gray-900 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground sm:text-4xl">
              Trusted by Designers
            </h2>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all duration-300">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-orange-400 text-orange-400" />
                ))}
              </div>
              <p className="text-lg italic text-muted-foreground mb-4">"Incredible accuracy. It changed how we approach UI design."</p>
              <p className="font-semibold text-foreground">- Smashing Magazine</p>
            </div>
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all duration-300">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-orange-400 text-orange-400" />
                ))}
              </div>
              <p className="text-lg italic text-muted-foreground mb-4">"A must-have tool for any UX researcher."</p>
              <p className="font-semibold text-foreground">- Codrops</p>
            </div>
            <div className="group bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all duration-300">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-orange-400 text-orange-400" />
                ))}
              </div>
              <p className="text-lg italic text-muted-foreground mb-4">"Saved us weeks of testing time."</p>
              <p className="font-semibold text-foreground">- Awwwards</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
