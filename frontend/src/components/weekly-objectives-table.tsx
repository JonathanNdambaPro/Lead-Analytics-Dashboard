"use client"

import * as React from "react"
import { getWeeklyEventCounts, type WeeklyEventCount } from "@/lib/api"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

interface ObjectiveRow {
  label: string;
  key: keyof WeeklyEventCount;
  objectif: number;
}

const objectives: ObjectiveRow[] = [
  {
    label: "Messages envoyés",
    key: "date_prise_contact",
    objectif: 50,
  },
  {
    label: "Conversations",
    key: "date_reponse_prospect",
    objectif: 25,
  },
  {
    label: "Appels proposés",
    key: "date_appel_propose",
    objectif: 17,
  },
  {
    label: "Appels bookés",
    key: "date_appel_booke",
    objectif: 3,
  },
]

export function WeeklyObjectivesTable() {
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

  // Calculer la moyenne pour chaque métrique
  const getAverage = (key: keyof WeeklyEventCount): number => {
    if (data.length === 0 || key === 'semaine') return 0

    const sum = data.reduce((acc, week) => {
      const value = week[key] ?? 0
      return acc + value
    }, 0)

    return Math.round(sum / data.length)
  }

  const getProgressColor = (average: number, objectif: number): string => {
    const percentage = (average / objectif) * 100
    if (percentage >= 100) return "text-green-600 dark:text-green-400"
    if (percentage >= 75) return "text-blue-600 dark:text-blue-400"
    if (percentage >= 50) return "text-yellow-600 dark:text-yellow-400"
    return "text-red-600 dark:text-red-400"
  }

  const getRowBackground = (average: number, objectif: number): string => {
    const percentage = (average / objectif) * 100
    if (percentage >= 100) return "bg-green-500/10"
    if (percentage < 50) return "bg-red-500/10"
    return ""
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Objectifs Hebdomadaires</CardTitle>
          <CardDescription>Loading data...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex h-[200px] items-center justify-center">
            <p className="text-muted-foreground">Loading objectives...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Objectifs Hebdomadaires</CardTitle>
          <CardDescription>Error loading data</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex h-[200px] items-center justify-center">
            <p className="text-destructive">{error}</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col gap-1">
          <CardTitle>Objectifs Hebdomadaires</CardTitle>
          <CardDescription>
            Moyenne hebdomadaire sur {data.length} semaine{data.length > 1 ? 's' : ''}
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[250px]">Métrique</TableHead>
              <TableHead className="text-right">Moyenne Hebdo</TableHead>
              <TableHead className="text-right">Objectif Hebdomadaire</TableHead>
              <TableHead className="text-right">Progression</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {objectives.map((objective) => {
              const average = getAverage(objective.key)
              const percentage = Math.round((average / objective.objectif) * 100)
              return (
                <TableRow
                  key={objective.key}
                  className={getRowBackground(average, objective.objectif)}
                >
                  <TableCell className="font-medium">{objective.label}</TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(average, objective.objectif)}`}>
                    {average}
                  </TableCell>
                  <TableCell className="text-right text-muted-foreground">
                    {objective.objectif}
                  </TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(average, objective.objectif)}`}>
                    {percentage}%
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
