"use client"

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"
import { getWeeklyEventCounts, type WeeklyEventCount } from "@/lib/api"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart"

const chartConfig = {
  date_prise_contact: {
    label: "Prise de contact",
    color: "var(--chart-1)",
  },
  date_reponse_prospect: {
    label: "Réponse prospect",
    color: "var(--chart-2)",
  },
  date_appel_booke: {
    label: "Appel booké",
    color: "var(--chart-3)",
  },
  date_appel_propose: {
    label: "Appel proposé",
    color: "var(--chart-4)",
  },
  date_relance: {
    label: "Relance",
    color: "var(--chart-5)",
  },
} satisfies ChartConfig

export function LeadsAnalyticsChart() {
  const [data, setData] = React.useState<WeeklyEventCount[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const result = await getWeeklyEventCounts()
        setData(result)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data')
        console.error('Error fetching weekly event counts:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <Card className="pt-0">
        <CardHeader className="border-b py-5">
          <CardTitle>Leads Analytics</CardTitle>
          <CardDescription>Loading data...</CardDescription>
        </CardHeader>
        <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
          <div className="flex h-[250px] items-center justify-center">
            <p className="text-muted-foreground">Loading chart data...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="pt-0">
        <CardHeader className="border-b py-5">
          <CardTitle>Leads Analytics</CardTitle>
          <CardDescription>Error loading data</CardDescription>
        </CardHeader>
        <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
          <div className="flex h-[250px] items-center justify-center">
            <p className="text-destructive">{error}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="pt-0">
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
        <div className="grid flex-1 gap-1">
          <CardTitle>Leads Analytics - Weekly Events</CardTitle>
          <CardDescription>
            Nombre d'événements par semaine pour tous les leads
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[400px] w-full"
        >
          <AreaChart data={data}>
            <defs>
              <linearGradient id="fillPriseContact" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-date_prise_contact)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-date_prise_contact)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillReponseProspect" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-date_reponse_prospect)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-date_reponse_prospect)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillAppelBooke" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-date_appel_booke)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-date_appel_booke)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillAppelPropose" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-date_appel_propose)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-date_appel_propose)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillRelance" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-date_relance)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-date_relance)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="semaine"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value: string) => {
                const date = new Date(value)
                return date.toLocaleDateString("fr-FR", {
                  month: "short",
                  day: "numeric",
                })
              }}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(value: string) => {
                    return new Date(value).toLocaleDateString("fr-FR", {
                      month: "long",
                      day: "numeric",
                      year: "numeric",
                    })
                  }}
                  indicator="dot"
                />
              }
            />
            <Area
              dataKey="date_prise_contact"
              type="natural"
              fill="url(#fillPriseContact)"
              stroke="var(--color-date_prise_contact)"
              stackId="a"
            />
            <Area
              dataKey="date_reponse_prospect"
              type="natural"
              fill="url(#fillReponseProspect)"
              stroke="var(--color-date_reponse_prospect)"
              stackId="a"
            />
            <Area
              dataKey="date_appel_booke"
              type="natural"
              fill="url(#fillAppelBooke)"
              stroke="var(--color-date_appel_booke)"
              stackId="a"
            />
            <Area
              dataKey="date_appel_propose"
              type="natural"
              fill="url(#fillAppelPropose)"
              stroke="var(--color-date_appel_propose)"
              stackId="a"
            />
            <Area
              dataKey="date_relance"
              type="natural"
              fill="url(#fillRelance)"
              stroke="var(--color-date_relance)"
              stackId="a"
            />
            <ChartLegend content={<ChartLegendContent />} />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
