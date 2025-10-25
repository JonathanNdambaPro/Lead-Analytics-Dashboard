import { LeadsAnalyticsChart } from "@/components/leads-analytics-chart";

export default function Home() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold">Leads Analytics Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Vue d'ensemble des événements hebdomadaires pour tous les leads
        </p>
      </div>

      <LeadsAnalyticsChart />
    </div>
  );
}
