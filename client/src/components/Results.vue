<template>
    <div class="chartPage">
        <b-form-select v-model="selectBox.selected" :options="selectBox.options" @change="changeSelectBox"></b-form-select>
        <apexchart width="500" type="line" :options="options" :series="series"></apexchart>

    </div>
</template>
<style>
#chart {
  max-width: 650px;
  margin: 35px auto;
}
</style>
<script>


import Vue from 'vue'
import VueApexCharts from 'vue-apexcharts'

Vue.component('apexchart', VueApexCharts)

export default {
  data() {
    return {
        selectBox: {
            selected: "chicago",
            options: [
              { value: 'chicago', text: 'Chicago' },
              { value: 'neopolitan', text: 'Neopolitan' },
              { value: 'sicilian', text: 'Sicilian' },
              { value: 'tomato', text: 'Tomato' },
            ]
        },
      options: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: [2017, 201704, 201708, 2018, 201804, 201808, 2019, 201904]
        }
      },
      series: [
            {
                name: 'Sales Predict',
                data: [30, 40, 45, 50, 49, 60, 70, 80]
            },
            {
                name: 'General Sales',
                data: [30, 40, 45, 50, 49, 100, 70, 50]
            },
        ]
    }
  },
    methods: {
        changeSelectBox(){
            console.log(this.selectBox.selected);
            this.series[0].data = [40, 50, 80, 100, 49, 60, 70, 80];
            console.log(this.selectBox.selected);
            this.series[1].data = [60, 73, 50, 90, 55, 56, 72, 80];
            console.log(this.selectBox.selected);
            this.series[2].data = [65, 70, 62, 95, 51, 52, 68, 90];
        }
    }
}

</script>
