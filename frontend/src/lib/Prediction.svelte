<script lang="ts">
    import { onMount } from 'svelte';
    import * as d3 from 'd3'; 

    export let visibility: string = 'hidden';

    onMount(() => {
        const data = [10, 20, 30, 40, 50];

        const width = 640;
        const height = 480;
        const margin = { top: 20, right: 30, bottom: 40, left: 90 };

        const svg = d3.select('#bar-chart')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        const x = d3.scaleLinear()
            .domain([0, d3.max(data)])
            .range([0, width - margin.left - margin.right]);

        const y = d3.scaleBand()
            .domain(data.map((d, i) => i.toString()))
            .range([0, height - margin.top - margin.bottom])
            .padding(0.1);

        svg.append('g')
            .selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
            .attr('x', 0)
            .attr('y', (d: number, i: number) => y(i.toString()))
            .attr('width', (d: number) => x(d))
            .attr('height', y.bandwidth())
            .attr('fill', 'steelblue');

        svg.append('g')
            .call(d3.axisLeft(y).tickFormat((d: number, i: number) => `Item ${i + 1}`));

        svg.append('g')
            .attr('transform', `translate(0,${height - margin.top - margin.bottom})`)
            .call(d3.axisBottom(x));
    });
</script>

<style>
    .vertical-line {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 50%;
      width: 1px;
      background-color: rgb(53, 52, 52); 
      transform: translateX(-50%);
      opacity: 0;
      transition: opacity 0.9s ease-in-out;
    }
    
    .visible {
      opacity: 1;
    }

    .bar-chart-container {
        position: absolute;
        right: 9.5%; 
        top: 13%; 
        display: flex;
        flex-direction: column; 
        align-items: flex-end;
        margin-top: 2rem; 
        transition: transform 0.3s ease;
    }
  </style>
  
<div class="vertical-line {visibility === 'visible' ? 'visible' : ''}" style="visibility: {visibility};"></div>

<div class="bar-chart-container {visibility === 'visible' ? 'visible' : ''}" style="visibility: {visibility};">
    <svg id="bar-chart"></svg>
</div>