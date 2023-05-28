<template>
    <NavBar/>
    <h1>Patient ID: {{ patientID }}</h1>
    <JournalEntrySummary :patient-id="patientID"/>
    <TopicsAndSentiments :patient-id="patientID"/>
    <MotivationAnalysis :patient-id="patientID"/>
</template>

<script lang="ts">
import "@/styles/style.css"
import {defineComponent} from "vue";

import MotivationAnalysis from "@/components/MotivationAnalysis.vue";
import NavBar from "@/components/Navbar.vue";
import JournalEntrySummary from "@/components/JournalEntrySummary.vue";
import TopicsAndSentiments from "@/components/TopicsAndSentiments.vue";

export default defineComponent({
    name: 'PatientAView',
    components: { TopicsAndSentiments, JournalEntrySummary, NavBar, MotivationAnalysis},
    data() {
        return {
            patientID: "12",
        }
    }
})
</script>

<style scoped>
h1 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2d3748;
    margin: 0;
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
}
</style>