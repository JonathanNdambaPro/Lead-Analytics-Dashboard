"use client"

import * as React from "react"
import { getMonthlyEventCounts, type MonthlyEventCount } from "@/lib/api"

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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface ObjectiveRow {
  label: string;
  key: keyof MonthlyEventCount;
  objectif: number;
}

const objectives: ObjectiveRow[] = [
  {
    label: "Messages envoyés",
    key: "date_prise_contact",
    objectif: 400,
  },
  {
    label: "Conversations",
    key: "date_reponse_prospect",
    objectif: 200,
  },
  {
    label: "Appels proposés",
    key: "date_appel_propose",
    objectif: 100,
  },
  {
    label: "Appels bookés",
    key: "date_appel_booke",
    objectif: 24,
  },
]

export function MonthlyObjectivesTable() {
  const [data, setData] = React.useState<MonthlyEventCount[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)
  const [selectedPeriod, setSelectedPeriod] = React.useState<string>("")

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const result = await getMonthlyEventCounts()
        setData(result)
        setError(null)

        // Sélectionner automatiquement le dernier mois disponible
        if (result.length > 0) {
          setSelectedPeriod(result[result.length - 1].mois)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data')
        console.error('Error fetching monthly event counts:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Trouver les données du mois sélectionné
  const currentMonthData = data.find(item => item.mois === selectedPeriod) || null

  // Créer la liste des périodes disponibles
  const availablePeriods = data.map(item => {
    const date = new Date(item.mois)
    return {
      value: item.mois,
      label: date.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
    }
  })

  const getTotal = (key: keyof MonthlyEventCount): number => {
    if (!currentMonthData || key === 'mois') return 0
    return currentMonthData[key] ?? 0
  }

  const getProgressColor = (total: number, objectif: number): string => {
    const percentage = (total / objectif) * 100
    if (percentage >= 100) return "text-green-600 dark:text-green-400"
    if (percentage >= 75) return "text-blue-600 dark:text-blue-400"
    if (percentage >= 50) return "text-yellow-600 dark:text-yellow-400"
    return "text-red-600 dark:text-red-400"
  }

  const getRowBackground = (total: number, objectif: number): string => {
    const percentage = (total / objectif) * 100
    if (percentage >= 100) return "bg-green-500/10"
    if (percentage < 50) return "bg-red-500/10"
    return ""
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Objectifs Mensuels</CardTitle>
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
          <CardTitle>Objectifs Mensuels</CardTitle>
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
      <CardHeader className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between space-y-0">
        <div className="flex flex-col gap-1">
          <CardTitle>Objectifs Mensuels</CardTitle>
          <CardDescription>
            Suivi des objectifs par mois
          </CardDescription>
        </div>
        <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Sélectionner un mois" />
          </SelectTrigger>
          <SelectContent>
            {availablePeriods.map((period) => (
              <SelectItem key={period.value} value={period.value}>
                {period.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[250px]">Métrique</TableHead>
              <TableHead className="text-right">Totaux</TableHead>
              <TableHead className="text-right">Objectif</TableHead>
              <TableHead className="text-right">Progression</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {objectives.map((objective) => {
              const total = getTotal(objective.key)
              const percentage = Math.round((total / objective.objectif) * 100)
              return (
                <TableRow
                  key={objective.key}
                  className={getRowBackground(total, objective.objectif)}
                >
                  <TableCell className="font-medium">{objective.label}</TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(total, objective.objectif)}`}>
                    {total}
                  </TableCell>
                  <TableCell className="text-right text-muted-foreground">
                    {objective.objectif}
                  </TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(total, objective.objectif)}`}>
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
