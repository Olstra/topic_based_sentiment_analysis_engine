<template>
    <h2>Motivations-Analyse</h2>
    <p>
        In diesem Graph wird gezeigt, wie motiviert der Patient ist und wie sich diese Motivation über die Zeit
        ändert.<br>
        Die Motivation des Patienten wird anhand folgender Punkte gemessen:
    </p>
    <div class="graph-div" v-for="(item, index) in col_names" :key="index">
        <input type="checkbox" :id="item" :value="item" v-model="checkedItems">
        <label :for="item">{{ item }}</label>
    </div>
    <GChart
        type="LineChart"
        :options="options"
        :data="chartData"
    />
</template>

<script lang="ts">
import {GChart} from "vue-google-charts";
import type {MoodScoresDTO} from "@/DTOs/moodScoresDTO";
import axiosInstance from "@/services/http/http-common";
import {GET_PATIENT_MOOD_SCORES} from "@/constants/http/api";
import {defineComponent} from "vue";
import {
    CHANCE_OF_SUCCESS,
    CONTROL,
    IMPORTANCE,
    MEANINGFULNESS,
    OVERALL_SCORE
} from "@/constants/analysis/MotivationAnalysis";

export default defineComponent({
    name: "MotivationAnalysis",
    components: {GChart},
    props: ['patientId'],
    data() {
        return {
            patientID: this.$props.patientId,
            col_names: [OVERALL_SCORE, IMPORTANCE, CHANCE_OF_SUCCESS, CONTROL, MEANINGFULNESS],
            moodScoresArray: [] as MoodScoresDTO[],
            chartData: [] as any,
            checkedItems: [OVERALL_SCORE, IMPORTANCE, CHANCE_OF_SUCCESS, CONTROL, MEANINGFULNESS],
            options: {
                title: "Motivation über Zeit",
                hAxis: {
                    title: "Zeitverlauf",
                },
                vAxis: {
                    title: "Motivations Score",
                    ticks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                },
                legend: {
                    position: "right",
                    textStyle: {
                        fontSize: 10
                    }
                },
                series: {
                    // custom (shorter) names for legend
                    0: {labelInLegend: 'Durchschnitt'},
                    1: {labelInLegend: 'Wichtigkeit'},
                    2: {labelInLegend: 'Erfolgschance'},
                    3: {labelInLegend: 'Kontrolle'},
                    4: {labelInLegend: 'Bedeutsamkeit'}
                },
                width: 800,
                height: 500,
                curveType: "function",
                pointShape: "circle",
                pointSize: 4
            }
        };
    },
    methods: {
        async fetchChartData() {
            try {
                const response = await axiosInstance.get(GET_PATIENT_MOOD_SCORES + this.patientID);
                this.moodScoresArray = response.data;
                this.chartData = this.convertDataPoints();
            } catch (error) {
                console.log(error);
            }
        },
        convertDataPoints() {
            let result: any[] = [];
            let headers = [];
            // copy values into new headers list
            this.col_names.forEach((e) => headers.push(e));
            headers.unshift("Day");
            result.push(headers);
            let toAdd: (string | number)[] = [];
            this.moodScoresArray.forEach((e) => {
                toAdd.push(new Date(e.date_noted).toLocaleDateString().replace(/\//g, "."));
                toAdd.push(e.overall_motivation);
                toAdd.push(e.perceived_importance);
                toAdd.push(e.chance_of_succ);
                toAdd.push(e.perceived_control);
                toAdd.push(e.meaningfulness);
                result.push(toAdd);
                toAdd = [];
            })
            return result;
        }
    },
    watch: {
        checkedItems(newC, oldC) {
            let result: any[] = [];
            let headers: string[] = [];
            // create new headers list according to selected items
            this.col_names.forEach((e) => {
                if (newC.includes(e)) {
                    headers.push(e);
                }
            });
            headers.unshift("Day");
            result.push(headers);
            let toAdd: (string | number)[] = [];
            this.moodScoresArray.forEach((e) => {
                toAdd.push(new Date(e.date_noted).toLocaleDateString().replace(/\//g, "."));
                if (headers.includes(OVERALL_SCORE)) {
                    toAdd.push(e.overall_motivation);
                }
                if (headers.includes(IMPORTANCE)) {
                    toAdd.push(e.perceived_importance);
                }
                if (headers.includes(CHANCE_OF_SUCCESS)) {
                    toAdd.push(e.chance_of_succ);
                }
                if (headers.includes(CONTROL)) {
                    toAdd.push(e.perceived_control);
                }
                if (headers.includes(MEANINGFULNESS)) {
                    toAdd.push(e.meaningfulness);
                }
                result.push(toAdd);
                toAdd = [];
            })
            // reset chart data
            this.chartData = result;
        }
    },
    mounted() {
        this.fetchChartData();
    }
})
</script>

<style scoped>
.graph-div {
    padding-left: 5%;
    padding-right: 5%;
}
input {
    accent-color: #115bfb;
}
</style>