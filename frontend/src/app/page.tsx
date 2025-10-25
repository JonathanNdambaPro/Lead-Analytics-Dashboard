import { LeadsAnalyticsChart } from "@/components/leads-analytics-chart";
import { MonthlyObjectivesTable } from "@/components/monthly-objectives-table";

export default function Home() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold">Leads Analytics Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Vue d'ensemble des événements et objectifs mensuels
        </p>
      </div>

      <LeadsAnalyticsChart />

      <MonthlyObjectivesTable />
    </div>
  );
}
