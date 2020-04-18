<template>
  <v-col cols="12" md="6" class="DataCard">
    <residence-pacients-bar-chart
      :title="$t('居住地別の感染者数')"
      :title-id="'number-of-confirmed-cases'"
      :chart-id="'residence-pacients-bar-chart-patients'"
      :chart-data="residencePatientsGraph"
      :date="Data.patients.date"
      :info="sumInfoOfPatients"
      :unit="$t('人')"
      :url="'https://www.pref.ishikawa.lg.jp/kansen/coronakennai.html'"
    />
  </v-col>
</template>

<script>
import Data from '@/data/data.json'
import formatGraph from '@/utils/formatGraph'
import formatResidenceGraph from '@/utils/formatResidenceGraph'
import ResidencePacientsBarChart from '@/components/ResidencePacientsBarChart.vue'

export default {
  components: {
    ResidencePacientsBarChart
  },
  data() {
    // 感染者数グラフ
    const patientsGraph = formatGraph(Data.patients_summary.data)

    // 居住地別感染者グラフ
    const residencePatientsGraph = formatResidenceGraph(
      Data.residence_pacients.data
    )

    const sumInfoOfPatients = {
      lText: patientsGraph[
        patientsGraph.length - 1
      ].cumulative.toLocaleString(),
      sText: this.$t('{date}の累計', {
        date: patientsGraph[patientsGraph.length - 1].label
      }),
      unit: this.$t('人')
    }

    const data = {
      Data,
      residencePatientsGraph,
      sumInfoOfPatients
    }
    return data
  }
}
</script>
