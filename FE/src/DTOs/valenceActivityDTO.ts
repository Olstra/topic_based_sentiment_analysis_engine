export type ValenceActivityDTO = {
  patient_id: number;
  topic: string;
  sentiment: string;
  nr_of_occurrences: number;
  id: number;
}

export type AvgValenceActivityDTO = {
  patient_id: number;
  topic: string;
  overall_sentiment: string;
  nr_of_occurrences: number;
}

export type ValenceDataPointDTO = {
  sentiment_score: number;
  date: Date;
}

export type ValenceChartDataDTO = {
  patient_id: number;
  topic: string;
  data: ValenceDataPointDTO[];
}
