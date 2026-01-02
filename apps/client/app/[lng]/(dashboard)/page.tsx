import { Button } from "@saas/ui";
import { ArrowRight, Check, Lightbulb, Eye, CheckCircle, ExternalLink } from "lucide-react";
import PricingCard from './pricing/PricingCard';
import { getStepPayProductCode, getStepPayProducts } from '@/lib/payments/steppay/steppay';

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
    <main>
      {/* Hero Section */}
      <section className="relative py-20 bg-gray-900 overflow-hidden">
        <div className="absolute inset-0 bg-black/60 z-10" />
        <div
          className="absolute inset-0 bg-cover bg-center z-0"
          style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=80")' }}
        />
        <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold text-white tracking-tight sm:text-5xl md:text-6xl mb-6">
            Uvolution AI
          </h1>
          <p className="text-xl text-gray-300 mb-4 font-medium">
            Predict User Attention with 96% Accuracy
          </p>
          <p className="text-sm text-gray-400 mb-8">
            Powered by DeepGaze IIE & MIT1003 Dataset
          </p>
          <div className="flex justify-center gap-4">
            <Button asChild className="bg-orange-500 hover:bg-orange-600 text-white rounded-full text-lg px-8 py-6">
              <a href={`/${lng}/admin`}>
                Try It Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-background w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-foreground sm:text-4xl mb-4">
              Comprehensive Analysis Reports
            </h2>
            <p className="text-xl text-muted-foreground">
              Get actionable insights backed by cognitive science and A/B testing research
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card rounded-xl border shadow-sm p-6">
              <div className="aspect-video relative mb-6 bg-muted rounded-md overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                  Heatmap Image
                </div>
              </div>
              <h3 className="text-2xl font-semibold mb-3 text-foreground">Predictive Heatmaps</h3>
              <p className="text-muted-foreground">
                See exactly where users will look first. Optimize your layout for maximum attention.
              </p>
            </div>

            <div className="bg-card rounded-xl border shadow-sm p-6">
              <div className="aspect-video relative mb-6 bg-muted rounded-md overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                  Color Psychology
                </div>
              </div>
              <h3 className="text-2xl font-semibold mb-3 text-foreground">Color Psychology</h3>
              <p className="text-muted-foreground">
                Get CTA color recommendations proven to increase conversions by up to 34%.
              </p>
            </div>

            <div className="bg-card rounded-xl border shadow-sm p-6">
              <div className="aspect-video relative mb-6 bg-muted rounded-md overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center text-muted-foreground">
                  UX Recommendations
                </div>
              </div>
              <h3 className="text-2xl font-semibold mb-3 text-foreground">UX Recommendations</h3>
              <p className="text-muted-foreground">
                Whitespace analysis, visual hierarchy, CTA placement, mobile-friendliness, and more.
              </p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <Button asChild size="lg" className="text-lg px-8 py-6 rounded-full">
              <a href={`/${lng}/admin`}>Try It Now - Free</a>
            </Button>
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
        </div>
      </section>

      {/* Pricing Section */}
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

          <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-8">
            {/* Dynamic StepPay Plans */}
            {productPrices.map((price) => (
              <div key={price.code} className="bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all flex flex-col">
                <PricingCard
                  product={stepPayProducts}
                  price={price}
                  lng={lng}
                />
              </div>
            ))}

            {/* Static Enterprise Plan */}
            <div className="bg-card rounded-2xl border p-8 shadow-sm hover:shadow-lg transition-all flex flex-col">
              <div className="pt-6">
                <h2 className="text-2xl font-medium text-foreground mb-2">
                  Enterprise
                </h2>
                <p className="text-4xl font-medium text-foreground mb-6">
                  Custom
                </p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Everything in Premium</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Custom integrations</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">Dedicated support</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">SLA guarantee</span>
                  </li>
                </ul>
                <Button variant="outline" className="w-full" asChild>
                  <a href="mailto:support@uvolution.ai">Contact Us</a>
                </Button>
              </div>
            </div>
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
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <p className="text-lg italic text-muted-foreground mb-4">"Incredible accuracy. It changed how we approach UI design."</p>
              <p className="font-semibold text-foreground">- Smashing Magazine</p>
            </div>
            <div className="p-6">
              <p className="text-lg italic text-muted-foreground mb-4">"A must-have tool for any UX researcher."</p>
              <p className="font-semibold text-foreground">- Codrops</p>
            </div>
            <div className="p-6">
              <p className="text-lg italic text-muted-foreground mb-4">"Saved us weeks of testing time."</p>
              <p className="font-semibold text-foreground">- Awwwards</p>
            </div>
          </div>
          <div className="mt-12 flex justify-center">
            <Button asChild className="bg-orange-500 hover:bg-orange-600 text-white rounded-full text-xl px-12 py-6">
              <a href={`/${lng}/admin`}>
                Start Analyzing Now
                <ArrowRight className="ml-3 h-6 w-6" />
              </a>
            </Button>
          </div>
        </div>
      </section>
    </main>
  );
}
