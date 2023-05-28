<template>
    <h2>Themen und assoziierte Sentimente</h2>
    <p>
        Hier werden die erkannten Themen aus den Journaleinträgen dargestellt.<br>
        Pro Thema wird eine Sentiment Analyse durchgeführt. Es wird untersucht, ob der Patient ein positives,
        neutrales oder negatives Gefühl gegenüber dem Thema aufweist.<br>
        Je öfters ein Thema erwähnt wurde, desto grösser die Schrift.<br><br>
    </p>
    <ul>
        <li><span class="positive" style="font-weight: bold">Grün</span>: vorüberwiegend positiver Sentiment assoziiert
        </li>
        <li><span class="negative" style="font-weight: bold">Rot</span>: vorüberwiegend negativer Sentiment assoziiert
        </li>
        <li><span class="neutral" style="font-weight: bold">Grau</span>: vorüberwiegend neutraler Sentiment assoziiert
        </li>
    </ul>
    <p><br>=> Klicken Sie auf ein Thema, um die Entwicklung der Sentimente über Zeit anzuzeigen!</p>
    <div class="word-cloud-div">
        <div class="word-cloud" id="word-cloud" v-for="item in valenceActivities" :key="item.topic">
            <div class="topic"
                 @click="pressedTopic(item.topic)"
                 :class="{
                'positive': item.overall_sentiment === 'positive',
                'neutral': item.overall_sentiment === 'neutral',
                'negative': item.overall_sentiment === 'negative',
                'selected': item.topic === selectedTopic
                }"
                 :style="{fontSize: `${item.nr_of_occurrences * 20}px`}"
            >
                {{ item.topic }}
            </div>
        </div>
    </div>
        <div class="graph-div">
            <GChart
                    type="LineChart"
                    :options="options"
                    :data="chartData"
            />
        </div>

</template>

<script lang="ts">
import {defineComponent} from "vue";
import axiosInstance from "@/services/http/http-common";
import {GET_TOPICS_SENTIMENTS, GET_VALENCE_DATA} from "@/constants/http/api";
import type {AvgValenceActivityDTO, ValenceChartDataDTO, ValenceDataPointDTO} from "@/DTOs/valenceActivityDTO";
import {GChart} from "vue-google-charts";

export default defineComponent({
    name: "TopicsAndSentiments",
    components: {GChart},
    props: ['patientId'],
    data() {
        return {
            patientID: this.$props.patientId,
            valenceActivities: [] as AvgValenceActivityDTO[],
            options: {
                title: "Sentiment-Graph zum selektierten Thema",
                hAxis: {
                    title: "Zeitverlauf",
                },
                vAxis: {
                    title: "Sentiment",
                    ticks: [-3, -2, -1, 0, 1, 2, 3]
                },
                legend: "none",
                width: 800,
                height: 500,
                curveType: "function",
                pointShape: "circle",
                pointSize: 4
            },
            selectedTopic: "",
            chartData: [] as any,
            valenceData: [] as ValenceChartDataDTO[]
        }
    },
    methods: {
        pressedTopic(topic: string): void {
            this.valenceData.forEach((e) => {
                    if (e.topic == topic) {
                        this.chartData = this.parseChartData(e.data);
                    }
                }
            )
            this.selectedTopic = topic;
        },
        parseChartData(data: ValenceDataPointDTO[]) {
            let result = [];
            let headers = ["Date", "Sentiment"];
            result.push(headers);
            let toAdd: (string | number)[] = [];
            data.forEach((e) => {
                toAdd.push(new Date(e.date).toLocaleDateString().replace(/\//g, "."));
                toAdd.push(e.sentiment_score);
                console.log("Sentiment: ", e.sentiment_score)
                result.push(toAdd);
                toAdd = [];
            })
            return result
        },
        async fetchChartData(): Promise<void> {
            try {
                const response = await axiosInstance.get(GET_VALENCE_DATA + this.patientID);
                this.valenceData = response.data;
                console.log("Data: ", this.valenceData)
            } catch (error) {
                console.log(error);
            }
        },
        async fetchTopicSentiments(): Promise<void> {
            try {
                const response = await axiosInstance.get(GET_TOPICS_SENTIMENTS + this.patientID);
                this.valenceActivities = response.data;
            } catch (error) {
                console.log(error);
            }
        }
    },
    mounted() {
        this.fetchTopicSentiments();
        this.fetchChartData();
    }
})
</script>

<style scoped>

ul {
    padding-left: 5%;
    padding-right: 5%;
    list-style-type: none;
}

.word-cloud-div {
    padding-left: 5%;
    padding-right: 8%;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-left: 5%;
    margin-right: 25%;
    border-style: dotted;
    border-color: #000;
}

.topic {
    padding-right: 5px;
}

.positive {
    color: #0f9015;
}

.neutral {
    color: #767678;
}

.negative {
    color: #d51c3f;
}

.selected {
    text-shadow: 0 0 20px #fbd411;
}

</style>