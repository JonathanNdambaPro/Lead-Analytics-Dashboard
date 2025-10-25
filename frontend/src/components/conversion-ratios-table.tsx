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

interface ConversionRow {
  label: string;
  ratioScalezia: number;
  calculate: (data: MonthlyEventCount) => number;
}

const conversions: ConversionRow[] = [
  {
    label: "Messages Envoyés → Conversations",
    ratioScalezia: 70,
    calculate: (data) => {
      const messages = data.date_prise_contact ?? 0
      const conversations = data.date_reponse_prospect ?? 0
      if (messages === 0) return 0
      return Math.round((conversations / messages) * 100)
    },
  },
  {
    label: "Conversations → Appel proposé",
    ratioScalezia: 50,
    calculate: (data) => {
      const conversations = data.date_reponse_prospect ?? 0
      const appelsPropose = data.date_appel_propose ?? 0
      if (conversations === 0) return 0
      return Math.round((appelsPropose / conversations) * 100)
    },
  },
  {
    label: "Appel proposé → Appel booké",
    ratioScalezia: 70,
    calculate: (data) => {
      const appelsPropose = data.date_appel_propose ?? 0
      const appelsBooke = data.date_appel_booke ?? 0
      if (appelsPropose === 0) return 0
      return Math.round((appelsBooke / appelsPropose) * 100)
    },
  },
  {
    label: "Conversations → Appel booké",
    ratioScalezia: 30,
    calculate: (data) => {
      const conversations = data.date_reponse_prospect ?? 0
      const appelsBooke = data.date_appel_booke ?? 0
      if (conversations === 0) return 0
      return Math.round((appelsBooke / conversations) * 100)
    },
  },
]

export function ConversionRatiosTable() {
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
  const currentMonthData = data.find(item => item.mois === selectedPeriod)

  // Créer la liste des périodes disponibles
  const availablePeriods = data.map(item => {
    const date = new Date(item.mois)
    return {
      value: item.mois,
      label: date.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
    }
  })

  const getProgressColor = (yourRatio: number, scalezia: number): string => {
    const difference = yourRatio - scalezia
    if (difference >= 0) return "text-green-600 dark:text-green-400"
    if (difference >= -10) return "text-yellow-600 dark:text-yellow-400"
    return "text-red-600 dark:text-red-400"
  }

  const getRowBackground = (yourRatio: number, scalezia: number): string => {
    const difference = yourRatio - scalezia
    if (difference >= 0) return "bg-green-500/10"
    if (difference < -10) return "bg-red-500/10"
    return ""
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Ratios de Conversion</CardTitle>
          <CardDescription>Loading data...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex h-[200px] items-center justify-center">
            <p className="text-muted-foreground">Loading ratios...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Ratios de Conversion</CardTitle>
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
          <CardTitle>Ratios de Conversion</CardTitle>
          <CardDescription>
            Comparaison de tes ratios avec les objectifs Souhaité
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
              <TableHead className="w-[300px]">Conversions</TableHead>
              <TableHead className="text-right">Ratio Souhaité</TableHead>
              <TableHead className="text-right">Ton Ratio</TableHead>
              <TableHead className="text-right">Différence</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {conversions.map((conversion, index) => {
              const yourRatio = currentMonthData ? conversion.calculate(currentMonthData) : 0
              const difference = yourRatio - conversion.ratioScalezia
              const differenceSign = difference >= 0 ? "+" : ""

              return (
                <TableRow
                  key={index}
                  className={getRowBackground(yourRatio, conversion.ratioScalezia)}
                >
                  <TableCell className="font-medium">{conversion.label}</TableCell>
                  <TableCell className="text-right text-muted-foreground">
                    {conversion.ratioScalezia}%
                  </TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(yourRatio, conversion.ratioScalezia)}`}>
                    {yourRatio}%
                  </TableCell>
                  <TableCell className={`text-right font-semibold ${getProgressColor(yourRatio, conversion.ratioScalezia)}`}>
                    {differenceSign}{difference}%
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
