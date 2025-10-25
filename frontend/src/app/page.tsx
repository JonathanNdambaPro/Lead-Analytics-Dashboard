import { LeadsAnalyticsChart } from "@/components/leads-analytics-chart";
import { MonthlyObjectivesTable } from "@/components/monthly-objectives-table";
import { WeeklyObjectivesTable } from "@/components/weekly-objectives-table";

export default function Home() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold">Leads Analytics Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Vue d'ensemble des événements et objectifs mensuels et hebdomadaires
        </p>
      </div>

      <LeadsAnalyticsChart />

      <div className="grid gap-6 lg:grid-cols-2">
        <MonthlyObjectivesTable />
        <WeeklyObjectivesTable />
      </div>
    </div>
  );
}
