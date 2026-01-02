import PricingCard from './PricingCard';
import { getStepPayProductCode, getStepPayProducts } from '@/lib/payments/steppay/steppay';
import { Button } from "@saas/ui";
import { Check } from "lucide-react";

export const revalidate = 3600;

export default async function PricingPage({ params }: { params: Promise<{ lng: string }> }) {
  const { lng } = await params;

  // Fetch StepPay products
  const productCode = await getStepPayProductCode();
  const stepPayProducts = await getStepPayProducts(productCode);
  const productPrices = stepPayProducts.prices;

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-foreground sm:text-5xl mb-6">
          Simple, Transparent Pricing
        </h1>
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
    </main>
  );
}